"""Model loading and type definitions for transcription.

This module resolves Faster-Whisper model names, downloads the model from
the Hugging Face Hub, and exposes a small protocol for the parts of the
model used by the project.
"""

from collections.abc import Iterable
from typing import Any, Protocol, TYPE_CHECKING, cast

import huggingface_hub
from faster_whisper import WhisperModel  # type: ignore[import-not-found]
from faster_whisper.utils import _MODELS  # type: ignore[import-not-found]
from tqdm.auto import tqdm

if TYPE_CHECKING:
    from technical_task_garage_race.transcript.schema import TranscriptSegment


class WhisperModelLike(Protocol):
    """Protocol describing the model interface used by the project."""

    def transcribe(
        self,
        audio: str,
        *,
        language: str | None = None,
        vad_filter: bool = False,
        beam_size: int = 5,
    ) -> tuple[Iterable["TranscriptSegment"], Any]:
        """Transcribe audio and return a segment generator plus info object."""
        ...


def _resolve_repo_id(size_or_id: str) -> str:
    """Resolve a friendly model name to a Hugging Face repository ID.

    Args:
        size_or_id: Model name like ``base`` or a full repository ID.

    Returns:
        str: Hugging Face repository ID.

    Raises:
        ValueError: If the model name is not recognized.
    """
    if "/" in size_or_id:
        return size_or_id

    repo_id = _MODELS.get(size_or_id)
    if repo_id is None:
        raise ValueError(
            f"Invalid model size '{size_or_id}', expected one of: {', '.join(_MODELS.keys())}"
        )

    return repo_id


def load_whisper_model(model_name: str = "base") -> WhisperModelLike:
    """Download and initialize the Whisper model.

    Args:
        model_name: Friendly Whisper model name or full repository ID.

    Returns:
        WhisperModelLike: Loaded Faster-Whisper model wrapper.
    """
    repo_id = _resolve_repo_id(model_name)
    model_path = huggingface_hub.snapshot_download(  # type: ignore[attr-defined]
        repo_id,
        allow_patterns=[
            "config.json",
            "preprocessor_config.json",
            "model.bin",
            "tokenizer.json",
            "vocabulary.*",
        ],
        tqdm_class=tqdm,
    )

    return cast(
        WhisperModelLike,
        WhisperModel(model_path, device="cpu", compute_type="int8"),
    )
