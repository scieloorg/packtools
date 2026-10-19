"""Localização de imagens referenciadas no XML (local ou remota) e leitura do tamanho natural."""

import hashlib
import os
import tempfile
from urllib.request import Request, urlopen

from PIL import Image

EMU_PER_INCH = 914400

# Herdado do old_pdf: sem metadado de DPI, assume 300 (resolução de impressão);
# um valor menor faria a imagem sair maior que o pretendido.
_FALLBACK_DPI = 300.0


class Assets:
    """Resolve href -> caminho local, baixando URLs uma vez por documento."""

    def __init__(self, assets_dir=None, timeout=20):
        """assets_dir: pasta onde procurar hrefs relativos; timeout: segundos por download."""
        self.assets_dir = assets_dir
        self.timeout = timeout
        self._cache_dir = None

    def path(self, href):
        """Caminho local existente do href, ou None."""
        if not href:
            return None
        href = str(href)
        if href.startswith(("http://", "https://")):
            return self._download(href)
        candidates = (
            [href]
            if os.path.isabs(href)
            else [os.path.join(self.assets_dir or "", href), href]
        )
        return next((c for c in candidates if os.path.isfile(c)), None)

    def natural_size(self, href):
        """
        Tamanho natural (largura, altura) da imagem em EMU, pelo DPI do
        arquivo, ou None se ilegível.

        As duas medidas usam o DPI horizontal, para (largura / altura) ser a
        proporção em pixels: é a mesma proporção que o python-docx usa ao
        calcular a altura a partir só da largura.
        """
        path = self.path(href)
        if not path:
            return None
        try:
            with Image.open(path) as im:
                dpi = _dpi(im)
                return (
                    int(im.width / dpi * EMU_PER_INCH),
                    int(im.height / dpi * EMU_PER_INCH),
                )
        except Exception:
            return None

    def natural_width(self, href):
        """Largura natural (EMU) da imagem pelo DPI do arquivo, ou None se ilegível."""
        size = self.natural_size(href)
        return size[0] if size else None

    def _download(self, url):
        """Baixa a URL uma vez para um cache temporário (nome = sha1 da URL + extensão); None se falhar ou vier vazio."""
        if self._cache_dir is None:
            self._cache_dir = tempfile.mkdtemp(prefix="scl_assets_")
        name = os.path.basename(url).split("?")[0].split("#")[0]
        ext = os.path.splitext(name)[1]
        target = os.path.join(
            self._cache_dir, hashlib.sha1(url.encode("utf-8")).hexdigest() + ext
        )
        if not os.path.isfile(target):
            try:
                request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urlopen(request, timeout=self.timeout) as response, open(
                    target, "wb"
                ) as out:
                    out.write(response.read())
            except Exception:
                return None
        return target if os.path.getsize(target) else None


def _dpi(im):
    """DPI horizontal pelos metadados (dpi ou densidade JFIF); senão _FALLBACK_DPI."""
    info = getattr(im, "info", {}) or {}
    dpi = info.get("dpi")
    if isinstance(dpi, tuple) and dpi and dpi[0]:
        return float(dpi[0])
    if isinstance(dpi, (int, float)) and dpi > 0:
        return float(dpi)
    unit, density = info.get("jfif_unit"), info.get("jfif_density")
    if isinstance(density, tuple) and density and density[0]:
        if unit == 1:
            return float(density[0])
        if unit == 2:
            return float(density[0]) * 2.54
    return _FALLBACK_DPI
