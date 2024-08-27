from packtools.sps.validation.utils import format_response
from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.models.article_dates import HistoryDates


# Classe base para validação de artigos, implementando a lógica comum de validação de artigos relacionados
class ValidationBase:
    def __init__(self, xml_tree, related_article_type):
        # Inicializa a árvore XML e configura o tipo de artigo relacionado a ser validado
        self.xml_tree = xml_tree
        self.article_lang = xml_tree.get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )  # Obtém o idioma do artigo
        self.article_type = xml_tree.xpath(".")[0].get(
            "article-type"
        )  # Obtém o tipo de artigo
        # Filtra os artigos relacionados com base no tipo especificado
        self.related_articles = [
            article
            for article in RelatedItems(xml_tree).related_articles
            if article.get("related-article-type") == related_article_type
        ]

    # Método principal de validação de artigos relacionados, que pode ser sobrescrito por subclasses
    def validate_related_article(
        self,
        expected_related_article_type,
        expected_message,
        advice,
        error_level="ERROR",
    ):
        if (
            self.article_type == "correction"
        ):  # Verifica se o tipo de artigo é uma correção
            if (
                not self.related_articles
            ):  # Se não houver artigos relacionados, retorna um erro
                yield self._format_error_response(
                    expected=f'at least one <related-article related-article-type="{expected_related_article_type}">',
                    advice=f'provide <related-article related-article-type="{expected_related_article_type}">',
                    error_level=error_level,
                )
            else:
                # Se houver artigos relacionados, valida cada um e retorna um sucesso
                for article in self.related_articles:
                    yield self._format_success_response(
                        article, expected_message, error_level
                    )

    # Método auxiliar para formatar uma resposta de erro
    def _format_error_response(self, expected, advice, error_level):
        return format_response(
            title="errata",
            parent="article",
            parent_id=None,
            parent_article_type=self.article_type,
            parent_lang=self.article_lang,
            item="related-article",
            sub_item="@related-article-type",
            validation_type="exist",
            is_valid=False,
            expected=expected,
            obtained=None,
            advice=advice,
            data=None,
            error_level=error_level,
        )

    # Método auxiliar para formatar uma resposta de sucesso
    def _format_success_response(self, article, expected_message, error_level):
        return format_response(
            title="errata",
            parent=article.get("parent"),
            parent_id=article.get("parent_id"),
            parent_article_type=article.get("parent_article_type"),
            parent_lang=self.article_lang,
            item="related-article",
            sub_item="@related-article-type",
            validation_type="match",
            is_valid=True,
            expected=expected_message,
            obtained=f'<related-article ext-link-type="{article.get("ext-link-type")}" '
            f'id="{article.get("id")}" related-article-type="{article.get("related-article-type")}" '
            f'xlink:href="{article.get("href")}"/>',
            advice=None,
            data=article,
            error_level=error_level,
        )


# Classe para validação de erratas, herda da ValidationBase e especifica o tipo "corrected-article"
class ErrataValidation(ValidationBase):
    def __init__(self, xml_tree):
        # Chama o construtor da classe base com o tipo "corrected-article"
        super().__init__(xml_tree, related_article_type="corrected-article")

    # Método de validação específico para erratas
    def validate_related_article(self, error_level="ERROR"):
        yield from super().validate_related_article(
            expected_related_article_type="corrected-article",
            expected_message='at least one <related-article related-article-type="corrected-article">',
            advice='provide <related-article related-article-type="corrected-article">',
            error_level=error_level,
        )


# Classe para validação de artigos corrigidos, herda da ValidationBase e especifica o tipo "correction-forward"
class CorrectedArticleValidation(ValidationBase):
    def __init__(self, xml_tree):
        # Chama o construtor da classe base com o tipo "correction-forward"
        super().__init__(xml_tree, related_article_type="correction-forward")
        # Filtra as datas históricas que têm o tipo "corrected"
        self.history_dates = [
            date
            for date in HistoryDates(xml_tree).history_dates()
            if "corrected" in date.get("history")
        ]

    # Método de validação específico para artigos corrigidos
    def validate_related_article(self, error_level="ERROR"):
        # Executa a validação básica de artigos relacionados
        yield from super().validate_related_article(
            expected_related_article_type="correction-forward",
            expected_message='at least one <related-article related-article-type="correction-forward">',
            advice='provide <related-article related-article-type="correction-forward">',
            error_level=error_level,
        )

        # Verifica se o número de datas corrigidas é menor que o número de artigos relacionados
        history_date_count = len(self.history_dates)
        related_article_count = len(self.related_articles)

        if history_date_count < related_article_count:
            # Retorna um erro se o número de datas corrigidas for insuficiente
            yield format_response(
                title="errata",
                parent="article",
                parent_id=None,
                parent_article_type=self.article_type,
                parent_lang=self.article_lang,
                item="related-article",
                sub_item="@related-article-type",
                validation_type="exist",
                is_valid=False,
                expected='equal numbers of <related-article type="correction-forward"> and <date type="corrected">',
                obtained=f'{related_article_count} <related-article type="correction-forward"> and {history_date_count} <date type="corrected">',
                advice='for each <related-article type="correction-forward">, there must be a corresponding <date type="corrected"> in <history>',
                data=self.history_dates,
                error_level=error_level,
            )
