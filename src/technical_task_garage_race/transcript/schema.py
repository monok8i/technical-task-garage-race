"""Data structures used by transcription.

This module contains the transcript result object and the segment protocol
returned by Faster-Whisper.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class TranscriptResult:
    """Result of transcribing one audio file.

    Attributes:
        audio_path: Path to the original audio file.
        transcript_path: Path to the saved transcript file.
        text: Full transcript content.
    """

    audio_path: Path
    transcript_path: Path
    text: str


class TranscriptSegment(Protocol):
    """Protocol for a single transcript segment emitted by the model."""

    text: str
