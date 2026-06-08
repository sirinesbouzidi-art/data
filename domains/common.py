"""Domain scenario helpers."""
from __future__ import annotations

PATTERN_SEQUENCE = [
    "linear",
    "xor",
    "parallel",
    "inclusive",
    "event_based",
    "subprocess",
    "call_activity",
    "transaction",
    "event_subprocess",
]


def make_scenarios(domain: str, names: list[str], objects: list[str], stores: list[str]) -> list[dict[str, object]]:
    scenarios: list[dict[str, object]] = []
    for index, name in enumerate(names):
        noun = name.lower()
        scenarios.append(
            {
                "process_name": name,
                "pattern": PATTERN_SEQUENCE[index % len(PATTERN_SEQUENCE)],
                "task_labels": [
                    f"Capture {noun} request",
                    f"Validate {noun} details",
                    f"Coordinate {noun} activities",
                    f"Review {noun} outcome",
                    f"Notify stakeholders about {noun}",
                ],
                "data_objects": [objects[index % len(objects)], objects[(index + 3) % len(objects)]],
                "data_stores": [stores[index % len(stores)]],
                "domain": domain,
            }
        )
    return scenarios
