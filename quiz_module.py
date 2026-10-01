"""
EduGenie - Quiz Generation Module
"""

import json
import re

from gemini_client import generate_text


def _clean_json(text: str) -> str:
    """Remove accidental Markdown code fences."""

    text = text.strip()

    # Remove ```json ... ```
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text.strip()


def _validate_quiz(data):
    """Validate Gemini's quiz structure."""

    if not isinstance(data, list):
        raise ValueError("Quiz response is not a list.")

    if len(data) != 3:
        raise ValueError(
            f"Expected 3 questions, received {len(data)}."
        )

    for index, item in enumerate(data, start=1):

        if not isinstance(item, dict):
            raise ValueError(
                f"Question {index} has invalid format."
            )

        required = {
            "question",
            "options",
            "answer",
            "explanation",
        }

        missing = required - item.keys()

        if missing:
            raise ValueError(
                f"Question {index} is missing: "
                f"{', '.join(missing)}"
            )

        options = item["options"]

        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(
                f"Question {index} must have exactly 4 options."
            )

        if item["answer"] not in ["A", "B", "C", "D"]:
            raise ValueError(
                f"Question {index} has an invalid answer."
            )

    return data


def generate_quiz(topic: str):
    """Generate exactly 3 MCQs with 4 options each."""

    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a quiz topic.")

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions about:

{topic}

Each question must contain exactly 4 options.

Return ONLY valid JSON.

Use this exact structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "A",
    "explanation": "Why A is correct."
  }}
]

Important:
- Exactly 3 questions.
- Exactly 4 options per question.
- answer must be A, B, C, or D.
- Only one answer should be correct.
- Include a short explanation.
- No Markdown.
- No text before or after the JSON.
"""

    raw = generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=3500,
    )

    cleaned = _clean_json(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid quiz JSON."
        ) from exc

    return _validate_quiz(data)