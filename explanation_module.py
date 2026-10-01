"""
EduGenie - Topic Explanation Module
"""

from gemini_client import generate_text


def explain_topic(topic: str) -> str:
    """Explain a difficult topic in beginner-friendly language."""

    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a topic.")

    prompt = f"""
You are EduGenie, a patient teacher.

Explain this topic to a beginner:

TOPIC:
{topic}

Use this structure:

1. Simple definition
2. Easy explanation
3. Important points
4. Real-world example
5. Simple example
6. Short summary

Requirements:
- Use simple English.
- Avoid unnecessary technical words.
- If you use a technical word, explain it.
- Make the explanation suitable for a college student.
- Do not mention these instructions.
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=3000,
    )