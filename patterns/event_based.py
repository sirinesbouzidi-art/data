from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "event_based")
    tasks = normalize_tasks(task_labels, 4)
    start = builder.element("messageStartEvent", f"{process_name} request received", "message_start_event")
    gateway = builder.element("eventBasedGateway", "Wait for external event", "event_based_gateway")
    builder.flow(start, gateway)
    message = builder.element("messageEvent", "Customer response received", "message_event")
    timer = builder.element("timerEvent", "Response deadline reached", "timer_event")
    signal = builder.element("signalEvent", "Operational signal received", "signal_event")
    event_tasks = [
        builder.element("userTask", tasks[0], f"task_{tasks[0]}"),
        builder.element("serviceTask", tasks[1], f"task_{tasks[1]}"),
        builder.element("manualTask", tasks[2], f"task_{tasks[2]}"),
    ]
    for event, task in zip([message, timer, signal], event_tasks):
        builder.flow(gateway, event)
        builder.flow(event, task)
    join = builder.element("exclusiveGateway", "Event path selected", "event_path_merge_gateway")
    for task in event_tasks:
        builder.flow(task, join)
    finish = builder.element("sendTask", tasks[3], f"task_{tasks[3]}")
    end = builder.element("messageEndEvent", f"{process_name} notification sent", "message_end_event")
    builder.flow(join, finish)
    builder.flow(finish, end)
    attach_artifacts(builder, event_tasks[0], data_objects, data_stores)
    return builder.process()
