import os

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.utils.request_utils import download_remote_asset
from packtools.sps.formats.pdf.utils.file_utils import resolve_asset_path
