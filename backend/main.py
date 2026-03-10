import os
import json
import plotly
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.agent import build_agent, run_query_with_data
from backend.chart_agent import decide_chart
from backend.chart_renderer import render_chart

load_dotenv()

app = FastAPI(title="Amazon Insights AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

agent = build_agent()

class Query(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok", "project": "Amazon Insights AI"}

@app.post("/ask")
async def ask(query: Query):
    result   = run_query_with_data(agent, query.question)
    answer   = result["answer"]
    raw_data = result["data"]

    chart_decision = decide_chart(query.question, answer, raw_data)

    chart_json = None
    if chart_decision.get("needs_chart") and raw_data:
        fig = render_chart(chart_decision, raw_data)
        if fig:
            chart_json = json.loads(plotly.io.to_json(fig))

    return {
        "question":        query.question,
        "answer":          answer,
        "chart":           chart_json,
        "chart_reasoning": chart_decision.get("reasoning"),
        "sql_generated":   result.get("sql"),
        "row_count":       len(raw_data)
    }