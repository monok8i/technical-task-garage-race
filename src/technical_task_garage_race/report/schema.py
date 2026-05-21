"""Data structures used by the report layer.

The report layer turns transcript files into structured summaries before
writing them into the Excel workbook.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CallSummary:
    """Structured representation of one analyzed call transcript.

    Attributes:
        source_path: Path to the transcript file.
        date: Date extracted from the file name.
        call_type: Incoming or outgoing call label.
        phone: Phone number extracted from the file name or transcript body.
        branch: Branch name if present.
        manager: Manager name if it can be detected.
        work_type: Work category inferred from the transcript.
        result: Overall result of the call.
        comment: Reviewer comment shown in the Excel sheet.
        scores: Checklist scores with 1/0 values.
        total_score: Sum of the checklist scores.
    """

    source_path: Path
    date: str
    call_type: str
    phone: str
    branch: str
    manager: str
    work_type: str
    result: str
    comment: str
    scores: dict[str, int]
    total_score: int
