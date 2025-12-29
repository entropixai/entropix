"""
flakestorm Integrations Module

V2 features for integrating with external services:
- HuggingFace model downloading
- GitHub Actions for CI/CD
- Local embeddings for semantic similarity
"""

# V2 features - import guards for optional dependencies

__all__ = [
    "HuggingFaceModelProvider",
    "GitHubActionsIntegration",
    "LocalEmbedder",
]


def __getattr__(name: str):
    """Lazy loading of integration modules."""
    if name == "HuggingFaceModelProvider":
        from flakestorm.integrations.huggingface import HuggingFaceModelProvider

        return HuggingFaceModelProvider
    elif name == "GitHubActionsIntegration":
        from flakestorm.integrations.github_actions import GitHubActionsIntegration

        return GitHubActionsIntegration
    elif name == "LocalEmbedder":
        from flakestorm.assertions.semantic import LocalEmbedder

        return LocalEmbedder
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
