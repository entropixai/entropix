"""
Open Source Edition Limits

Defines feature limits for the open source (local-only) version.
These limits encourage users to upgrade to Entropix Cloud for:
- Faster parallel execution
- Cloud LLMs (higher quality mutations)
- Advanced features
- Team collaboration
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

if TYPE_CHECKING:
    pass


# =============================================================================
# OPEN SOURCE EDITION LIMITS
# =============================================================================

# Maximum mutations per test run (sequential = slow)
MAX_MUTATIONS_PER_RUN = 50

# Maximum golden prompts
MAX_GOLDEN_PROMPTS = 10

# Execution mode (sequential only - no parallelism)
PARALLEL_EXECUTION_ENABLED = False

# GitHub Actions integration
GITHUB_ACTIONS_ENABLED = False

# Advanced features disabled
ADVANCED_MUTATIONS_ENABLED = False  # Sophisticated prompt injections
ADVANCED_SAFETY_CHECKS_ENABLED = False  # NER, ML-based detection, factuality
TEST_HISTORY_ENABLED = False  # Dashboard, history tracking
TEAM_FEATURES_ENABLED = False  # Sharing, collaboration

# Cloud features disabled
CLOUD_LLM_ENABLED = False


# =============================================================================
# ALLOWED MUTATION TYPES (5 types for open source)
# =============================================================================

ALLOWED_MUTATION_TYPES = [
    "paraphrase",  # Semantic rewrites
    "noise",  # Typos, spelling errors
    "tone_shift",  # Tone changes
    "prompt_injection",  # Basic adversarial
    "custom",  # User-defined templates
]


# =============================================================================
# UPGRADE MESSAGING
# =============================================================================

CLOUD_URL = "https://entropix.cloud"
UPGRADE_CTA = f"⚡ Upgrade to Entropix Cloud for 20x faster execution → {CLOUD_URL}"


@dataclass
class LimitViolation:
    """Represents a limit that was exceeded."""

    limit_name: str
    current_value: int
    max_value: int
    message: str


def check_mutation_limit(
    requested_count: int, num_prompts: int
) -> LimitViolation | None:
    """
    Check if the requested mutation count exceeds limits.

    Args:
        requested_count: Requested mutations per prompt
        num_prompts: Number of golden prompts

    Returns:
        LimitViolation if exceeded, None otherwise
    """
    total = requested_count * num_prompts
    if total > MAX_MUTATIONS_PER_RUN:
        return LimitViolation(
            limit_name="mutations_per_run",
            current_value=total,
            max_value=MAX_MUTATIONS_PER_RUN,
            message=(
                f"Open Source limit: {MAX_MUTATIONS_PER_RUN} mutations per run. "
                f"You requested {total} ({requested_count} × {num_prompts} prompts).\n"
                f"Upgrade to Cloud for unlimited mutations."
            ),
        )
    return None


def check_golden_prompt_limit(num_prompts: int) -> LimitViolation | None:
    """Check if golden prompt count exceeds limits."""
    if num_prompts > MAX_GOLDEN_PROMPTS:
        return LimitViolation(
            limit_name="golden_prompts",
            current_value=num_prompts,
            max_value=MAX_GOLDEN_PROMPTS,
            message=(
                f"Open Source limit: {MAX_GOLDEN_PROMPTS} golden prompts. "
                f"You have {num_prompts}.\n"
                f"Upgrade to Cloud for unlimited prompts."
            ),
        )
    return None


def enforce_mutation_limit(requested_count: int, num_prompts: int) -> int:
    """
    Enforce mutation limit by capping the count.

    Returns the actual count to use (may be reduced).
    """
    max_per_prompt = MAX_MUTATIONS_PER_RUN // max(num_prompts, 1)
    return min(requested_count, max(max_per_prompt, 1))


def print_upgrade_banner(console: Console, reason: str = "faster execution") -> None:
    """Print an upgrade banner to the console."""
    banner = Panel(
        Text.from_markup(
            f"[bold yellow]⚡ Want {reason}?[/bold yellow]\n\n"
            f"[white]Entropix Cloud offers:[/white]\n"
            f"  • [green]20x faster[/green] parallel execution\n"
            f"  • [green]Cloud LLMs[/green] for higher quality mutations\n"
            f"  • [green]Advanced safety checks[/green] (NER, ML-detection)\n"
            f"  • [green]Test history[/green] and analytics dashboard\n"
            f"  • [green]Team features[/green] for collaboration\n\n"
            f"[bold cyan]→ {CLOUD_URL}[/bold cyan]"
        ),
        title="[bold blue]Upgrade to Entropix Cloud[/bold blue]",
        border_style="blue",
        padding=(1, 2),
    )
    console.print(banner)


def print_limit_warning(console: Console, violation: LimitViolation) -> None:
    """Print a limit warning to the console."""
    warning = Panel(
        Text.from_markup(
            f"[bold yellow]⚠️ Limit Reached[/bold yellow]\n\n"
            f"[white]{violation.message}[/white]\n\n"
            f"[bold cyan]→ {CLOUD_URL}[/bold cyan]"
        ),
        title="[bold yellow]Open Source Edition[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    )
    console.print(warning)


def print_sequential_notice(console: Console) -> None:
    """Print a notice about sequential execution."""
    console.print(
        "\n[dim]ℹ️  Running in sequential mode (Open Source). "
        f"Upgrade to Cloud for parallel execution: {CLOUD_URL}[/dim]\n"
    )


def print_completion_upsell(console: Console, duration_seconds: float) -> None:
    """Print upsell after test completion based on duration."""
    if duration_seconds > 60:  # More than 1 minute
        estimated_cloud_time = (
            duration_seconds / 20
        )  # ~20x faster with parallel + cloud
        console.print(
            f"\n[dim]⏱️  Test took {duration_seconds:.1f}s. "
            f"With Entropix Cloud, this would take ~{estimated_cloud_time:.1f}s[/dim]"
        )
        console.print(f"[dim cyan]→ {CLOUD_URL}[/dim cyan]\n")


def get_feature_comparison() -> str:
    """Get a feature comparison table for documentation."""
    return """
## Feature Comparison

| Feature | Open Source | Cloud Pro | Cloud Team |
|---------|:-----------:|:---------:|:----------:|
| Mutation Types | 5 basic | All types | All types |
| Mutations/Run | 50 | Unlimited | Unlimited |
| Execution | Sequential | Parallel (20x) | Parallel (20x) |
| LLM | Local only | Cloud + Local | Cloud + Local |
| PII Detection | Basic | Advanced (NER) | Advanced (NER) |
| Prompt Injection | Basic | ML-powered | ML-powered |
| Factuality Check | ❌ | ✅ | ✅ |
| Test History | ❌ | ✅ | ✅ |
| Dashboard | ❌ | ✅ | ✅ |
| GitHub Actions | ❌ | ✅ | ✅ |
| Team Sharing | ❌ | ❌ | ✅ |
| SSO/SAML | ❌ | ❌ | ✅ |
| Price | Free | $49/mo | $299/mo |

**Why is Open Source slower?**
- Sequential execution: Tests run one at a time
- Local LLM: Slower than cloud GPU inference
- No caching: Each run starts fresh

**Cloud advantages:**
- 20x faster with parallel execution
- Higher quality mutations with cloud LLMs
- Historical comparison across runs
"""
