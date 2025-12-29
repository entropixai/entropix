"""
GitHub Actions Integration

⚠️ CLOUD FEATURE: GitHub Actions integration is available in flakestorm Cloud.
The Open Source edition provides documentation only.

Upgrade to flakestorm Cloud for:
- One-click CI/CD integration
- Block PRs based on reliability score
- Automated test history tracking
- Team notifications

→ https://flakestorm.cloud
"""

from __future__ import annotations

from pathlib import Path

from flakestorm.core.limits import CLOUD_URL, GITHUB_ACTIONS_ENABLED


class GitHubActionsDisabledError(Exception):
    """Raised when trying to use GitHub Actions in Open Source edition."""

    def __init__(self):
        super().__init__(
            "GitHub Actions integration is available in flakestorm Cloud.\n"
            f"Upgrade at: {CLOUD_URL}"
        )


# GitHub Action YAML template (for reference/documentation)
ACTION_YAML = """# ⚠️ CLOUD FEATURE: This requires flakestorm Cloud
# Upgrade at: https://flakestorm.cloud

name: 'flakestorm Agent Test'
description: 'Run chaos testing on AI agents to verify reliability'
author: 'flakestorm'

branding:
  icon: 'shield'
  color: 'purple'

inputs:
  config:
    description: 'Path to flakestorm.yaml configuration file'
    required: false
    default: 'flakestorm.yaml'
  min_score:
    description: 'Minimum robustness score to pass (0.0-1.0)'
    required: false
    default: '0.9'
  api_key:
    description: 'flakestorm Cloud API key (required)'
    required: true

outputs:
  score:
    description: 'The robustness score achieved'
  passed:
    description: 'Whether the test passed (true/false)'
  report_url:
    description: 'URL to the full report on flakestorm Cloud'

runs:
  using: 'composite'
  steps:
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install flakestorm
      shell: bash
      run: pip install flakestorm

    - name: Run Cloud Tests
      shell: bash
      env:
        FLAKESTORM_API_KEY: ${{ inputs.api_key }}
      run: |
        flakestorm cloud run \\
          --config ${{ inputs.config }} \\
          --min-score ${{ inputs.min_score }} \\
          --ci
"""


# Example workflow YAML
WORKFLOW_EXAMPLE = """# flakestorm Cloud CI/CD Integration
# ⚠️ Requires flakestorm Cloud subscription
# Get started: https://flakestorm.cloud

name: Agent Reliability Check

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  reliability-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run flakestorm Cloud Tests
        uses: flakestorm/flakestorm-action@v1
        with:
          config: flakestorm.yaml
          min_score: '0.9'
          api_key: ${{ secrets.FLAKESTORM_API_KEY }}
"""


class GitHubActionsIntegration:
    """
    Helper class for GitHub Actions integration.

    ⚠️ NOTE: Full CI/CD integration requires flakestorm Cloud.

    The Open Source edition provides:
    - Documentation and examples
    - Local testing only

    flakestorm Cloud provides:
    - One-click GitHub Actions setup
    - Block PRs based on reliability score
    - Test history and comparison
    - Slack/Discord notifications

    Upgrade at: https://flakestorm.cloud
    """

    @staticmethod
    def _check_enabled() -> None:
        """Check if GitHub Actions is enabled."""
        if not GITHUB_ACTIONS_ENABLED:
            raise GitHubActionsDisabledError()

    @staticmethod
    def generate_action_yaml() -> str:
        """
        Generate the GitHub Action definition YAML.

        Note: This returns documentation only in Open Source edition.
        Full integration requires flakestorm Cloud.

        Returns:
            Action YAML content
        """
        return ACTION_YAML.strip()

    @staticmethod
    def generate_workflow_example() -> str:
        """
        Generate an example workflow that uses flakestorm.

        Note: Requires flakestorm Cloud for full functionality.

        Returns:
            Workflow YAML content
        """
        return WORKFLOW_EXAMPLE.strip()

    @staticmethod
    def save_action(output_dir: Path) -> Path:
        """
        Save the GitHub Action files to a directory.

        ⚠️ Cloud Feature: This creates documentation only.
        For working CI/CD, upgrade to flakestorm Cloud.

        Args:
            output_dir: Directory to save action files

        Returns:
            Path to the action.yml file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        action_path = output_dir / "action.yml"
        action_path.write_text(ACTION_YAML.strip(), encoding="utf-8")

        # Also create a README explaining Cloud requirement
        readme_path = output_dir / "README.md"
        readme_path.write_text(
            f"""# flakestorm GitHub Action

⚠️ **Cloud Feature**: Full CI/CD integration requires flakestorm Cloud.

## What You Get with Cloud

- ✅ One-click GitHub Actions setup
- ✅ Block PRs based on reliability score
- ✅ Test history and comparison across runs
- ✅ Slack/Discord notifications
- ✅ 20x faster parallel execution

## Upgrade

Get started at: {CLOUD_URL}

## Local Testing

For local-only testing, use the Open Source CLI:

```bash
flakestorm run --config flakestorm.yaml
```

Note: Local runs are sequential and may be slow for large test suites.
""",
            encoding="utf-8",
        )

        return action_path

    @staticmethod
    def save_workflow_example(output_path: Path) -> Path:
        """
        Save an example workflow file.

        Args:
            output_path: Path to save the workflow file

        Returns:
            Path to the saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(WORKFLOW_EXAMPLE.strip(), encoding="utf-8")

        return output_path

    @staticmethod
    def setup_ci(
        repo_path: Path,
        config_path: str = "flakestorm.yaml",
        min_score: float = 0.9,
    ) -> None:
        """
        Set up CI/CD integration for a repository.

        ⚠️ Cloud Feature: Requires flakestorm Cloud subscription.

        Raises:
            GitHubActionsDisabledError: Always in Open Source edition
        """
        GitHubActionsIntegration._check_enabled()
        # Cloud implementation would go here
