"""Command-line interface for the Garage Race technical task.

The CLI orchestrates transcription, transcript analysis, and Excel report
generation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from technical_task_garage_race.report import build_report
from technical_task_garage_race.transcript import transcribe_directory


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser.

    Returns:
        argparse.ArgumentParser: Parser configured with all supported CLI
        options.
    """
    parser = argparse.ArgumentParser(description="Transcribe audio files in a folder.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("src/technical_task_garage_race/data/calls"),
        help="Folder with audio files to transcribe.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("src/technical_task_garage_race/data/transcripts"),
        help="Folder for transcript files.",
    )
    parser.add_argument(
        "--model",
        default="large-v3",
        help="Whisper model name, for example tiny, base, small, medium, large-v3 or distil-large-v3.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Optional language code, for example uk, en, ru.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Rewrite transcript files if they already exist.",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam search size for better transcription quality.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(
            "src/technical_task_garage_race/data/table/Звіт прослуханих розмов.xlsx"
        ),
        help="Excel template to copy and fill.",
    )
    parser.add_argument(
        "--report-output",
        type=Path,
        default=Path(
            "src/technical_task_garage_race/data/table/Звіт прослуханих розмов - заповнений.xlsx"
        ),
        help="Path for the generated Excel report.",
    )
    parser.add_argument(
        "--skip-transcript",
        action="store_true",
        help="Skip audio transcription and only generate the report from existing transcripts.",
    )
    parser.add_argument(
        "--skip-report",
        action="store_true",
        help="Only transcribe audio and skip Excel generation.",
    )
    return parser


def main() -> int:
    """Execute the CLI workflow.

    Returns:
        int: Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args()

    if args.skip_transcript:
        transcript_count = len(list(args.output_dir.glob("*.txt")))
        print(
            f"Skipping transcription. Found {transcript_count} transcript file(s) in {args.output_dir}."
        )
    else:
        results = transcribe_directory(
            args.input_dir,
            model_name=args.model,
            language=args.language,
            output_dir=args.output_dir,
            overwrite=args.overwrite,
            beam_size=args.beam_size,
        )

        if not results:
            print(f"No audio files found in {args.input_dir}")
            return 0

        for result in results:
            print(
                f"Transcribed: {result.audio_path.name} -> {result.transcript_path.name}"
            )

    if not args.skip_report:
        summaries = build_report(args.template, args.output_dir, args.report_output)
        print(f"Report generated: {args.report_output}")
        print(f"Rows written: {len(summaries)}")

    print("Done.")
    return 0
