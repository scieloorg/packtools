from packtools.sps.models.alternatives import ArticleAlternatives
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationAlternativesException


class AlternativeValidation:
    def __init__(self, alternative, children_list):
        self.alternative = alternative
        self.obtained_children = alternative.get("alternative_children")
        self.children_list = children_list

    def validation(self):
        """
            Check whether the alternatives match the tag that contains them.

            XML input
            ---------
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <table-wrap>
                        <alternatives>
                            <p />
                        </alternatives>
                    </table-wrap>
                </body>
                <sub-article article-type="translation" xml:lang="en" id="TRen">
                    <body>
                        <fig>
                            <alternatives>
                                <title />
                                <abstract />
                            </alternatives>
                        </fig>
                    </body>
                </sub-article>
            </article>

            Params
            ------
            alternative : dict, such as:
                {
                    'alternative_children': ['graphic', 'table'],
                    'alternative_parent': 'table-wrap',
                    'parent': 'article',
                    'parent_id': None
                }

            children_list : list, such as:
                ["graphic", "table"]

            Returns
            -------
            list[dict], such as:
                [
                    {
                        'title': 'Alternatives validation',
                        'parent': 'article',
                        'parent_id': None,
                        'item': 'table-wrap',
                        'sub_item': 'alternatives',
                        'validation_type': 'value in list',
                        'expected_value': ['graphic', 'table'],
                        'got_value': ['p'],
                        'response': 'ERROR',
                        'message': "Got ['p'], expected ['graphic', 'table']",
                        'advice': "Provide child tags according to the list: ['graphic', 'table']",
                        'data': {
                            'alternative_children': ['p'],
                            'alternative_parent': 'table-wrap',
                            'parent': 'article',
                            'parent_id': None
                        }
                    },
                ]
        """
        for tag in self.obtained_children:
            if tag not in (self.children_list or []):
                parent = self.alternative.get("alternative_parent")
                yield format_response(
                    title="Alternatives validation",
                    parent=self.alternative.get("parent"),
                    parent_id=self.alternative.get("parent_id"),
                    item=parent,
                    sub_item="alternatives",
                    validation_type="value in list",
                    is_valid=False,
                    expected=self.children_list,
                    obtained=self.obtained_children,
                    advice=f'Add {self.children_list} as sub-elements of {parent}/alternatives',
                    data=self.alternative
                )


class AlternativesValidation:
    def __init__(self, xmltree, parent_children_dict=None):
        self.xmltree = xmltree
        self.parent_children_dict = parent_children_dict
        self.alternatives = ArticleAlternatives(xmltree).alternatives()

    def validation(self, parent_children_dict=None):
        parent_children_dict = parent_children_dict or self.parent_children_dict
        for alternative in self.alternatives:
            parent = alternative.get("alternative_parent")
            if not parent_children_dict:
                raise ValidationAlternativesException(f"The element '{parent}' is not configured to use 'alternatives'."
                                                      " Provide alternatives parent and children")
            children_list = parent_children_dict.get(parent)
            if children_list is None:
                raise ValidationAlternativesException(f"The element '{parent}' is not configured to use 'alternatives'."
                                                      " Provide alternatives parent and children")
            yield from AlternativeValidation(alternative, children_list).validation()


