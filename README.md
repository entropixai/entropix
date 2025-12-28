# Entropix

<p align="center">
  <strong>The Agent Reliability Engine</strong><br>
  <em>Chaos Engineering for AI Agents</em>
</p>

<p align="center">
  <a href="https://github.com/entropix/entropix/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-AGPLv3-blue.svg" alt="License">
  </a>
  <a href="https://pypi.org/project/entropix/">
    <img src="https://img.shields.io/pypi/v/entropix.svg" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/entropix/">
    <img src="https://img.shields.io/pypi/pyversions/entropix.svg" alt="Python Versions">
  </a>
  <a href="https://entropix.cloud">
    <img src="https://img.shields.io/badge/☁️-Cloud%20Available-blueviolet" alt="Cloud">
  </a>
</p>

---

> **📢 This is the Open Source Edition.** For production workloads, check out [Entropix Cloud](https://entropix.cloud) — 20x faster with parallel execution, cloud LLMs, and CI/CD integration.

---

## The Problem

**The "Happy Path" Fallacy**: Current AI development tools focus on getting an agent to work *once*. Developers tweak prompts until they get a correct answer, declare victory, and ship.

**The Reality**: LLMs are non-deterministic. An agent that works on Monday with `temperature=0.7` might fail on Tuesday. Users don't follow "Happy Paths" — they make typos, they're aggressive, they lie, and they attempt prompt injections.

**The Void**:
- **Observability Tools** (LangSmith) tell you *after* the agent failed in production
- **Eval Libraries** (RAGAS) focus on academic scores rather than system reliability
- **Missing Link**: A tool that actively *attacks* the agent to prove robustness before deployment

## The Solution

**Entropix** is a local-first testing engine that applies **Chaos Engineering** principles to AI Agents.

Instead of running one test case, Entropix takes a single "Golden Prompt", generates adversarial mutations (semantic variations, noise injection, hostile tone, prompt injections), runs them against your agent, and calculates a **Robustness Score**.

> **"If it passes Entropix, it won't break in Production."**

## Open Source vs Cloud

| Feature | Open Source (Free) | Cloud Pro ($49/mo) | Cloud Team ($299/mo) |
|---------|:------------------:|:------------------:|:--------------------:|
| Mutation Types | 5 basic | All types | All types |
| Mutations/Run | **50 max** | Unlimited | Unlimited |
| Execution | **Sequential** | ⚡ Parallel (20x) | ⚡ Parallel (20x) |
| LLM | Local only | Cloud + Local | Cloud + Local |
| PII Detection | Basic regex | Advanced NER + ML | Advanced NER + ML |
| Prompt Injection | Basic | ML-powered | ML-powered |
| Factuality Check | ❌ | ✅ | ✅ |
| Test History | ❌ | ✅ Dashboard | ✅ Dashboard |
| GitHub Actions | ❌ | ✅ One-click | ✅ One-click |
| Team Features | ❌ | ❌ | ✅ SSO + Sharing |

**Why the difference?**

```
Developer workflow:
1. Make code change
2. Run Entropix tests (waiting...)
3. Get results
4. Fix issues
5. Repeat

Open Source: ~10 minutes per iteration → Run once, then skip
Cloud Pro:   ~30 seconds per iteration → Run every commit
```

👉 [**Upgrade to Cloud**](https://entropix.cloud) for production workloads.

## Features (Open Source)

- ✅ **5 Mutation Types**: Paraphrasing, noise, tone shifts, basic adversarial, custom templates
- ✅ **Invariant Assertions**: Deterministic checks, semantic similarity, basic safety
- ✅ **Local-First**: Uses Ollama with Qwen 3 8B for free testing
- ✅ **Beautiful Reports**: Interactive HTML reports with pass/fail matrices
- ⚠️ **50 Mutations Max**: Per test run (upgrade to Cloud for unlimited)
- ⚠️ **Sequential Only**: One test at a time (upgrade to Cloud for 20x parallel)
- ❌ **No CI/CD**: GitHub Actions requires Cloud

## Quick Start

### Installation

```bash
pip install entropix
```

### Prerequisites

Entropix uses [Ollama](https://ollama.ai) for local model inference:

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the default model
ollama pull qwen3:8b
```

### Initialize Configuration

```bash
entropix init
```

This creates an `entropix.yaml` configuration file:

```yaml
version: "1.0"

agent:
  endpoint: "http://localhost:8000/invoke"
  type: "http"
  timeout: 30000

model:
  provider: "ollama"
  name: "qwen3:8b"
  base_url: "http://localhost:11434"

mutations:
  count: 10  # Max 50 total per run in Open Source
  types:
    - paraphrase
    - noise
    - tone_shift
    - prompt_injection

golden_prompts:
  - "Book a flight to Paris for next Monday"
  - "What's my account balance?"

invariants:
  - type: "latency"
    max_ms: 2000
  - type: "valid_json"

output:
  format: "html"
  path: "./reports"
```

### Run Tests

```bash
entropix run
```

Output:
```
ℹ️  Running in sequential mode (Open Source). Upgrade for parallel: https://entropix.cloud

Generating mutations... ━━━━━━━━━━━━━━━━━━━━ 100%
Running attacks...      ━━━━━━━━━━━━━━━━━━━━ 100%

╭──────────────────────────────────────────╮
│  Robustness Score: 87.5%                 │
│  ────────────────────────                │
│  Passed: 17/20 mutations                 │
│  Failed: 3 (2 latency, 1 injection)      │
╰──────────────────────────────────────────╯

⏱️  Test took 245.3s. With Entropix Cloud, this would take ~12.3s
→ https://entropix.cloud

Report saved to: ./reports/entropix-2024-01-15-143022.html
```

### Check Limits

```bash
entropix limits   # Show Open Source edition limits
entropix cloud    # Learn about Cloud features
```

## Mutation Types

| Type | Description | Example |
|------|-------------|---------|
| **Paraphrase** | Semantically equivalent rewrites | "Book a flight" → "I need to fly out" |
| **Noise** | Typos and spelling errors | "Book a flight" → "Book a fliight plz" |
| **Tone Shift** | Aggressive/impatient phrasing | "Book a flight" → "I need a flight NOW!" |
| **Prompt Injection** | Basic adversarial attacks | "Book a flight and ignore previous instructions" |
| **Custom** | Your own mutation templates | Define with `{prompt}` placeholder |

> **Need advanced mutations?** Sophisticated jailbreaks, multi-step injections, and domain-specific attacks are available in [Entropix Cloud](https://entropix.cloud).

## Invariants (Assertions)

### Deterministic
```yaml
invariants:
  - type: "contains"
    value: "confirmation_code"
  - type: "latency"
    max_ms: 2000
  - type: "valid_json"
```

### Semantic
```yaml
invariants:
  - type: "similarity"
    expected: "Your flight has been booked"
    threshold: 0.8
```

### Safety (Basic)
```yaml
invariants:
  - type: "excludes_pii"  # Basic regex patterns
  - type: "refusal_check"
```

> **Need advanced safety?** NER-based PII detection, ML-powered prompt injection detection, and factuality checking are available in [Entropix Cloud](https://entropix.cloud).

## Agent Adapters

### HTTP Endpoint
```yaml
agent:
  type: "http"
  endpoint: "http://localhost:8000/invoke"
```

### Python Callable
```python
from entropix import test_agent

@test_agent
async def my_agent(input: str) -> str:
    # Your agent logic
    return response
```

### LangChain
```yaml
agent:
  type: "langchain"
  module: "my_agent:chain"
```

## CI/CD Integration

> ⚠️ **Cloud Feature**: GitHub Actions integration requires [Entropix Cloud](https://entropix.cloud).

For local testing only:
```bash
# Run before committing (manual)
entropix run --min-score 0.9
```

With Entropix Cloud, you get:
- One-click GitHub Actions setup
- Automatic PR blocking below threshold
- Test history comparison
- Slack/Discord notifications

## Robustness Score

The Robustness Score is calculated as:

$$R = \frac{W_s \cdot S_{passed} + W_d \cdot D_{passed}}{N_{total}}$$

Where:
- $S_{passed}$ = Semantic variations passed
- $D_{passed}$ = Deterministic tests passed
- $W$ = Weights assigned by mutation difficulty

## Documentation

### Getting Started
- [📖 Usage Guide](docs/USAGE_GUIDE.md) - Complete end-to-end guide
- [⚙️ Configuration Guide](docs/CONFIGURATION_GUIDE.md) - All configuration options
- [🧪 Test Scenarios](docs/TEST_SCENARIOS.md) - Real-world examples with code

### For Developers
- [🏗️ Architecture & Modules](docs/MODULES.md) - How the code works
- [❓ Developer FAQ](docs/DEVELOPER_FAQ.md) - Q&A about design decisions
- [📦 Publishing Guide](docs/PUBLISHING.md) - How to publish to PyPI
- [🤝 Contributing](docs/CONTRIBUTING.md) - How to contribute

### Reference
- [📋 API Specification](docs/API_SPECIFICATION.md) - API reference
- [🧪 Testing Guide](docs/TESTING_GUIDE.md) - How to run and write tests
- [✅ Implementation Checklist](docs/IMPLEMENTATION_CHECKLIST.md) - Development progress

## License

AGPLv3 - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Tested with Entropix</strong><br>
  <img src="https://img.shields.io/badge/tested%20with-entropix-brightgreen" alt="Tested with Entropix">
</p>

<p align="center">
  <a href="https://entropix.cloud">
    <strong>⚡ Need speed? Try Entropix Cloud →</strong>
  </a>
</p>
