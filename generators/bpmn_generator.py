"""Dataset orchestration for deterministic BPMN pattern generation."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

from generators.prompt_generator import generate_prompts
from validators.bpmn_validator import validate_bpmn

PATTERN_MODULES = {
    "linear": "patterns.linear",
    "xor": "patterns.xor",
    "parallel": "patterns.parallel",
    "inclusive": "patterns.inclusive",
    "event_based": "patterns.event_based",
    "subprocess": "patterns.subprocess",
    "call_activity": "patterns.call_activity",
    "transaction": "patterns.transaction",
    "event_subprocess": "patterns.event_subprocess",
}
DOMAIN_MODULES = ["hr", "finance", "telecom", "healthcare", "education", "logistics", "manufacturing"]


def load_scenarios() -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for domain in DOMAIN_MODULES:
        module = importlib.import_module(f"domains.{domain}")
        scenarios.extend(module.SCENARIOS)
    return scenarios


def generate_process(scenario: dict[str, Any]) -> dict[str, Any]:
    pattern = str(scenario["pattern"])
    module = importlib.import_module(PATTERN_MODULES[pattern])
    process = module.generate(
        process_name=str(scenario["process_name"]),
        task_labels=list(scenario.get("task_labels", [])),
        data_objects=list(scenario.get("data_objects", [])),
        data_stores=list(scenario.get("data_stores", [])),
    )
    validate_bpmn(process)
    return process


def generate_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for scenario in load_scenarios():
        process = generate_process(scenario)
        assistant_content = json.dumps(process, ensure_ascii=False, sort_keys=True)
        for prompt in generate_prompts(str(scenario["process_name"])):
            records.append(
                {
                    "messages": [
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": assistant_content},
                    ]
                }
            )
    return records


def write_jsonl(path: str | Path) -> int:
    records = generate_records()
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return len(records)
