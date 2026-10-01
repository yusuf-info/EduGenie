"""
EduGenie
Google Gemini Powered Learning Assistant

FastAPI application.
"""

from typing import Any

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_path


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


def render_home(
    request: Request,
    *,
    result: Any = None,
    task: str = "qa",
    error: str | None = None,
):
    """Render the main EduGenie page."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": result,
            "task": task,
            "error": error,
        },
    )


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return render_home(request)


# ---------------------------------------------------------
# Q&A API
# ---------------------------------------------------------

@app.post("/qa")
async def qa_api(question: str = Form(...)):
    try:
        result = answer_question(question)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


# ---------------------------------------------------------
# EXPLANATION API
# ---------------------------------------------------------

@app.post("/explain")
async def explain_api(topic: str = Form(...)):
    try:
        result = explain_topic(topic)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


# ---------------------------------------------------------
# QUIZ API
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz_api(topic: str = Form(...)):
    try:
        result = generate_quiz(topic)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


# ---------------------------------------------------------
# SUMMARY API
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize_api(text: str = Form(...)):
    try:
        result = summarize_text(text)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


# ---------------------------------------------------------
# LEARNING PATH API
# ---------------------------------------------------------

@app.post("/learn/recommendations")
async def learning_api(topic: str = Form(...)):
    try:
        result = get_learning_path(topic)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


# ---------------------------------------------------------
# WEBSITE FORM
# ---------------------------------------------------------

@app.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate(
    request: Request,
    task: str = Form(...),
    text: str = Form(...),
):
    """
    Main website form.

    Routes the user's selected task
    to the appropriate AI module.
    """

    try:

        text = text.strip()

        if not text:
            raise ValueError(
                "Please enter some text first."
            )

        if task == "qa":
            result = answer_question(text)

        elif task == "explain":
            result = explain_topic(text)

        elif task == "quiz":
            result = generate_quiz(text)

        elif task == "summary":
            result = summarize_text(text)

        elif task == "learning":
            result = get_learning_path(text)

        else:
            raise ValueError(
                "Invalid task selected."
            )

        return render_home(
            request,
            result=result,
            task=task,
        )

    except Exception as exc:

        return render_home(
            request,
            task=task,
            error=str(exc),
        )


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "application": "EduGenie",
        "version": "1.0.0",
    }