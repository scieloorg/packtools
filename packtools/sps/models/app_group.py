import warnings as _warnings

from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.label_and_caption import LabelAndCaption
from packtools.sps.models.media import Media
from packtools.sps.models.graphic import Graphic


class App(LabelAndCaption):
    @property
    def id(self):
        return self.node.get("id")

    @property
    def graphics(self):
        """Retorna uma lista de dados de gráficos (<graphic>) dentro do <app>."""
        return [Graphic(graphic).data for graphic in self.node.xpath(".//graphic")]

    @property
    def media(self):
        """Retorna uma lista de dados de mídias (<media>) dentro do <app>."""
        return [Media(media).data for media in self.node.xpath(".//media")]

    @property
    def data(self):
        """Inclui os atributos de LabelAndCaption e adiciona 'id', 'graphics' e 'media'."""
        base_data = super().data or {}
        return {
            **base_data,
            "id": self.id,
            "graphics": self.graphics,
            "media": self.media,
        }


def __getattr__(name):
    _moved = {
        "XmlAppGroup": "packtools.sps.validation.models.app_group",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.app_group is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
