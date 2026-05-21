# Technical task

Small local tool that transcribes audio calls and writes the result into an Excel report.

## Workflow

`transcribing` -> `analyzing` -> `writing to table`

Audio files are transcribed to `.txt`, each transcript is analyzed into a report row, and the Excel table is updated.

## Run with `uv`

```bash
uv sync
uv run garage-race
```

If you already have transcripts and only want to build the table:

```bash
uv run garage-race --skip-transcript
```

If you only want transcription and do not want to touch the table:

```bash
uv run garage-race --skip-report
```

## Run with plain Python

```
python -m venv venv
source venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python main.py
```

You can also run only one part of the pipeline:

```bash
python main.py --skip-report
python main.py --skip-transcript
```

## CLI arguments

- `--input-dir` - folder with audio files.
- `--output-dir` - folder for transcript `.txt` files.
- `--model` - transcription model name.
- `--language` - optional language code like `uk`, `en`, or `ru`.
- `--overwrite` - rewrite existing transcript files.
- `--beam-size` - beam search size for better quality.
- `--template` - Excel template file to copy and fill.
- `--report-output` - output path for the generated Excel report.
- `--skip-transcript` - skip transcription and only build the report from existing transcripts.
- `--skip-report` - skip Excel generation and only transcribe audio.

## Models

I tested several Whisper variants.

- `base` was faster, but the transcription quality was too weak for this task.
- `large-v3` gives much better transcript quality, so it is the default now.
- `distil-large-v3` is a good compromise if you want better quality than `base` but less weight than the full large model.

## Output

- Transcripts are saved as `.txt` files next to the audio files.
- The Excel report is saved as `src/technical_task_garage_race/data/table/Звіт прослуханих розмов - заповнений.xlsx`.
- The report can be re-run on an already existing workbook and it will append new rows instead of recreating everything.
