"""Validation for the supported BPMN JSON training schema."""
from __future__ import annotations

import re
from typing import Any

ALLOWED_ELEMENT_TYPES = {
    "startEvent", "messageStartEvent", "timerStartEvent", "signalStartEvent", "conditionalStartEvent",
    "intermediateCatchEvent", "intermediateThrowEvent", "messageEvent", "timerEvent", "signalEvent",
    "escalationEvent", "compensationEvent", "linkEvent", "endEvent", "terminateEndEvent", "errorEndEvent",
    "messageEndEvent", "signalEndEvent", "escalationEndEvent", "userTask", "serviceTask", "scriptTask",
    "businessRuleTask", "manualTask", "sendTask", "receiveTask", "exclusiveGateway", "parallelGateway",
    "inclusiveGateway", "eventBasedGateway", "complexGateway", "subProcess", "adHocSubProcess", "transaction",
    "eventSubProcess", "callActivity", "textAnnotation", "dataObjectReference", "dataStoreReference",
}
ALLOWED_FLOW_TYPES = {"sequenceFlow", "messageFlow", "association"}
START_TYPES = {"startEvent", "messageStartEvent", "timerStartEvent", "signalStartEvent", "conditionalStartEvent"}
END_TYPES = {"endEvent", "terminateEndEvent", "errorEndEvent", "messageEndEvent", "signalEndEvent", "escalationEndEvent"}
ARTIFACT_TYPES = {"textAnnotation", "dataObjectReference", "dataStoreReference"}
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


class BpmnValidationError(ValueError):
    """Raised when a generated BPMN process violates the supported schema."""


def validate_bpmn(document: dict[str, Any]) -> None:
    errors = collect_validation_errors(document)
    if errors:
        raise BpmnValidationError("; ".join(errors))


def collect_validation_errors(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    process = document.get("process")
    if not isinstance(process, dict):
        return ["document must contain a process object"]

    for key in ("id", "name", "elements", "flows"):
        if key not in process:
            errors.append(f"process missing {key}")
    if errors:
        return errors

    elements = process["elements"]
    flows = process["flows"]
    if not isinstance(elements, list):
        errors.append("process.elements must be a list")
        elements = []
    if not isinstance(flows, list):
        errors.append("process.flows must be a list")
        flows = []

    seen_ids: set[str] = set()
    element_ids: set[str] = set()
    incoming: dict[str, int] = {}
    outgoing: dict[str, int] = {}

    process_id = process.get("id")
    if not isinstance(process_id, str) or not SNAKE_CASE.fullmatch(process_id):
        errors.append("process.id must be snake_case")
    else:
        seen_ids.add(process_id)

    for element in elements:
        if not isinstance(element, dict):
            errors.append("each element must be an object")
            continue
        element_id = element.get("id")
        element_type = element.get("type")
        if element_type in ALLOWED_FLOW_TYPES:
            errors.append(f"flow type {element_type} must not appear in elements")
        if element_type not in ALLOWED_ELEMENT_TYPES:
            errors.append(f"unsupported element type {element_type}")
        if not isinstance(element_id, str) or not SNAKE_CASE.fullmatch(element_id):
            errors.append(f"element id {element_id} must be snake_case")
            continue
        if element_id in seen_ids:
            errors.append(f"duplicate id {element_id}")
        seen_ids.add(element_id)
        element_ids.add(element_id)
        incoming[element_id] = 0
        outgoing[element_id] = 0

    for flow in flows:
        if not isinstance(flow, dict):
            errors.append("each flow must be an object")
            continue
        flow_id = flow.get("id")
        flow_type = flow.get("type")
        if flow_type not in ALLOWED_FLOW_TYPES:
            errors.append(f"unsupported flow type {flow_type}")
        if flow_type in ALLOWED_ELEMENT_TYPES:
            errors.append(f"element type {flow_type} must not appear in flows")
        if not isinstance(flow_id, str) or not SNAKE_CASE.fullmatch(flow_id):
            errors.append(f"flow id {flow_id} must be snake_case")
        elif flow_id in seen_ids:
            errors.append(f"duplicate id {flow_id}")
        else:
            seen_ids.add(flow_id)
        source = flow.get("sourceRef")
        target = flow.get("targetRef")
        if source not in element_ids:
            errors.append(f"flow {flow_id} has invalid sourceRef {source}")
        else:
            outgoing[source] += 1
        if target not in element_ids:
            errors.append(f"flow {flow_id} has invalid targetRef {target}")
        else:
            incoming[target] += 1

    element_types = {element.get("type") for element in elements if isinstance(element, dict)}
    if not element_types.intersection(START_TYPES):
        errors.append("process must contain at least one start event")
    if not element_types.intersection(END_TYPES):
        errors.append("process must contain at least one end event")

    for element in elements:
        if not isinstance(element, dict):
            continue
        element_id = element.get("id")
        element_type = element.get("type")
        if element_id not in element_ids:
            continue
        if element_type in START_TYPES:
            if outgoing[element_id] == 0:
                errors.append(f"start event {element_id} has no outgoing flow")
        elif element_type in END_TYPES:
            if incoming[element_id] == 0:
                errors.append(f"end event {element_id} has no incoming flow")
        elif element_type in ARTIFACT_TYPES:
            if incoming[element_id] + outgoing[element_id] == 0:
                errors.append(f"artifact {element_id} is not associated")
        else:
            if incoming[element_id] + outgoing[element_id] == 0:
                errors.append(f"element {element_id} is dangling")
    return errors
