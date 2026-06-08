"""Natural-language prompt generation for BPMN fine-tuning records."""
from __future__ import annotations

PROMPT_TEMPLATES = [
    "Create a BPMN process for {process_name}.",
    "Design a workflow for {process_name}.",
    "Generate a business process for {process_name}.",
    "Model the {process_name} workflow.",
    "Create a detailed BPMN diagram for {process_name}.",
    "Convert the {process_name} procedure into BPMN JSON.",
    "Draft a valid BPMN 2.0 process describing {process_name}.",
    "Build a structured BPMN JSON model for {process_name}.",
]


def generate_prompts(process_name: str) -> list[str]:
    return [template.format(process_name=process_name) for template in PROMPT_TEMPLATES]
