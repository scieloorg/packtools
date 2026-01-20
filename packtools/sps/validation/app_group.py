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
        yield from self.validate_media_accessibility()

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
                advice_text='Add @id attribute to <app>. Example: <app id="{example_id}">',
                advice_params={
                    "example_id": "app1"
                }
            )

    def validate_app_label(self):
        """
        Valida presença obrigatória do elemento <label> em <app>.

        Regra SciELO: "<app> exigem o elemento <label> como título do apêndice ou anexo"

        Yields:
            dict: Resultado de validação (CRITICAL se ausente)
        """
        for app in self.apps:
            label = app.get("label")
            is_valid = bool(label)

            yield build_response(
                title="<app> <label> element",
                parent=app,
                item="app",
                sub_item="label",
                validation_type="exist",
                is_valid=is_valid,
                expected="<label> element in <app>",
                obtained=label if is_valid else None,
                advice=f'Add <label> element to <app id="{app.get("id", "?")}">. '
                       f'Example: <app id="{app.get("id", "app1")}"><label>Appendix 1</label></app>',
                data=app,
                error_level=self.params["app_label_error_level"],
                advice_text='Add <label> element to <app id="{app_id}">. '
                           'Example: <app id="{app_id}"><label>{example_label}</label></app>',
                advice_params={
                    "app_id": app.get("id", "?"),
                    "example_label": "Appendix 1"
                }
            )

    def validate_app_group_wrapper(self):
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
        else:
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

    def validate_media_accessibility(self):
        """
        Valida acessibilidade de elementos <media> dentro de <app>.

        Regra SciELO: "Para acessibilidade recomenda-se que vídeos e áudios venham
        com sua descrição em <alt-text> e/ou <long-desc> mais a transcrição do
        conteúdo na seção <sec sec-type='transcript'>"

        Yields:
            dict: Resultados de validação para cada mídia
        """
        for app in self.apps:
            media_list = app.get("media", [])

            for media in media_list:
                # Validar presença de alt-text OU long-desc
                alt_text = media.get("alt_text")
                long_desc = media.get("long_desc")
                has_description = bool(alt_text or long_desc)

                media_href = media.get("xlink_href", "unknown")

                yield build_response(
                    title="Media accessibility: alt-text or long-desc",
                    parent=app,
                    item="media",
                    sub_item="alt-text/long-desc",
                    validation_type="exist",
                    is_valid=has_description,
                    expected="<alt-text> or <long-desc> in <media>",
                    obtained=f"alt-text: {bool(alt_text)}, long-desc: {bool(long_desc)}",
                    advice=f'Add <alt-text> or <long-desc> to <media xlink:href="{media_href}"> '
                           f'for accessibility. Example: <media ...><alt-text>Description</alt-text></media>',
                    data=media,
                    error_level=self.params["media_alt_text_error_level"],
                    advice_text='Add <alt-text> or <long-desc> to <media xlink:href="{media_href}"> '
                               'for accessibility. Example: <media ...><alt-text>Description</alt-text></media>',
                    advice_params={
                        "media_href": media_href
                    }
                )

                # Validar referência a transcrição
                xref_sec_rid = media.get("xref_sec_rid")
                has_transcript_ref = bool(xref_sec_rid)

                yield build_response(
                    title="Media accessibility: transcript reference",
                    parent=app,
                    item="media",
                    sub_item="xref[@ref-type='sec']",
                    validation_type="exist",
                    is_valid=has_transcript_ref,
                    expected="<xref ref-type='sec' rid='...'> referencing <sec sec-type='transcript'>",
                    obtained=xref_sec_rid if has_transcript_ref else None,
                    advice=f'Add <xref ref-type="sec" rid="TR1"/> inside <media xlink:href="{media_href}"> '
                           f'to reference transcript section. '
                           f'Example: <media ...><xref ref-type="sec" rid="TR1"/></media>',
                    data=media,
                    error_level=self.params["media_transcript_error_level"],
                    advice_text='Add <xref ref-type="sec" rid="{transcript_id}"/> inside <media xlink:href="{media_href}"> '
                               'to reference transcript section. '
                               'Example: <media ...><xref ref-type="sec" rid="{transcript_id}"/></media>',
                    advice_params={
                        "media_href": media_href,
                        "transcript_id": "TR1"
                    }
                )
