from ..models.supplementary_material import ArticleSupplementaryMaterials
from ..validation.utils import format_response


class SupplementaryMaterialValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.supplementary_materials = ArticleSupplementaryMaterials(xmltree).data()

    def validate_supplementary_material_existence(self, error_level="WARNING"):
        for supp in self.supplementary_materials:
            yield format_response(
                title="validation of <supplementary-material> elements",
                parent=supp.get("parent"),
                parent_id=supp.get("parent_id"),
                parent_article_type=supp.get("parent_article_type"),
                parent_lang=supp.get("parent_lang"),
                item="supplementary-material",
                sub_item=None,
                validation_type="exist",
                is_valid=True,
                expected=supp.get("supplementary_material_id"),
                obtained=supp.get("supplementary_material_id"),
                advice=None,
                data=supp,
                error_level="OK",
            )
        else:
            yield format_response(
                title="validation of <supplementary-material> elements",
                parent="article",
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="supplementary-material",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<supplementary-material> element",
                obtained=None,
                advice="Consider adding a <supplementary-material> element to provide additional data or materials related to the article.",
                data=None,
                error_level=error_level,
            )
