import os
import re

from flask import Flask, render_template, request, make_response
from openai import OpenAI
from ddgs import DDGS

app = Flask(__name__)


# ============================================================
# GROQ
# ============================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY is not set.")
    exit()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


# ============================================================
# SEARCH
# ============================================================

def search_web(question):

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    question,
                    max_results=3
                )
            )

        return results

    except Exception as e:

        print("SEARCH ERROR:", e)

        return []


# ============================================================
# CLEAN ANSWER
# ============================================================

def clean_answer(text):

    text = re.sub(
        r"^#+\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    text = text.replace("**", "")
    text = text.replace("__", "")

    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    text = re.sub(
        r"https?://\S+",
        "",
        text
    )

    return text.strip()


# ============================================================
# AI ANSWER
# ============================================================

def generate_answer(question, sources):

    information = ""

    for source in sources:

        information += (
            source.get("body", "")
            + "\n"
        )

    prompt = f"""
You are a research assistant.

Question:
{question}

Web information:
{information}

Give a brief answer in 2 to 4 sentences.

Rules:
- Plain text only.
- No Markdown.
- No headings.
- No bullet points.
- No URLs.
- Do not repeat the question.
- Do not invent information.
"""

    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )

    return clean_answer(
        response.output_text
    )


# ============================================================
# FRESH HOME PAGE
# ============================================================

@app.route("/")
def home():

    response = make_response(
        render_template(
            "index.html",
            results=[]
        )
    )

    # Tell browser not to cache old page
    response.headers["Cache-Control"] = (
        "no-cache, no-store, must-revalidate"
    )

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response


# ============================================================
# RESEARCH
# ============================================================

@app.route(
    "/research",
    methods=["POST"]
)
def research():

    question_text = request.form.get(
        "questions",
        ""
    ).strip()

    questions = [

        q.strip()

        for q in question_text.splitlines()

        if q.strip()

    ]

    results = []

    print()
    print("=" * 60)
    print(
        "QUESTIONS RECEIVED:",
        len(questions)
    )
    print("=" * 60)


    for question in questions:

        print(
            "Searching:",
            question
        )

        sources = search_web(
            question
        )

        print(
            "Sources found:",
            len(sources)
        )


        if not sources:

            results.append({

                "question": question,

                "answer":
                    "No sources were found.",

                "sources": []

            })

            continue


        try:

            print(
                "Generating answer..."
            )

            answer = generate_answer(
                question,
                sources
            )

            print(
                "Answer generated."
            )

        except Exception as e:

            print(
                "GROQ ERROR:",
                e
            )

            answer = (
                "Unable to generate an answer."
            )


        clean_sources = []


        for source in sources:

            url = source.get(
                "href",
                ""
            )

            title = source.get(
                "title",
                "Web Source"
            )


            if url:

                clean_sources.append({

                    "title": title,

                    "url": url

                })


        results.append({

            "question":
                question,

            "answer":
                answer,

            "sources":
                clean_sources[:2]

        })


    print(
        "Research finished."
    )


    # Show results on the same frontend
    response = make_response(
        render_template(
            "index.html",
            results=results
        )
    )

    response.headers["Cache-Control"] = (
        "no-cache, no-store, must-revalidate"
    )

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
