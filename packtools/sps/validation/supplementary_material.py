from lxml import etree
from langdetect import detect
from packtools.sps.models.supplementary_material import XmlSupplementaryMaterials
from packtools.sps.models.media import XmlMedias
from packtools.sps.models.graphic import Graphic, XmlGraphic
from packtools.sps.validation.graphic import GraphicValidation
from packtools.sps.validation.media import MediaValidation
from packtools.sps.validation.utils import build_response


class SupplementaryMaterialValidation:
    def __init__(self, data, params, node=None):
        """
        Inicializa a validação de um material suplementar.

        Args:
            supp (dict): Dados do material suplementar extraídos do modelo
        """
        self.data = data
        self.params = params
        self.node = node

    def validate(self):
        """
        Executa todas as validações definidas.
        """
        for media in self.node.xpath(".//media"):
            if media.data:
                yield from MediaValidation(media.data, self.params).validate()

        for graphic in self.node.xpath(".//graphic"):
            if graphic.data:
                yield from GraphicValidation(graphic, self.params).validate()

        yield self.validate_sec_type()
        yield self.validate_label()
        yield self.validate_not_in_app_group()

    def validate_sec_type(self):
        """
        Verifica se <supplementary-material> está inserido em <sec>, caso esteja, valida @sec-type="supplementary-material"
        """
        if self.data.get("parent_suppl_mat") == "sec":
            sec_type = self.data.get("sec_type")
            valid = sec_type == "supplementary-material"
            return build_response(
                title="@sec-type",
                parent=self.data,
                item="sec",
                sub_item="supplementary-material",
                is_valid=valid,
                validation_type="match",
                expected="<sec sec-type='supplementary-material'>",
                obtained=self.data.get("parent_tag"),
                advice=f'In <sec sec-type="{sec_type}"><supplementary-material> replace "{sec_type}" with "supplementary-material".',
                error_level=self.params["sec_type_error_level"],
                data=self.data,
            )

    def validate_label(self):
        """
        Verifica a presença obrigatória de <label>
        """
        label = self.data.get("label")
        valid = bool(label)
        return build_response(
            title="label",
            parent=self.data,
            item="supplementary-material",
            sub_item="label",
            is_valid=valid,
            validation_type="exist",
            expected="<label> in <supplementary-material>",
            obtained=label,
            advice="Add label in <supplementary-material>: <supplementary-material><label>. Consult SPS documentation for more detail.",
            error_level=self.params["label_error_level"],
            data=self.data,
        )

    def validate_not_in_app_group(self):
        """
        Ensures that <supplementary-material> does not occur inside <app-group> and <app>.
        """
        valid = self.data.get("parent_suppl_mat") not in ["app-group", "app"]
        return build_response(
            title="Prohibition of <supplementary-material> inside <app-group> and <app>",
            parent=self.data,
            item="supplementary-material",
            sub_item="parent",
            is_valid=valid,
            validation_type="forbidden",
            expected="Outside <app-group> and <app>",
            obtained=self.data.get("parent_tag"),
            advice="Do not use <supplementary-material> inside <app-group> or <app>.",
            error_level=self.params["app_group_error_level"],
            data=self.data,
        )

    def validate_prohibited_inline(self):
        """
        Ensures that <inline-supplementary-material> is not used.
        """

        nodes = self.xml_tree.xpath(".//inline-supplementary-material")
        obtained = etree.tostring(nodes[0]) if nodes else "None"
        valid = not bool(nodes)

        return build_response(
            title="Prohibition of inline-supplementary-material",
            parent=self.data,
            item="inline-supplementary-material",
            sub_item=None,
            is_valid=valid,
            validation_type="forbidden",
            expected="No <inline-supplementary-material>",
            obtained=obtained,
            advice="The use of <inline-supplementary-material> is prohibited.",
            error_level=self.params["inline_error_level"],
            data=self.data,
        )


class ArticleSupplementaryMaterialValidation:
    def __init__(self, xml_tree, params):
        self.article_supp = list(XmlSupplementaryMaterials(xml_tree).items)
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        for supp in self.article_supp:
            yield from SupplementaryMaterialValidation(
                supp, self.xml_tree, self.params
            ).validate()

        SupplementaryMaterialValidation(
            {}, self.xml_tree, self.params
        ).validate_prohibited_inline()
