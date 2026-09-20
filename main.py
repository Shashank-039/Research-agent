from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

import research_agent


app = FastAPI(
    title="AI Research Agent"
)


templates = Jinja2Templates(
    directory="templates"
)


@app.get("/")
def home(request: Request):

    context = {
        "request": request,
        "question": "",
        "result": None
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context
    )


@app.post("/research")
def run_research(
    request: Request,
    question: str = Form(...)
):

    question = question.strip()

    if not question:

        result = {
            "success": False,
            "title": "No Question",
            "answer": "Please enter a research question.",
            "source": ""
        }

    else:

        result = research_agent.research(
            question
        )

    context = {
        "request": request,
        "question": question,
        "result": result
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context
    )