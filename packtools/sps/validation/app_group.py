from packtools.sps.models.app_group import XmlAppGroup
from packtools.sps.validation.utils import build_response


class AppValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.apps = list(XmlAppGroup(xmltree).data)
        self.params = params

    def validate(self):
        """
        Executa todas as validações para <app> e <app-group>.

        Yields:
            dict: Resultados de validação
        """
        yield from self.validate_app_existence()
        yield from self.validate_app_id()
        yield from self.validate_app_label()
        yield from self.validate_app_group_wrapper()

    def validate_app_existence(self):
        """
        Valida a existência de elementos <app>.

        Nota: <app> é opcional segundo SciELO, mas esta validação
        fornece informação útil aos editores.

        Yields:
            dict: Resultado de validação (nível informativo)
        """
        if not self.apps:
            yield build_response(
                title="<app> element",
                parent={
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": self.xmltree.get("article-type"),
                    "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                },
                item="app-group",
                sub_item="app",
                validation_type="exist",
                is_valid=False,
                expected="<app> element",
                obtained=None,
                advice="Consider adding an <app> element to include additional content such as appendices.",
                data=None,
                error_level=self.params["app_existence_error_level"],
                advice_text="Consider adding an <app> element to include additional content such as appendices.",
                advice_params={}
            )
        else:
            for app in self.apps:
                yield build_response(
                    title="<app> element",
                    parent=app,
                    item="app-group",
                    sub_item="app",
                    validation_type="exist",
                    is_valid=True,
                    expected=app.get("id"),
                    obtained=app.get("id"),
                    advice=None,
                    data=app,
                    error_level=self.params["app_existence_error_level"],
                    advice_text=None,
                    advice_params=None
                )

    def validate_app_id(self):
        """
        Valida presença obrigatória do atributo @id em <app>.

        Regra SciELO: "Atributo obrigatório para <app>: @id"

        Yields:
            dict: Resultado de validação (CRITICAL se ausente)
        """
        for app in self.apps:
            app_id = app.get("id")
            is_valid = bool(app_id)

            yield build_response(
                title="<app> @id attribute",
                parent=app,
                item="app",
                sub_item="@id",
                validation_type="exist",
                is_valid=is_valid,
                expected="@id attribute in <app>",
                obtained=app_id if is_valid else None,
                advice='Add @id attribute to <app>. Example: <app id="app1">',
                data=app,
                error_level=self.params["app_id_error_level"],
                advice_text='Add @id attribute to <app>. Example: <app id="app1">',
                advice_params=None
            )

    def validate_app_label(self):
        """
        Valida presença obrigatória do elemento <label> em <app>.

        Regra SciELO: "<app> exige o elemento <label> como título do apêndice ou anexo"

        Yields:
            dict: Resultado de validação (CRITICAL se ausente)
        """
        for app in self.apps:
            label = app.get("label")
            is_valid = bool(label)
            app_id_or_placeholder = app.get("id", "?")
            app_id_or_example_fix = app.get("id", "app1")

            yield build_response(
                title="<app> <label> element",
                parent=app,
                item="app",
                sub_item="label",
                validation_type="exist",
                is_valid=is_valid,
                expected="<label> element in <app>",
                obtained=label if is_valid else None,
                advice=f'Add <label> element to <app id="{app_id_or_placeholder}">. '
                       f'Example: <app id="{app_id_or_example_fix}"><label>Appendix 1</label></app>',
                data=app,
                error_level=self.params["app_label_error_level"],
                advice_text='Add <label> element to <app id="{app_id_or_placeholder}">. '
                           'Example: <app id="{app_id_or_example_fix}"><label>Appendix 1</label></app>',
                advice_params={
                    "app_id_or_placeholder": app_id_or_placeholder,
                    "app_id_or_example_fix": app_id_or_example_fix
                }
            )

    def validate_app_group_wrapper(self):
        """
        Valida regras de estrutura de <app-group>.

        Yields:
            dict: Resultados de validação
        """
        yield from self.validate_orphan_apps()
        yield from self.validate_multiple_app_groups()

    def validate_orphan_apps(self):
        """
        Valida que <app> está dentro de <app-group>.

        Regra SciELO: "O elemento <app-group> deve sempre ser usado como agrupador
        do elemento <app>, mesmo se houver somente uma ocorrência deste último"

        Nota: Esta validação verifica se há <app> órfão (fora de <app-group>).

        Yields:
            dict: Resultado de validação (CRITICAL se órfão encontrado)
        """
        # Buscar <app> que estão diretamente em <back>, sem <app-group>
        orphan_apps = self.xmltree.xpath(".//back/app")

        if orphan_apps:
            for orphan in orphan_apps:
                app_id = orphan.get("id", "unknown")

                yield build_response(
                    title="<app-group> wrapper required",
                    parent={
                        "parent": "article",
                        "parent_id": None,
                        "parent_article_type": self.xmltree.get("article-type"),
                        "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                    },
                    item="app",
                    sub_item="app-group",
                    validation_type="wrapper",
                    is_valid=False,
                    expected="<app> inside <app-group>",
                    obtained=f"<app id='{app_id}'> directly in <back>",
                    advice=f'Wrap <app id="{app_id}"> with <app-group>. '
                           f'Example: <back><app-group><app id="{app_id}">...</app></app-group></back>',
                    data={"app_id": app_id},
                    error_level=self.params["app_group_wrapper_error_level"],
                    advice_text='Wrap <app id="{app_id}"> with <app-group>. '
                               'Example: <back><app-group><app id="{app_id}">...</app></app-group></back>',
                    advice_params={
                        "app_id": app_id
                    }
                )

    def validate_multiple_app_groups(self):
        """
        Valida que existe no máximo um <app-group> em <back>.

        Regra SciELO: Deve haver zero ou um <app-group> em <back>

        Yields:
            dict: Resultado de validação (CRITICAL se múltiplos encontrados)
        """
        # Verificar se há múltiplos <app-group> (deve ser 0 ou 1)
        app_groups = self.xmltree.xpath(".//back/app-group")

        if len(app_groups) > 1:
            yield build_response(
                title="Single <app-group> allowed",
                parent={
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": self.xmltree.get("article-type"),
                    "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                },
                item="back",
                sub_item="app-group",
                validation_type="occurrence",
                is_valid=False,
                expected="Zero or one <app-group> in <back>",
                obtained=f"{len(app_groups)} <app-group> elements found",
                advice=f'Merge all {len(app_groups)} <app-group> elements into a single <app-group>.',
                data={"count": len(app_groups)},
                error_level=self.params["app_group_occurrence_error_level"],
                advice_text='Merge all {count} <app-group> elements into a single <app-group>.',
                advice_params={
                    "count": len(app_groups)
                }
            )
