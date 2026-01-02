"""
flakestorm Reports Module

Provides report generation in multiple formats:
- Interactive HTML reports
- JSON exports
- Terminal output
"""

from flakestorm.reports.html import HTMLReportGenerator
from flakestorm.reports.json_export import JSONReportGenerator
from flakestorm.reports.models import (
    CheckResult,
    MutationResult,
    TestResults,
    TestStatistics,
    TypeStatistics,
)
from flakestorm.reports.terminal import TerminalReporter

__all__ = [
    "TestResults",
    "TestStatistics",
    "MutationResult",
    "CheckResult",
    "TypeStatistics",
    "HTMLReportGenerator",
    "JSONReportGenerator",
    "TerminalReporter",
]
