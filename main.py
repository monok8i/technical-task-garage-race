"""Local Python entrypoint for the Garage Race project.

This wrapper allows running the project with plain ``python main.py``
without using the installed console script.
"""

from technical_task_garage_race.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
