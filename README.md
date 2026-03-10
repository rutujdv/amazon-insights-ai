# Amazon Insights AI

### Natural language analytics for Amazon product data — plain English in, SQL + visualization out, in under 11 seconds.

![Chat Interface](assets/screenshot_chat.png)

> 95% SQL accuracy · 10.7s avg response · dbt-modeled star schema · GPT-4o powered · FastAPI + Streamlit

---

## Problem

Amazon sellers and business analysts manage hundreds of SKUs but lack accessible analytics. Answering basic business questions like "which products are underperforming?" or "which category drives the most value?" requires writing SQL queries that most stakeholders do not have time for. Existing tools are either too technical or too rigid for teams that need fast, ad-hoc insights.

---

## Solution

Reduces analyst time-to-insight from 15 minutes of manual SQL querying to under 10 seconds — no SQL knowledge required. A self-serve natural language analytics platform that converts plain-English business questions into SQL, executes them against a structured product database, and automatically generates the right visualization.

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

Raw Amazon product data is ingested through a Python ETL pipeline, cleaned, and modeled into a PostgreSQL star schema following analytics engineering best practices. A LangChain SQL agent powered by GPT-4o converts natural language questions into validated SQL queries. A secondary GPT-4o call acts as a chart decision engine, selecting the appropriate visualization type based on query intent and result shape. Results are served through a FastAPI backend and rendered in a Streamlit conversational interface.

---

## How This Differs From Tutorial Text-to-SQL Projects

Most LangChain Text-to-SQL projects query an existing flat table and return text. This project goes further in five ways.

**Raw messy CSV to star schema** — The dataset required real ETL work: stripping currency symbols, parsing a pipe-delimited five-level category hierarchy, deduplicating products, and computing engineered metrics. Most tutorial projects start with a pre-cleaned table.

**dbt staging and marts layer** — All transformations are defined as dbt models with a staging layer and a marts layer. A schema.yml file documents every column and enforces 12 data quality tests. This is how analytics engineering teams actually build and govern metrics.

**Dedicated chart decision engine** — A second GPT-4o call analyzes query intent and result shape to decide whether a chart is needed and which type to render. Most projects return text only.

**Benchmarked accuracy** — 20 test questions were run and manually verified against direct PostgreSQL queries. The accuracy and response time numbers in this README are real measured results, not estimates.

**Separated architecture** — ETL, dbt models, LangChain agent, chart agent, chart renderer, FastAPI backend, and Streamlit frontend are all separate modules with clear responsibilities. Most tutorial projects run everything in a single script.

---

## Database Schema

The raw dataset was normalized from a flat CSV into a star schema with three tables.

**fct_product_metrics** — discounted_price, actual_price, discount_percentage, rating, rating_count, savings, value_score

**dim_products** — product_id, product_name, about_product, img_link, product_link

**dim_categories** — category_id, category_l1, category_l2, category_l3, category_l4, category_l5

value_score is an engineered metric defined as rating multiplied by rating_count, representing weighted product popularity and used as the primary ranking signal across the platform.

---

## Features

**Natural Language to SQL** — GPT-4o generates and executes SQL queries from plain-English questions, with a ReAct agent loop that validates queries before execution.

**Automatic Chart Generation** — A dedicated GPT-4o call analyzes query intent and result shape to decide whether a bar, line, scatter, or pie chart is appropriate. Charts are rendered using Plotly with a dark analytics theme.

**SQL Transparency Panel** — Every response includes a collapsible panel showing the exact SQL query generated, enabling analyst review and trust in AI-generated results.

**Query Safety Guardrails** — The agent is explicitly instructed to never execute DROP, DELETE, UPDATE, or INSERT statements. All queries are read-only.

**Star Schema Modeling** — Raw flat data was normalized into fact and dimension tables following analytics engineering conventions, with a five-level category hierarchy parsed from a pipe-delimited field.

**dbt Analytics Layer** — All transformations are defined as dbt models with a staging and marts layer. 12 data quality tests cover not_null and unique constraints across all tables.

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

Note: The one failed case involved an ambiguous "average price" query where the agent used actual_price instead of discounted_price. This reflects a known limitation of natural language ambiguity in pricing queries.

---

## Tech Stack

**Language** — Python 3.10

**Data Processing** — pandas, SQLAlchemy, psycopg2

**Analytics Engineering** — dbt-core, dbt-postgres

**AI and Agents** — LangChain, LangGraph, OpenAI GPT-4o

**Database** — PostgreSQL 15

**Backend** — FastAPI, Uvicorn, Pydantic

**Frontend** — Streamlit

**Visualization** — Plotly Express

**Infrastructure** — Docker, Docker Compose

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

**Step 1 — Clone the repository and create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Step 2 — Create a .env file in the project root**
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://analyst:analyst123@127.0.0.1:5433/amazon_insights
```

**Step 3 — Start PostgreSQL using Docker**
```bash
docker-compose up -d
```

**Step 4 — Run the ETL pipeline**
```bash
python etl/clean_and_load.py
```

**Step 5 — Start the FastAPI backend**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Step 6 — Start the Streamlit frontend**
```bash
streamlit run frontend/app.py
```

**Step 7 — Optional: Run dbt models and tests**
```bash
cd analytics_layer
dbt run
dbt test
```

---

## Dataset

Amazon Sales Dataset — 1,465 products across 9 top-level categories including Electronics, Computers and Accessories, and Home and Kitchen. Source: Kaggle. The dataset was not pushed to this repository. Download it from Kaggle and place it in the data/ folder before running the ETL pipeline.

Dataset is scoped to 1,465 products for demonstration. The dbt models, star schema, and FastAPI architecture follow the same patterns used in production environments handling 100M+ record datasets.