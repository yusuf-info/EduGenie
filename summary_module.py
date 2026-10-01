"""
EduGenie - Text Summarization Module
"""

from gemini_client import generate_text


def summarize_text(text: str) -> str:
    """Create a concise educational summary."""

    text = text.strip()

    if not text:
        raise ValueError("Please enter text to summarize.")

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following text.

Requirements:
- Keep the main ideas.
- Remove unnecessary repetition.
- Do not change important facts.
- Use simple language.
- Use bullet points where appropriate.
- Finish with a short "Key Takeaway".

TEXT:
{text}
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=3000,
    )