import os
from openai import OpenAI
from ddgs import DDGS

# Groq setup
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Groq API key not found.")
    exit()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


# Search web
def search_web(question):

    with DDGS() as ddgs:
        results = list(
            ddgs.text(
                question,
                max_results=3
            )
        )

    return results


# Generate short answer
def generate_answer(question, results):

    source_info = ""

    for result in results:

        source_info += (
            result.get("body", "")
            + "\n"
        )

    prompt = f"""
Answer this question briefly:

{question}

Use this information:

{source_info}

Rules:
- Give only 2 to 4 sentences.
- Use simple language.
- Give a direct answer.
- Do not add a Sources section.
- Do not include URLs.
"""

    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )

    return response.output_text


# ============================================================
# PROGRAM
# ============================================================

print("=" * 60)
print("             SIMPLE RESEARCH AGENT")
print("=" * 60)

print()
print("Enter your questions.")
print("Type DONE when you are finished.")
print()

questions = []

while True:

    question = input("Question: ").strip()

    if question.lower() == "done":
        break

    if question:
        questions.append(question)


if not questions:

    print("No questions entered.")
    exit()


# ============================================================
# RESEARCH
# ============================================================

for number, question in enumerate(questions, 1):

    print()
    print("=" * 60)
    print(f"QUESTION {number}")
    print("=" * 60)

    print(question)
    print()
    print("Searching...")

    try:

        results = search_web(question)

        if not results:
            print("No source found.")
            continue

        answer = generate_answer(
            question,
            results
        )

        print()
        print("ANSWER:")
        print(answer)

        # Show source links immediately
        print()
        print("SOURCE:")

        for result in results[:2]:

            print(result.get("href", ""))

    except Exception as e:

        print("Error:", e)


print()
print("=" * 60)
print("DONE")
print("=" * 60)
