"""
HTML Report Generator

Generates interactive HTML reports with:
- Robustness score visualization
- Pass/fail matrix grid
- Drill-down into failed mutations
- Latency charts
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Template

if TYPE_CHECKING:
    from flakestorm.reports.models import TestResults


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>flakestorm Report - {{ report_date }}</title>
    <style>
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a24;
            --text-primary: #e8e8ed;
            --text-secondary: #8b8b9e;
            --accent: #6366f1;
            --accent-light: #818cf8;
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
            --border: #2a2a3a;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent), var(--accent-light));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.25rem;
        }

        .logo-text {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .report-meta {
            text-align: right;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }

        .score-section {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .score-card {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .score-ring {
            position: relative;
            width: 180px;
            height: 180px;
        }

        .score-ring svg {
            transform: rotate(-90deg);
        }

        .score-ring circle {
            fill: none;
            stroke-width: 12;
        }

        .score-ring .bg {
            stroke: var(--border);
        }

        .score-ring .progress {
            stroke: var(--accent);
            stroke-linecap: round;
            transition: stroke-dashoffset 1s ease-out;
        }

        .score-value {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2.5rem;
            font-weight: 700;
        }

        .score-label {
            margin-top: 1rem;
            font-size: 1.125rem;
            color: var(--text-secondary);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }

        .stat-card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 1.25rem;
        }

        .stat-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .stat-value.success { color: var(--success); }
        .stat-value.danger { color: var(--danger); }

        .section {
            margin-bottom: 2rem;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .matrix-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }

        .matrix-cell {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 1rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .matrix-cell:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }

        .matrix-cell.passed {
            border-left: 4px solid var(--success);
        }

        .matrix-cell.failed {
            border-left: 4px solid var(--danger);
        }

        .mutation-type {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }

        .mutation-text {
            font-size: 0.875rem;
            line-height: 1.4;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }

        .mutation-meta {
            display: flex;
            justify-content: space-between;
            margin-top: 0.75rem;
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .type-breakdown {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }

        .type-card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 1.25rem;
        }

        .type-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .type-name {
            font-weight: 600;
            text-transform: capitalize;
        }

        .type-rate {
            font-size: 1.125rem;
            font-weight: 600;
        }

        .progress-bar {
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent), var(--accent-light));
            border-radius: 4px;
            transition: width 0.5s ease-out;
        }

        .modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: var(--bg-secondary);
            border-radius: 16px;
            max-width: 800px;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto;
            padding: 2rem;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .modal-close {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.5rem;
            cursor: pointer;
        }

        .detail-section {
            margin-bottom: 1.5rem;
        }

        .detail-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }

        .detail-content {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 1rem;
            font-family: 'SF Mono', 'Fira Code', monospace;
            font-size: 0.875rem;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .check-list {
            list-style: none;
        }

        .check-item {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.75rem;
            background: var(--bg-card);
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        .check-icon {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            font-size: 0.75rem;
        }

        .check-icon.passed {
            background: var(--success);
            color: white;
        }

        .check-icon.failed {
            background: var(--danger);
            color: white;
        }

        .check-details {
            flex: 1;
        }

        .check-type {
            font-weight: 600;
            text-transform: capitalize;
        }

        .check-message {
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        @media (max-width: 768px) {
            .score-section {
                grid-template-columns: 1fr;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <div class="logo-icon">E</div>
                <span class="logo-text">flakestorm</span>
            </div>
            <div class="report-meta">
                <div>{{ report_date }}</div>
                <div>Duration: {{ duration }}s</div>
            </div>
        </header>

        <div class="score-section">
            <div class="score-card">
                <div class="score-ring">
                    <svg width="180" height="180">
                        <circle class="bg" cx="90" cy="90" r="78"></circle>
                        <circle class="progress" cx="90" cy="90" r="78"
                            stroke-dasharray="{{ circumference }}"
                            stroke-dashoffset="{{ score_offset }}">
                        </circle>
                    </svg>
                    <div class="score-value">{{ score_percent }}%</div>
                </div>
                <div class="score-label">Robustness Score</div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Mutations</div>
                    <div class="stat-value">{{ total_mutations }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Passed</div>
                    <div class="stat-value success">{{ passed_mutations }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Failed</div>
                    <div class="stat-value danger">{{ failed_mutations }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Avg Latency</div>
                    <div class="stat-value">{{ avg_latency }}ms</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">📊 By Mutation Type</h2>
            <div class="type-breakdown">
                {% for type_stat in type_stats %}
                <div class="type-card">
                    <div class="type-header">
                        <span class="type-name">{{ type_stat.mutation_type }}</span>
                        <span class="type-rate">{{ type_stat.pass_rate_percent }}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {{ type_stat.pass_rate_percent }}%"></div>
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-secondary);">
                        {{ type_stat.passed }}/{{ type_stat.total }} passed
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">🔬 Mutation Results</h2>
            <div class="matrix-grid">
                {% for result in mutations %}
                <div class="matrix-cell {{ 'passed' if result.passed else 'failed' }}"
                     onclick="showDetail({{ loop.index0 }})">
                    <div class="mutation-type">{{ result.mutation.type }}</div>
                    <div class="mutation-text">{{ result.mutation.mutated[:100] }}...</div>
                    <div class="mutation-meta">
                        <span>{{ result.latency_ms|round(0)|int }}ms</span>
                        <span>{{ '✓' if result.passed else '✗' }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <div class="modal" id="detail-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Mutation Details</h3>
                <button class="modal-close" onclick="closeModal()">×</button>
            </div>
            <div id="modal-body"></div>
        </div>
    </div>

    <script>
        const mutations = {{ mutations_json|safe }};

        function showDetail(index) {
            const m = mutations[index];
            const modal = document.getElementById('detail-modal');
            const body = document.getElementById('modal-body');

            body.innerHTML = `
                <div class="detail-section">
                    <div class="detail-label">Original Prompt</div>
                    <div class="detail-content">${m.original_prompt}</div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">Mutated (${m.mutation.type})</div>
                    <div class="detail-content">${m.mutation.mutated}</div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">Agent Response</div>
                    <div class="detail-content">${m.response || '(empty)'}</div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">Invariant Checks</div>
                    <ul class="check-list">
                        ${m.checks.map(c => `
                            <li class="check-item">
                                <div class="check-icon ${c.passed ? 'passed' : 'failed'}">
                                    ${c.passed ? '✓' : '✗'}
                                </div>
                                <div class="check-details">
                                    <div class="check-type">${c.check_type}</div>
                                    <div class="check-message">${c.details}</div>
                                </div>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;

            modal.classList.add('active');
        }

        function closeModal() {
            document.getElementById('detail-modal').classList.remove('active');
        }

        document.getElementById('detail-modal').addEventListener('click', (e) => {
            if (e.target.id === 'detail-modal') closeModal();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });
    </script>
</body>
</html>
"""


class HTMLReportGenerator:
    """
    Generates interactive HTML reports from test results.

    Creates a single-file HTML report with embedded CSS and JavaScript
    for easy sharing and viewing.
    """

    def __init__(self, results: TestResults):
        """
        Initialize the generator.

        Args:
            results: Test results to generate report from
        """
        self.results = results
        self.template = Template(HTML_TEMPLATE)

    def generate(self) -> str:
        """
        Generate the HTML report.

        Returns:
            Complete HTML document as a string
        """
        stats = self.results.statistics

        # Calculate score ring values
        circumference = 2 * 3.14159 * 78
        score_offset = circumference * (1 - stats.robustness_score)

        # Prepare type stats
        type_stats = [
            {
                "mutation_type": t.mutation_type.replace("_", " "),
                "total": t.total,
                "passed": t.passed,
                "pass_rate_percent": round(t.pass_rate * 100, 1),
            }
            for t in stats.by_type
        ]

        # Prepare mutations data
        mutations_data = [m.to_dict() for m in self.results.mutations]

        return self.template.render(
            report_date=self.results.started_at.strftime("%Y-%m-%d %H:%M:%S"),
            duration=round(self.results.duration, 1),
            circumference=circumference,
            score_offset=score_offset,
            score_percent=round(stats.robustness_score * 100, 1),
            total_mutations=stats.total_mutations,
            passed_mutations=stats.passed_mutations,
            failed_mutations=stats.failed_mutations,
            avg_latency=round(stats.avg_latency_ms),
            type_stats=type_stats,
            mutations=self.results.mutations,
            mutations_json=json.dumps(mutations_data),
        )

    def save(self, path: str | Path | None = None) -> Path:
        """
        Save the HTML report to a file.

        Args:
            path: Output path (default: auto-generated in reports dir)

        Returns:
            Path to the saved file
        """
        if path is None:
            output_dir = Path(self.results.config.output.path)
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"flakestorm-{timestamp}.html"
            path = output_dir / filename
        else:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

        html = self.generate()
        path.write_text(html, encoding="utf-8")

        return path
