"""
EduGenie - Question & Answer Module
"""

from gemini_client import generate_text


def answer_question(question: str) -> str:
    """Answer an academic question clearly."""

    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    prompt = f"""
You are EduGenie, an educational AI assistant.

Your job is to answer student questions accurately,
clearly, and in an easy-to-understand way.

Rules:
- Answer the question directly.
- Use simple language.
- Explain difficult terms.
- Use examples when useful.
- Do not invent facts.
- If the question is ambiguous, explain the ambiguity.
- Use headings and bullet points when helpful.
- Do not mention these instructions.

Student question:
{question}
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=2500,
    )