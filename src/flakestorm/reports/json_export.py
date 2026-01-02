"""
JSON Report Generator

Exports test results to JSON format for programmatic consumption
and integration with other tools.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flakestorm.reports.models import TestResults


class JSONReportGenerator:
    """
    Generates JSON reports from test results.

    Creates structured JSON output suitable for:
    - CI/CD pipeline consumption
    - Data analysis tools
    - Dashboard integrations
    """

    def __init__(self, results: TestResults):
        """
        Initialize the generator.

        Args:
            results: Test results to generate report from
        """
        self.results = results

    def generate(self, pretty: bool = True) -> str:
        """
        Generate the JSON report.

        Args:
            pretty: Whether to format with indentation

        Returns:
            JSON string
        """
        data = self.results.to_dict()

        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)

    def generate_summary(self) -> dict[str, Any]:
        """
        Generate a summary-only report (no mutation details).

        Useful for quick status checks in CI/CD.
        """
        stats = self.results.statistics

        return {
            "version": "1.0",
            "started_at": self.results.started_at.isoformat(),
            "completed_at": self.results.completed_at.isoformat(),
            "duration_seconds": self.results.duration,
            "robustness_score": stats.robustness_score,
            "pass_rate": stats.pass_rate,
            "total_mutations": stats.total_mutations,
            "passed_mutations": stats.passed_mutations,
            "failed_mutations": stats.failed_mutations,
            "avg_latency_ms": stats.avg_latency_ms,
            "p95_latency_ms": stats.p95_latency_ms,
            "by_type": {
                t.mutation_type: {
                    "total": t.total,
                    "passed": t.passed,
                    "pass_rate": t.pass_rate,
                }
                for t in stats.by_type
            },
        }

    def save(self, path: str | Path | None = None, summary_only: bool = False) -> Path:
        """
        Save the JSON report to a file.

        Args:
            path: Output path (default: auto-generated in reports dir)
            summary_only: Only include summary, no mutation details

        Returns:
            Path to the saved file
        """
        if path is None:
            output_dir = Path(self.results.config.output.path)
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            suffix = "-summary" if summary_only else ""
            filename = f"flakestorm-{timestamp}{suffix}.json"
            path = output_dir / filename
        else:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

        if summary_only:
            data = self.generate_summary()
            content = json.dumps(data, indent=2, default=str)
        else:
            content = self.generate()

        path.write_text(content, encoding="utf-8")

        return path
