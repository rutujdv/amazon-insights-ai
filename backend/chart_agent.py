import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def decide_chart(question: str, answer: str, data: list) -> dict:
    if not data or len(data) < 2:
        return {"needs_chart": False}

    columns = list(data[0].keys()) if data else []

    prompt = f"""
You are a data visualization expert for an e-commerce analytics platform.

User question: {question}
Answer: {answer}
Data columns available: {columns}
Sample data (2 rows): {json.dumps(data[:2], default=str)}
Total rows: {len(data)}

Decide if a Plotly chart would help. Respond ONLY with JSON:
{{
  "needs_chart": true or false,
  "chart_type": "bar" | "line" | "pie" | "scatter",
  "x_column": "exact column name",
  "y_column": "exact column name",
  "title": "Chart title",
  "reasoning": "why this chart type"
}}

Rules:
- bar: rankings, category comparisons, top-N lists
- line: trends over time or ordered sequence
- pie: share or proportion with max 6 items only
- scatter: correlation between 2 numeric columns
- needs_chart false for single numbers, yes or no answers, or text-only results
- x_column and y_column MUST exactly match one of: {columns}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )
    result = json.loads(response.choices[0].message.content)

    if result.get("needs_chart"):
        if result.get("x_column") not in columns or result.get("y_column") not in columns:
            result["needs_chart"] = False

    return result