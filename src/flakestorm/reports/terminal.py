"""
Terminal Report Generator

Displays test results directly in the terminal using rich formatting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from flakestorm.reports.models import TestResults


class TerminalReporter:
    """
    Displays test results in the terminal using rich formatting.

    Provides colorful, informative output for interactive use.
    """

    def __init__(self, results: TestResults, console: Console | None = None):
        """
        Initialize the reporter.

        Args:
            results: Test results to display
            console: Rich console (default: new console)
        """
        self.results = results
        self.console = console or Console()

    def print_summary(self) -> None:
        """Print a summary of the test results."""
        stats = self.results.statistics

        # Robustness score with color
        score = stats.robustness_score
        if score >= 0.9:
            score_style = "bold green"
            score_emoji = "🎉"
        elif score >= 0.7:
            score_style = "bold yellow"
            score_emoji = "⚠️"
        else:
            score_style = "bold red"
            score_emoji = "❌"

        score_text = Text()
        score_text.append(f"{score_emoji} Robustness Score: ", style="bold")
        score_text.append(f"{score:.1%}", style=score_style)

        # Create summary panel
        summary_lines = [
            score_text,
            "",
            f"Total Mutations: {stats.total_mutations}",
            Text.assemble(
                ("Passed: ", ""),
                (str(stats.passed_mutations), "green"),
                (" | Failed: ", ""),
                (str(stats.failed_mutations), "red"),
            ),
            "",
            f"Avg Latency: {stats.avg_latency_ms:.0f}ms",
            f"P95 Latency: {stats.p95_latency_ms:.0f}ms",
            f"Duration: {self.results.duration:.1f}s",
        ]

        panel_content = "\n".join(str(line) for line in summary_lines)

        self.console.print(
            Panel(
                panel_content,
                title="flakestorm Results",
                border_style="blue",
            )
        )

    def print_type_breakdown(self) -> None:
        """Print breakdown by mutation type."""
        stats = self.results.statistics

        table = Table(title="By Mutation Type", show_header=True)
        table.add_column("Type", style="cyan")
        table.add_column("Passed", justify="right", style="green")
        table.add_column("Failed", justify="right", style="red")
        table.add_column("Pass Rate", justify="right")
        table.add_column("Progress", width=20)

        for type_stat in stats.by_type:
            # Create a simple text-based progress bar
            bar_width = 15
            filled = int(type_stat.pass_rate * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)

            table.add_row(
                type_stat.mutation_type.replace("_", " ").title(),
                str(type_stat.passed),
                str(type_stat.total - type_stat.passed),
                f"{type_stat.pass_rate:.1%}",
                bar,
            )

        self.console.print(table)

    def print_failures(self, limit: int = 10) -> None:
        """
        Print details of failed mutations.

        Args:
            limit: Maximum number of failures to show
        """
        failed = self.results.failed_mutations

        if not failed:
            self.console.print("[green]✓ No failures![/green]")
            return

        self.console.print(
            f"\n[bold red]Failed Mutations ({len(failed)} total):[/bold red]"
        )

        for i, result in enumerate(failed[:limit]):
            self.console.print(f"\n[bold]#{i+1} - {result.mutation.type.value}[/bold]")
            self.console.print(
                f"  [dim]Original:[/dim] {result.original_prompt[:50]}..."
            )
            self.console.print(
                f"  [dim]Mutated:[/dim] {result.mutation.mutated[:50]}..."
            )

            for check in result.failed_checks:
                self.console.print(
                    f"  [red]✗ {check.check_type}:[/red] {check.details}"
                )

        if len(failed) > limit:
            self.console.print(
                f"\n[dim]...and {len(failed) - limit} more failures. "
                "See HTML report for details.[/dim]"
            )

    def print_full_report(self) -> None:
        """Print the complete terminal report."""
        self.console.print()
        self.print_summary()
        self.console.print()
        self.print_type_breakdown()
        self.print_failures()
        self.console.print()
