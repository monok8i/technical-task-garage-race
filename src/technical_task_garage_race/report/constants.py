"""Constants for the report generation.

The values in this module define the workbook layout and the regular
expressions used to extract metadata from transcript file names.
"""

import re

SHEET_NAME = "Лист1"
HEADER_ROW = 2
DATA_START_ROW = 3
RED = "FF0000"

PHONE_RE = re.compile(r"(?<!\d)(?:\+?38)?0\d{9}(?!\d)")
NAME_RE = re.compile(
    r"(?:мене звати|я\s+звати|моє ім['’]?я|ім['’]?я)\s+([A-ЯІЇЄҐA-Z][а-яіїєґa-z'-]+)",
    re.IGNORECASE,
)
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
