from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "inclusive")
    tasks = normalize_tasks(task_labels, 5)
    start = builder.element("startEvent", f"{process_name} initiated", "start_event")
    assess = builder.element("businessRuleTask", tasks[0], f"task_{tasks[0]}")
    split = builder.element("inclusiveGateway", "Select applicable paths", "inclusive_split_gateway")
    builder.flow(start, assess)
    builder.flow(assess, split)
    branches = []
    for label, task_type in zip(tasks[1:4], ["userTask", "serviceTask", "manualTask"]):
        branch = builder.element(task_type, label, f"task_{label}")
        branches.append(branch)
        builder.flow(split, branch, name=f"if {label.lower()} applies")
    join = builder.element("inclusiveGateway", "Merge completed paths", "inclusive_join_gateway")
    for branch in branches:
        builder.flow(branch, join)
    close = builder.element("sendTask", tasks[4], f"task_{tasks[4]}")
    end = builder.element("endEvent", f"{process_name} closed", "end_event")
    builder.flow(join, close)
    builder.flow(close, end)
    attach_artifacts(builder, assess, data_objects, data_stores)
    return builder.process()
