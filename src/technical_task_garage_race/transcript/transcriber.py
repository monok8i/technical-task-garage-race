"""Audio transcription helpers.

The functions in this module turn audio files into transcript text files
using a Faster-Whisper model.
"""

from pathlib import Path

from technical_task_garage_race.transcript.constants import SUPPORTED_AUDIO_EXTENSIONS
from technical_task_garage_race.transcript.model import (
    WhisperModelLike,
    load_whisper_model,
)
from technical_task_garage_race.transcript.schema import TranscriptResult


def iter_audio_files(directory: Path) -> list[Path]:
    """Collect supported audio files from a directory.

    Args:
        directory: Folder to scan for audio files.

    Returns:
        list[Path]: Sorted list of supported audio file paths.
    """
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
    )


def transcribe_audio_file(
    audio_path: Path,
    *,
    model: "WhisperModelLike",
    language: str | None = None,
    beam_size: int = 5,
    transcript_path: Path | None = None,
) -> TranscriptResult:
    """Transcribe one audio file and save the transcript next to it.

    Args:
        audio_path: Path to the audio file.
        model: Loaded Faster-Whisper model instance.
        language: Optional language code used by the model.
        beam_size: Beam search size for decoding quality.
        transcript_path: Optional explicit output path for the transcript.

    Returns:
        TranscriptResult: Path and text of the saved transcript.
    """
    output_path = transcript_path or audio_path.with_suffix(".txt")

    segments, _info = model.transcribe(
        str(audio_path),
        language=language,
        vad_filter=True,
        beam_size=beam_size,
    )

    text_parts: list[str] = []
    for segment in segments:
        segment_text = segment.text.strip()
        if segment_text:
            text_parts.append(segment_text)

    text = "\n".join(text_parts).strip()
    output_path.write_text(text + ("\n" if text else ""), encoding="utf-8")

    return TranscriptResult(
        audio_path=audio_path, transcript_path=output_path, text=text
    )


def transcribe_directory(
    input_dir: Path,
    *,
    model_name: str = "base",
    language: str | None = None,
    output_dir: Path | None = None,
    overwrite: bool = False,
    beam_size: int = 5,
) -> list[TranscriptResult]:
    """Transcribe all supported audio files inside a directory.

    Args:
        input_dir: Folder containing audio files.
        model_name: Whisper model name or repository ID.
        language: Optional language code used by the model.
        output_dir: Optional directory where transcript files should be saved.
        overwrite: Whether to rewrite existing transcript files.
        beam_size: Beam search size for decoding quality.

    Returns:
        list[TranscriptResult]: Transcription results for the processed files.

    Raises:
        FileNotFoundError: If the input directory does not exist.
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    audio_files = iter_audio_files(input_dir)
    if not audio_files:
        return []

    model = load_whisper_model(model_name)
    results: list[TranscriptResult] = []

    for audio_path in audio_files:
        transcript_path = (
            (output_dir / f"{audio_path.stem}.txt")
            if output_dir
            else audio_path.with_suffix(".txt")
        )
        if transcript_path.exists() and not overwrite:
            results.append(
                TranscriptResult(
                    audio_path=audio_path,
                    transcript_path=transcript_path,
                    text=transcript_path.read_text(encoding="utf-8").strip(),
                )
            )
            continue

        transcript_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Transcribing: {audio_path.name} -> {transcript_path.name}")
        result = transcribe_audio_file(
            audio_path,
            model=model,
            language=language,
            beam_size=beam_size,
            transcript_path=transcript_path,
        )
        results.append(result)

    return results
