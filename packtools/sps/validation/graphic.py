from packtools.sps.validation.utils import build_response
from packtools.sps.validation.visual_resource_base import VisualResourceBaseValidation


class GraphicValidation(VisualResourceBaseValidation):
    def validate(self):
        yield from super().validate()