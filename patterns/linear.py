from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks

TASK_TYPES = ["userTask", "serviceTask", "businessRuleTask", "manualTask", "sendTask", "receiveTask", "scriptTask"]


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "linear")
    start = builder.element("startEvent", f"{process_name} requested", "start_event")
    previous = start
    tasks = normalize_tasks(task_labels, 3)
    first_task = None
    for index, label in enumerate(tasks):
        task = builder.element(TASK_TYPES[index % len(TASK_TYPES)], label, f"task_{label}")
        first_task = first_task or task
        builder.flow(previous, task)
        previous = task
    end = builder.element("endEvent", f"{process_name} completed", "end_event")
    builder.flow(previous, end)
    attach_artifacts(builder, first_task or previous, data_objects, data_stores)
    return builder.process()
