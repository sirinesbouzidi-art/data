from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "xor")
    tasks = normalize_tasks(task_labels, 4)
    start = builder.element("startEvent", f"{process_name} received", "start_event")
    review = builder.element("userTask", tasks[0], f"task_{tasks[0]}")
    split = builder.element("exclusiveGateway", "Decision required", "exclusive_decision_gateway")
    builder.flow(start, review)
    builder.flow(review, split)
    branch_tasks = []
    for index, label in enumerate(tasks[1:3], start=1):
        branch = builder.element("serviceTask" if index == 1 else "manualTask", label, f"task_{label}")
        branch_tasks.append(branch)
        builder.flow(split, branch, name=f"option {index}")
    join = builder.element("exclusiveGateway", "Decision outcome merged", "exclusive_merge_gateway")
    for branch in branch_tasks:
        builder.flow(branch, join)
    finalize = builder.element("sendTask", tasks[3], f"task_{tasks[3]}")
    end = builder.element("endEvent", f"{process_name} resolved", "end_event")
    builder.flow(join, finalize)
    builder.flow(finalize, end)
    attach_artifacts(builder, review, data_objects, data_stores)
    return builder.process()
