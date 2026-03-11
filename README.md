# Amazon Insights AI

### Natural language analytics for Amazon product data - plain English in, SQL + visualization out, in under 11 seconds.

![Chat Interface](assets/screenshot_chat.png)

> 95% SQL accuracy · 10.7s avg response · dbt-modeled star schema · GPT-4o powered · FastAPI + Streamlit

---

## Problem

Amazon sellers and business analysts deal with hundreds of products across multiple categories but have no easy way to get answers from their data. Questions like "which category is driving the most value?" or "which products are most discounted?" require someone to open a SQL editor, write a query, run it, and then build a chart manually. That process takes 10 to 15 minutes per question and assumes SQL knowledge that most business stakeholders simply do not have.

---

## Solution

Amazon Insights AI cuts that down to under 10 seconds. Type a plain English question, get a verified SQL result, a written answer, and an automatically generated chart. No SQL knowledge required.

---

## Screenshots

**Chat Interface**

![Chat Interface](assets/screenshot_chat.png)

**Auto-Generated Chart**

![Chart](assets/screenshot_chart.png)

**SQL Transparency Panel**

![SQL Panel](assets/screenshot_sql.png)

---

## Architecture

Raw Amazon product data goes through a Python ETL pipeline where it gets cleaned and loaded into a PostgreSQL star schema. A LangChain SQL agent powered by GPT-4o takes natural language questions and converts them into validated SQL queries. A second GPT-4o call then looks at the query intent and result shape and decides what kind of chart to render. Everything gets served through a FastAPI backend and displayed in a Streamlit chat interface.

---

## How This Differs From Tutorial Text-to-SQL Projects

Most LangChain Text-to-SQL projects connect an LLM to a database, run a query, and return text. This project goes further in a few meaningful ways.

The data engineering layer is real. The raw dataset was a messy flat CSV with currency symbols in price columns, pipe-separated category hierarchies, and duplicate product entries. A proper ETL pipeline was built to clean all of it and normalize it into a star schema with engineered metrics.

The dbt layer makes it production-grade. All transformations live in dbt models with a staging layer and a marts layer. Every column is documented in schema.yml and 12 data quality tests run against the tables. This is how analytics engineering teams actually build and govern metrics in production.

Charts are not an afterthought. A dedicated second GPT-4o call analyzes the query intent and result shape and decides whether a bar, line, scatter, or pie chart is appropriate. Most tutorial projects return text only.

The accuracy numbers are real. 20 test questions were run and manually verified against direct PostgreSQL queries. The benchmark table in this README reflects actual measured results, not estimates.

The architecture is modular. ETL, dbt models, LangChain agent, chart agent, chart renderer, FastAPI backend, and Streamlit frontend are all separate modules. Most tutorial projects run everything in a single script.

---

## Data Model

Raw flat CSV normalized into a PostgreSQL star schema - one fact table (pricing, ratings, discounts, value_score) and two dimension tables (products, categories). Category hierarchy parsed from pipe-delimited strings into five structured levels.

---

## Features

**Natural Language to SQL** - GPT-4o generates and executes SQL queries from plain-English questions using a ReAct agent loop that validates queries before execution.

**Automatic Chart Generation** - A dedicated GPT-4o call decides whether a bar, line, scatter, or pie chart fits the result. Charts render using Plotly with a dark analytics theme.

**SQL Transparency Panel** - Every response includes a collapsible panel showing the exact SQL query that was generated and run. Analysts can verify every answer.

**Query Safety Guardrails** - The agent is instructed to never run DROP, DELETE, UPDATE, or INSERT. All queries are read-only.

**Star Schema Modeling** - Raw flat data was normalized into fact and dimension tables with a five-level category hierarchy parsed from a pipe-delimited field.

**dbt Analytics Layer** - Transformations are defined as dbt models across staging and marts layers. 12 data quality tests cover not_null and unique constraints across all tables.

---

## Query Accuracy Benchmark

20 test questions were run against the platform and evaluated manually for SQL correctness and answer accuracy.

| Question Type | Accuracy | Avg Response Time |
|---|---|---|
| Single aggregations (AVG, SUM, COUNT) | 100% | 8.75s |
| Multi-table joins | 100% | 12.25s |
| Category hierarchy filters | 75% | 14.1s |
| Top-N rankings | 100% | 10.5s |
| Correlation and distribution queries | 100% | 8.3s |
| **Overall** | **95%** | **10.7s** |

The one failed case was an ambiguous "average price" question where the agent picked actual_price instead of discounted_price. This is a known limitation of natural language ambiguity in pricing queries.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Data Processing | pandas, SQLAlchemy, psycopg2 |
| Analytics Engineering | dbt-core, dbt-postgres |
| AI and Agents | LangChain, LangGraph, OpenAI GPT-4o |
| Database | PostgreSQL 15 |
| Backend | FastAPI, Uvicorn, Pydantic |
| Frontend | Streamlit |
| Visualization | Plotly Express |
| Infrastructure | Docker, Docker Compose |

---

## Sample Questions

- Which product category has the highest average discount?
- What are the top 10 products by value score?
- Show average discount percentage by top level category
- What is the relationship between discount percentage and rating?
- Which category has the best average rating?
- What is the average savings across all products?
- Show product count by top level category
- What percentage of products have a discount above 50%?
- Which product has the highest savings amount?
- What is the distribution of ratings across all products?

---

## Setup Instructions

**Step 1 - Clone the repository and create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Step 2 - Create a .env file in the project root**
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://analyst:analyst123@127.0.0.1:5433/amazon_insights
```

**Step 3 - Start PostgreSQL using Docker**
```bash
docker-compose up -d
```

**Step 4 - Run the ETL pipeline**
```bash
python etl/clean_and_load.py
```

**Step 5 - Start the FastAPI backend**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Step 6 - Start the Streamlit frontend**
```bash
streamlit run frontend/app.py
```

**Step 7 - Optional: Run dbt models and tests**
```bash
cd analytics_layer
dbt run
dbt test
```

---

## Dataset

Amazon Sales Dataset with 1,465 products across 9 top-level categories including Electronics, Computers and Accessories, and Home and Kitchen. Source: Kaggle. The dataset is not included in this repository. Download it from Kaggle and place it in the data/ folder before running the ETL pipeline.

This project is scoped to 1,465 products for demonstration purposes. The dbt models, star schema, and FastAPI architecture follow the same patterns used in production environments handling 100M+ record datasets.