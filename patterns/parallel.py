from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "parallel")
    tasks = normalize_tasks(task_labels, 5)
    start = builder.element("startEvent", f"{process_name} started", "start_event")
    prepare = builder.element("userTask", tasks[0], f"task_{tasks[0]}")
    split = builder.element("parallelGateway", "Work in parallel", "parallel_split_gateway")
    builder.flow(start, prepare)
    builder.flow(prepare, split)
    branches = []
    for label, task_type in zip(tasks[1:4], ["serviceTask", "manualTask", "businessRuleTask"]):
        branch = builder.element(task_type, label, f"task_{label}")
        branches.append(branch)
        builder.flow(split, branch)
    join = builder.element("parallelGateway", "Synchronize work", "parallel_join_gateway")
    for branch in branches:
        builder.flow(branch, join)
    finish = builder.element("sendTask", tasks[4], f"task_{tasks[4]}")
    end = builder.element("endEvent", f"{process_name} completed", "end_event")
    builder.flow(join, finish)
    builder.flow(finish, end)
    attach_artifacts(builder, prepare, data_objects, data_stores)
    return builder.process()
