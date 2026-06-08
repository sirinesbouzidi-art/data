from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "call_activity")
    tasks = normalize_tasks(task_labels, 4)
    start = builder.element("startEvent", f"{process_name} started", "start_event")
    qualify = builder.element("businessRuleTask", tasks[0], f"task_{tasks[0]}")
    call = builder.element("callActivity", f"Call reusable procedure for {tasks[1]}", f"call_activity_{tasks[1]}")
    inspect = builder.element("userTask", tasks[2], f"task_{tasks[2]}")
    close = builder.element("sendTask", tasks[3], f"task_{tasks[3]}")
    end = builder.element("endEvent", f"{process_name} finished", "end_event")
    for source, target in [(start, qualify), (qualify, call), (call, inspect), (inspect, close), (close, end)]:
        builder.flow(source, target)
    attach_artifacts(builder, qualify, data_objects, data_stores)
    return builder.process()
