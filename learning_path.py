"""
EduGenie - Personalized Learning Path Module
"""

from gemini_client import generate_text


def get_learning_path(topic: str) -> str:
    """Generate a beginner-to-advanced learning roadmap."""

    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a subject or skill.")

    prompt = f"""
You are EduGenie, an educational learning-path designer.

Create a structured learning roadmap for:

{topic}

Use exactly these major sections:

# BEGINNER

Include:
- Prerequisites
- Topics to learn
- Recommended order
- Small practice activities

# INTERMEDIATE

Include:
- Topics to learn
- Recommended order
- Practice projects

# ADVANCED

Include:
- Advanced concepts
- Projects
- Real-world applications

# RESOURCES

Suggest:
- Documentation
- Books
- Video/course types
- Practice websites

# ESTIMATED TIMELINE

Give a realistic approximate learning timeline.

Rules:
- Start from zero knowledge.
- Progress gradually.
- Avoid unnecessary topics.
- Use simple language.
- Do not invent specific URLs.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=4000,
    )