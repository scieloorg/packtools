import gettext
from contextvars import ContextVar
from pathlib import Path


DOMAIN = "packtools_sps"
LOCALE_DIR = Path(__file__).resolve().parent / "locale"

_translation = ContextVar(
    "packtools_sps_translation",
    default=gettext.NullTranslations(),
)


def set_locale(lang="en"):
    translation = gettext.translation(
        DOMAIN,
        localedir=str(LOCALE_DIR),
        languages=[lang],
        fallback=True,
    )

    _translation.set(translation)


def _(message):
    return _translation.get().gettext(message)
