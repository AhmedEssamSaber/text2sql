import json
from typing import List


def load_examples(path: str) -> List[str]:
    with open(path, "r") as f:
        data = json.load(f)

    texts = []

    for ex in data:
        texts.append(
            f"Question: {ex['question']} SQL: {ex['sql']}"
        )

    return texts