from __future__ import annotations

from typing import Any

from .common import BpmnBuilder, attach_artifacts, normalize_tasks


def generate(process_name: str, task_labels: list[str], data_objects: list[str] | None = None, data_stores: list[str] | None = None) -> dict[str, Any]:
    builder = BpmnBuilder(process_name, "transaction")
    tasks = normalize_tasks(task_labels, 5)
    start = builder.element("startEvent", f"{process_name} requested", "start_event")
    validate = builder.element("businessRuleTask", tasks[0], f"task_{tasks[0]}")
    transaction = builder.element("transaction", f"Execute transaction for {tasks[1]}", f"transaction_{tasks[1]}")
    split = builder.element("exclusiveGateway", "Transaction successful?", "transaction_result_gateway")
    commit = builder.element("serviceTask", tasks[2], f"task_{tasks[2]}")
    compensate = builder.element("manualTask", tasks[3], f"task_{tasks[3]}")
    success_end = builder.element("endEvent", f"{process_name} committed", "success_end_event")
    compensation_end = builder.element("compensationEvent", f"{process_name} compensation recorded", "compensation_event")
    error_end = builder.element("errorEndEvent", f"{process_name} failed", "error_end_event")
    notify = builder.element("sendTask", tasks[4], f"task_{tasks[4]}")
    builder.flow(start, validate)
    builder.flow(validate, transaction)
    builder.flow(transaction, split)
    builder.flow(split, commit, name="success")
    builder.flow(commit, notify)
    builder.flow(notify, success_end)
    builder.flow(split, compensate, name="failure")
    builder.flow(compensate, compensation_end)
    builder.flow(compensation_end, error_end)
    attach_artifacts(builder, validate, data_objects, data_stores)
    return builder.process()
