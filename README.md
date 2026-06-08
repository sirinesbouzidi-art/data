# Deterministic BPMN Dataset Generator

This project generates a JSONL fine-tuning dataset for natural-language-to-BPMN-JSON training. BPMN structures are created deterministically from predefined BPMN patterns rather than by an LLM.

## Supported schema

Every assistant answer is a JSON string compatible with:

```json
{
  "process": {
    "id": "string",
    "name": "string",
    "elements": [],
    "flows": []
  }
}
```

## Implemented BPMN patterns

- Linear sequence
- Exclusive gateway (XOR)
- Parallel gateway
- Inclusive gateway
- Event-based gateway
- SubProcess
- Call Activity
- Transaction
- Event SubProcess

## Domain coverage

The generator includes 20 realistic scenarios for each of these domains:

- HR
- Finance
- Telecom
- Healthcare
- Education
- Logistics
- Manufacturing

With 140 scenarios and 8 prompt templates per scenario, the default run creates 1,120 training examples.

## Validation

Each generated BPMN process is validated before it is written. The validator checks:

- Unique IDs across processes, elements, and flows
- Allowed case-sensitive BPMN types
- Valid flow references
- At least one start event and one end event
- Separation of elements and flows
- snake_case IDs
- No dangling unconnected elements or artifacts

## Running

```bash
python generate_dataset.py
```

The output file is written to:

```text
output/bpmn_training_dataset.jsonl
```

## Record format

Each JSONL row has the following chat format:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Create a BPMN process for Loan Approval."
    },
    {
      "role": "assistant",
      "content": "{ BPMN JSON }"
    }
  ]
}
```
