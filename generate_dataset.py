from __future__ import annotations

from config import MAX_EXAMPLES, MIN_EXAMPLES, OUTPUT_FILE
from generators.bpmn_generator import write_jsonl


def main() -> None:
    count = write_jsonl(OUTPUT_FILE)
    if not MIN_EXAMPLES <= count <= MAX_EXAMPLES:
        raise RuntimeError(f"Generated {count} examples, expected between {MIN_EXAMPLES} and {MAX_EXAMPLES}")
    print(f"Generated {count} BPMN training examples at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
