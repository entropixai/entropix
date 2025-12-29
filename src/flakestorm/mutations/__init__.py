"""
flakestorm Mutation Engine

Generates adversarial mutations from golden prompts using local LLMs.
Supports paraphrasing, noise injection, tone shifting, and prompt injection.
"""

from flakestorm.mutations.engine import MutationEngine
from flakestorm.mutations.templates import MUTATION_TEMPLATES, MutationTemplates
from flakestorm.mutations.types import Mutation, MutationType

__all__ = [
    "MutationEngine",
    "MutationType",
    "Mutation",
    "MutationTemplates",
    "MUTATION_TEMPLATES",
]
