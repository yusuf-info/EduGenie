"""
EduGenie - Gemini Client
Google Gemini Powered Learning Assistant

Includes:
- Gemini API integration
- Quota/error handling
- Demo fallback mode
"""

import os
import json
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiConfigurationError(Exception):
    pass


class GeminiQuotaError(Exception):
    pass


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    """Create and cache Gemini client."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. "
            "Please add it to your .env file."
        )

    return genai.Client(api_key=api_key)


MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4,
    max_output_tokens: int = 4096,
) -> str:
    """
    Generate text using Gemini.

    If Gemini quota is exhausted, return a friendly
    demo-mode response instead of crashing the website.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    if len(prompt) > 100_000:
        raise ValueError(
            "Input is too large. Please use a shorter text."
        )

    try:

        client = get_client()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )

        text = getattr(response, "text", None)

        if text:
            return text.strip()

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    except Exception as exc:

        error_text = str(exc).lower()

        # Google Gemini quota error
        if (
            "429" in error_text
            or "resource_exhausted" in error_text
            or "quota" in error_text
            or "rate limit" in error_text
        ):

            return demo_fallback(prompt)

        raise


def demo_fallback(prompt: str) -> str:
    """
    Fallback response used when Gemini quota is exhausted.

    This keeps the EduGenie demonstration functional.
    """

    lower = prompt.lower()

    # -------------------------------------------------
    # QUESTION / ANSWER
    # -------------------------------------------------

    if "student question:" in lower:

        question = prompt.split(
            "Student question:",
            1
        )[-1].strip()

        return f"""
EduGenie Demo Mode

Gemini API quota has currently been reached.

Your question:
{question}

General learning guidance:

This topic should be understood by first identifying
the basic definition, then learning the important
concepts, and finally applying them through examples
and practice.

Suggested study approach:

1. Learn the basic definition.
2. Understand the main concepts.
3. Study a simple example.
4. Practice the concept yourself.
5. Review the important points.

Note:
Gemini API will automatically be used again when
available.
""".strip()

    # -------------------------------------------------
    # TOPIC EXPLANATION
    # -------------------------------------------------

    if "explain this topic" in lower:

        topic = ""

        if "TOPIC:" in prompt:
            topic = prompt.split(
                "TOPIC:",
                1
            )[1].split(
                "Use this structure:",
                1
            )[0].strip()

        return f"""
EduGenie Demo Mode
==================

Topic: {topic}

1. Simple Definition
--------------------
{topic} is a subject that can be understood by
learning its fundamental concepts and how those
concepts are connected.

2. Easy Explanation
-------------------
Start with the basic idea of {topic}. Learn the
important terms first and then study how the concepts
work together.

3. Important Points
-------------------
• Understand the basic terminology.
• Learn the main concepts.
• Study practical examples.
• Practice what you learn.
• Review common mistakes.

4. Real-World Example
---------------------
Many academic and professional subjects become easier
when the concepts are connected to real-world
applications.

5. Simple Example
-----------------
Take one small example of {topic}, understand each
step, and then try a similar example independently.

6. Short Summary
----------------
Learn the basics first, understand the main concepts,
and then strengthen your knowledge through examples
and practice.

Demo mode is active because the Gemini free-tier
quota has been reached.
""".strip()

    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    if "summarize the following text" in lower:

        if "TEXT:" in prompt:
            source = prompt.split(
                "TEXT:",
                1
            )[-1].strip()
        else:
            source = ""

        words = source.split()

        if len(words) > 80:
            short_text = " ".join(words[:80]) + "..."
        else:
            short_text = source

        return f"""
EduGenie Demo Mode - Summary

Main Content:
{short_text}

Key Points:
• The supplied text contains the main subject matter
  provided by the user.
• Important information should be identified and
  reviewed carefully.
• Repeated or unnecessary information can be removed
  during revision.

Key Takeaway:
Review the main ideas first, then study the supporting
details.

Gemini quota has currently been reached, so this
summary is being generated using EduGenie's fallback
mode.
""".strip()

    # -------------------------------------------------
    # LEARNING PATH
    # -------------------------------------------------

    if "learning roadmap" in lower:

        topic = ""

        marker = "Create a structured learning roadmap for:"

        if marker in prompt:
            topic = prompt.split(
                marker,
                1
            )[1].split(
                "Use exactly these major sections:",
                1
            )[0].strip()

        return f"""
EduGenie Learning Roadmap - Demo Mode

Topic: {topic}

# BEGINNER

Prerequisites:
• Basic computer knowledge
• Basic understanding of the subject area

Topics:
1. Introduction to {topic}
2. Basic terminology
3. Fundamental concepts
4. Simple examples

Practice:
• Complete beginner exercises
• Create small examples
• Review basic concepts


# INTERMEDIATE

Topics:
1. Core concepts
2. Practical techniques
3. Problem solving
4. Real-world applications

Practice Projects:
• Build a small project
• Solve practical problems
• Review and improve your work


# ADVANCED

Topics:
1. Advanced concepts
2. Optimization
3. Advanced problem solving
4. Professional applications

Projects:
• Build a complete project
• Solve a real-world problem
• Document your work


# RESOURCES

Recommended resource types:

• Official documentation
• Beginner-friendly books
• Online courses
• Video tutorials
• Practice websites
• Project-based learning


# ESTIMATED TIMELINE

Beginner:
2-4 weeks

Intermediate:
4-8 weeks

Advanced:
8-12+ weeks

The exact timeline depends on your previous knowledge
and daily study time.

Demo mode is active because the Gemini free-tier
quota has been reached.
""".strip()

    # -------------------------------------------------
    # QUIZ
    # -------------------------------------------------

    if "multiple-choice questions" in lower:

        topic = ""

        marker = "about:"

        if marker in prompt:
            topic = prompt.split(
                marker,
                1
            )[1].split(
                "Each question",
                1
            )[0].strip()

        quiz = [
            {
                "question": f"What is an important first step when learning {topic}?",
                "options": [
                    "Understand the basic concepts",
                    "Skip all fundamentals",
                    "Avoid practice",
                    "Memorize unrelated information"
                ],
                "answer": "A",
                "explanation": "Understanding the fundamentals provides a strong foundation."
            },
            {
                "question": f"Which approach is useful for studying {topic}?",
                "options": [
                    "Only reading once",
                    "Learning concepts and practicing them",
                    "Avoiding examples",
                    "Skipping difficult topics"
                ],
                "answer": "B",
                "explanation": "Combining conceptual learning with practice improves understanding."
            },
            {
                "question": f"How can a student improve their knowledge of {topic}?",
                "options": [
                    "Never practice",
                    "Avoid projects",
                    "Practice with examples and projects",
                    "Study without reviewing"
                ],
                "answer": "C",
                "explanation": "Examples and projects help turn theoretical knowledge into practical skills."
            }
        ]

        return json.dumps(quiz)

    # -------------------------------------------------
    # GENERIC FALLBACK
    # -------------------------------------------------

    return """
EduGenie Demo Mode

The Gemini API quota has currently been reached.

Your EduGenie application is working correctly, but
Gemini requests are temporarily unavailable.

Please try again when the API quota becomes available.
""".strip()