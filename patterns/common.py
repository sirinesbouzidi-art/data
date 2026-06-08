"""Shared utilities for deterministic BPMN process construction."""
from __future__ import annotations

import re
from typing import Any

ARTIFACT_TYPES = {"textAnnotation", "dataObjectReference", "dataStoreReference"}


def snake_case(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "item"


class BpmnBuilder:
    """Small deterministic builder that guarantees unique snake_case IDs."""

    def __init__(self, process_name: str, pattern_slug: str) -> None:
        self.process_name = process_name
        self.process_id = f"process_{snake_case(process_name)}_{snake_case(pattern_slug)}"
        self.elements: list[dict[str, Any]] = []
        self.flows: list[dict[str, Any]] = []
        self._ids: set[str] = {self.process_id}
        self._counts: dict[str, int] = {}

    def unique_id(self, base: str) -> str:
        base_id = snake_case(base)
        count = self._counts.get(base_id, 0)
        candidate = base_id if count == 0 else f"{base_id}_{count + 1}"
        while candidate in self._ids:
            count += 1
            candidate = f"{base_id}_{count + 1}"
        self._counts[base_id] = count + 1
        self._ids.add(candidate)
        return candidate

    def element(self, bpmn_type: str, name: str, id_base: str | None = None, **extra: Any) -> dict[str, Any]:
        element = {"id": self.unique_id(id_base or f"{bpmn_type}_{name}"), "type": bpmn_type, "name": name}
        element.update({key: value for key, value in extra.items() if value is not None})
        self.elements.append(element)
        return element

    def flow(
        self,
        source: dict[str, Any],
        target: dict[str, Any],
        bpmn_type: str = "sequenceFlow",
        name: str | None = None,
        id_base: str | None = None,
    ) -> dict[str, Any]:
        flow = {
            "id": self.unique_id(id_base or f"{bpmn_type}_{source['id']}_to_{target['id']}"),
            "type": bpmn_type,
            "sourceRef": source["id"],
            "targetRef": target["id"],
        }
        if name:
            flow["name"] = name
        self.flows.append(flow)
        return flow

    def process(self) -> dict[str, Any]:
        return {"process": {"id": self.process_id, "name": self.process_name, "elements": self.elements, "flows": self.flows}}


def normalize_tasks(task_labels: list[str], minimum: int = 3) -> list[str]:
    tasks = [label.strip() for label in task_labels if label.strip()]
    while len(tasks) < minimum:
        tasks.append(f"Complete process step {len(tasks) + 1}")
    return tasks


def attach_artifacts(builder: BpmnBuilder, anchor: dict[str, Any], data_objects: list[str] | None, data_stores: list[str] | None) -> None:
    for label in data_objects or []:
        artifact = builder.element("dataObjectReference", label, f"data_object_{label}")
        builder.flow(anchor, artifact, "association", f"uses {label}")
    for label in data_stores or []:
        store = builder.element("dataStoreReference", label, f"data_store_{label}")
        builder.flow(anchor, store, "association", f"updates {label}")
