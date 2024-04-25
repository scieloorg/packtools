from packtools.sps.models.article_author_notes import AuthorNotes
from packtools.sps.validation.utils import format_response


class AuthorNotesValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.author_notes = AuthorNotes(self.xmltree)

    def corresp_validation(self):
        for author_note in self.author_notes.data:
            corresp = author_note.get("corresp")
            is_valid = corresp != []
            yield format_response(
                title="Author notes validation",
                parent=author_note.get("parent"),
                parent_id=author_note.get("parent_id"),
                item="author-notes",
                sub_item="corresp",
                validation_type="exist",
                is_valid=is_valid,
                expected=corresp if is_valid else "corresponding author identification",
                obtained=corresp,
                advice="provide identification data of the corresponding author",
                data=author_note
            )

    def fn_type_validation(self):
        for author_note in self.author_notes.data:
            fn_types = author_note.get("fn_types")
            fn_numbers = author_note.get("fn_numbers")
            is_valid = len(fn_types) == fn_numbers
            yield format_response(
                title="Author notes validation",
                parent=author_note.get("parent"),
                parent_id=author_note.get("parent_id"),
                item="fn",
                sub_item="@fn-type",
                validation_type="match",
                is_valid=is_valid,
                expected=f"{fn_numbers} fn-types",
                obtained=f"{len(fn_types)} fn-types",
                advice="provide one <@fn-type> for each <fn> tag",
                data=author_note
            )


