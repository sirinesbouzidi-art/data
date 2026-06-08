from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "event_subprocess")
    tasks = normalize_tasks(task_labels, 5)
    start = builder.element("startEvent", f"{process_name} started", "start_event")
    main_task = builder.element("userTask", tasks[0], f"task_{tasks[0]}")
    service = builder.element("serviceTask", tasks[1], f"task_{tasks[1]}")
    end = builder.element("endEvent", f"{process_name} completed", "end_event")
    event_subprocess = builder.element("eventSubProcess", f"Handle exception during {process_name}", "event_subprocess")
    trigger = builder.element("conditionalStartEvent", "Exception condition detected", "conditional_start_event")
    recover = builder.element("manualTask", tasks[2], f"task_{tasks[2]}")
    escalate = builder.element("escalationEndEvent", tasks[3], f"escalation_end_{tasks[3]}")
    notify = builder.element("sendTask", tasks[4], f"task_{tasks[4]}")
    builder.flow(start, main_task)
    builder.flow(main_task, service)
    builder.flow(service, end)
    builder.flow(main_task, event_subprocess, "association", "monitored by")
    builder.flow(trigger, recover)
    builder.flow(recover, notify)
    builder.flow(notify, escalate)
    attach_artifacts(builder, main_task, data_objects, data_stores)
    return builder.process()
