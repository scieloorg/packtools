import io
import os
import re

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from lxml import etree
from PIL import Image

NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_ASVG = 'http://schemas.microsoft.com/office/drawing/2016/SVG/main'
NS_SVG = 'http://www.w3.org/2000/svg'
# Extensão do Office 2016+ que liga um SVG à imagem PNG de reserva.
SVG_BLIP_EXT_URI = '{96DAC541-7B7A-43D3-8B79-37D633B846F1}'

# Fatores para px (96 por polegada), como no CSS.
_SVG_UNITS = {'': 1.0, 'px': 1.0, 'pt': 96 / 72, 'pc': 16.0, 'mm': 96 / 25.4, 'cm': 96 / 2.54, 'in': 96.0}
_SVG_LENGTH = re.compile(r'^\s*([0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s*([a-z]*)\s*$')

# Largura do PNG de reserva gerado quando não vem um junto com o SVG.
_FALLBACK_WIDTH_PX = 200


def read_png_size(path):
    """
    Retorna (largura, altura) em pixels. Levanta ValueError se o arquivo não
    existir ou não for PNG.
    """
    _check_file(path)
    try:
        with Image.open(path) as im:
            fmt = im.format
            size = im.size
    except Exception as exc:
        raise ValueError(f'arquivo de logo ilegível: {path} ({exc})') from exc
    if fmt != 'PNG':
        raise ValueError(f'logo precisa ser PNG ou SVG, recebido {fmt}: {path}')
    return size


def read_svg_size(path):
    """
    Retorna (largura, altura) do SVG em px, a partir de width/height
    absolutos ou do viewBox. Levanta ValueError se não for SVG ou se não
    houver tamanho. Referências externas do SVG (href, use, @import) são
    mantidas como vieram; o LibreOffice 24.2 não as busca ao gerar o PDF.
    """
    _check_file(path)
    root = _parse_svg(path)
    width = _svg_length(root.get('width'))
    height = _svg_length(root.get('height'))
    if width and height:
        return width, height
    view_box = (root.get('viewBox') or '').replace(',', ' ').split()
    if len(view_box) == 4:
        try:
            vb_w, vb_h = float(view_box[2]), float(view_box[3])
        except ValueError:
            vb_w = vb_h = 0
        if vb_w > 0 and vb_h > 0:
            return vb_w, vb_h
    raise ValueError(f'SVG sem width/height absolutos nem viewBox: {path}')


def read_logo_size(path):
    """
    Detecta o formato pelo conteúdo e retorna (tipo, largura, altura), com
    tipo 'png' ou 'svg'. Levanta ValueError para qualquer outro formato.
    """
    _check_file(path)
    if _looks_like_svg(path):
        width, height = read_svg_size(path)
        return 'svg', width, height
    width, height = read_png_size(path)
    return 'png', width, height


def add_logo_run(paragraph, path, width_emu, height_emu, kind='png', fallback_path=None):
    """
    Insere o logo como imagem em linha, com largura e altura explícitas.
    Para SVG, insere um PNG de reserva e liga o SVG a ele (svgBlip).
    """
    run = paragraph.add_run()
    if kind == 'svg':
        fallback = fallback_path or _transparent_png(width_emu, height_emu)
        shape = run.add_picture(fallback, width=int(width_emu), height=int(height_emu))
        _attach_svg(run, shape, path)
    else:
        shape = run.add_picture(path, width=int(width_emu), height=int(height_emu))
    # Sem dist*, o LibreOffice aplica 0,32 cm de espaçamento em volta da imagem.
    for side in ('distT', 'distB', 'distL', 'distR'):
        shape._inline.set(side, '0')
    return shape


def _check_file(path):
    if not path or not os.path.isfile(path):
        raise ValueError(f'arquivo de logo não encontrado: {path}')


def _looks_like_svg(path):
    with open(path, 'rb') as f:
        head = f.read(8192)
    return head.lstrip().startswith(b'<') and b'<svg' in head


def _parse_svg(path):
    # Sem entidades externas nem rede: o arquivo vem de fora.
    parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    try:
        root = etree.parse(path, parser).getroot()
    except etree.XMLSyntaxError as exc:
        raise ValueError(f'SVG inválido: {path} ({exc})') from exc
    if root.tag != f'{{{NS_SVG}}}svg':
        raise ValueError(f'arquivo não é SVG: {path}')
    return root


def _svg_length(value):
    """Comprimento absoluto em px, ou None (ausente, porcentagem, unidade relativa)."""
    match = _SVG_LENGTH.match(value or '')
    if not match or match.group(2) not in _SVG_UNITS:
        return None
    length = float(match.group(1)) * _SVG_UNITS[match.group(2)]
    return length if length > 0 else None


def _transparent_png(width_emu, height_emu):
    width = _FALLBACK_WIDTH_PX
    height = max(1, round(width * height_emu / width_emu))
    stream = io.BytesIO()
    Image.new('RGBA', (width, height), (255, 255, 255, 0)).save(stream, format='PNG')
    stream.seek(0)
    return stream


def _attach_svg(run, shape, svg_path):
    with open(svg_path, 'rb') as f:
        svg_bytes = f.read()
    story_part = run.part
    package = story_part.package
    partname = package.next_partname('/word/media/image%d.svg')
    svg_part = Part(PackURI(partname), 'image/svg+xml', svg_bytes, package)
    rid = story_part.relate_to(svg_part, RT.IMAGE)
    blip = shape._inline.find(f'.//{{{NS_A}}}blip')
    ext_lst = blip.find(f'{{{NS_A}}}extLst')
    if ext_lst is None:
        ext_lst = etree.SubElement(blip, f'{{{NS_A}}}extLst')
    ext = etree.SubElement(ext_lst, f'{{{NS_A}}}ext', uri=SVG_BLIP_EXT_URI)
    svg_blip = etree.SubElement(ext, f'{{{NS_ASVG}}}svgBlip', nsmap={'asvg': NS_ASVG})
    svg_blip.set(f'{{{NS_R}}}embed', rid)
