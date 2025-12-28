"""Shared test fixtures for Entropix tests."""

import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_yaml():
    """Sample valid config YAML."""
    return """
agent:
  endpoint: "http://localhost:8000/chat"
  type: http
  timeout: 30

golden_prompts:
  - "Test prompt 1"
  - "Test prompt 2"

mutations:
  count: 5
  types:
    - paraphrase
    - noise

invariants:
  - type: latency
    max_ms: 5000
"""


@pytest.fixture
def config_file(temp_dir, sample_config_yaml):
    """Create a config file in temp directory."""
    config_path = temp_dir / "entropix.yaml"
    config_path.write_text(sample_config_yaml)
    return config_path


@pytest.fixture
def minimal_config_yaml():
    """Minimal valid config YAML."""
    return """
agent:
  endpoint: "http://localhost:8000/chat"
  type: http

golden_prompts:
  - "Test prompt"

mutations:
  count: 2
  types:
    - paraphrase

invariants: []
"""


@pytest.fixture
def minimal_config_file(temp_dir, minimal_config_yaml):
    """Create a minimal config file."""
    config_path = temp_dir / "entropix.yaml"
    config_path.write_text(minimal_config_yaml)
    return config_path
