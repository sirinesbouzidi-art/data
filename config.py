"""Configuration for BPMN dataset generation."""
from __future__ import annotations

from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "bpmn_training_dataset.jsonl"
MIN_EXAMPLES = 1000
MAX_EXAMPLES = 3000
