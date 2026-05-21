"""Excel reporting helpers.

The subpackage exposes the function that converts transcript files into
rows in the workbook template.
"""

from .reporter import build_report

__all__ = ("build_report",)
