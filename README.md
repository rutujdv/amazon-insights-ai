# Amazon Insights AI

A natural language analytics platform that converts plain-English questions into SQL queries, executes them against a PostgreSQL database, and automatically generates Plotly visualizations powered by GPT-4o and LangChain.

---

## Architecture

Raw CSV data is ingested through an ETL pipeline, cleaned, and loaded into a PostgreSQL star schema. A LangChain SQL agent powered by GPT-4o converts natural language questions into SQL queries. Query results are passed to a chart decision engine that selects the appropriate visualization type and renders interactive Plotly charts. The backend is served via FastAPI and the frontend is built with Streamlit.

---

## Database Schema

The raw Amazon dataset was normalized from a flat CSV into a star schema with the following tables.

**fct_product_metrics** stores discounted_price, actual_price, discount_percentage, rating, rating_count, savings, and value_score.

**dim_products** stores product_id, product_name, about_product, img_link, and product_link.

**dim_categories** stores category_id, category_l1, category_l2, category_l3, category_l4, and category_l5.

value_score is a computed metric defined as rating multiplied by rating_count, representing weighted product popularity.

---

## Features

**Natural Language to SQL** — Users ask questions in plain English. GPT-4o generates and executes the corresponding SQL query against the PostgreSQL database.

**Automatic Chart Generation** — A secondary GPT-4o call analyzes the query intent and result shape to decide whether a chart is needed and which type to render: bar, line, scatter, or pie.

**SQL Transparency Panel** — Every response includes a collapsible panel showing the exact SQL query that was generated and executed.

**Query Safety Guardrails** — The agent is instructed to never execute destructive operations including DROP, DELETE, UPDATE, or INSERT.

**Star Schema Modeling** — Raw flat data was normalized into fact and dimension tables, following analytics engineering best practices.

---

## Tech Stack

**Language** — Python 3.10

**Data Processing** — pandas, SQLAlchemy, psycopg2

**AI and Agents** — LangChain, LangGraph, OpenAI GPT-4o

**Database** — PostgreSQL 15

**Backend** — FastAPI, Uvicorn

**Frontend** — Streamlit

**Visualization** — Plotly Express

**Infrastructure** — Docker

---

## Sample Questions

- Which product category has the highest average discount?
- What are the top 10 products by value score?
- Show average discount percentage by top level category
- What is the relationship between discount percentage and rating?
- Which category has the best average rating?
- What is the average savings across all products?
- Show product count by top level category

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

---

## Dataset

Amazon Sales Dataset containing 1,465 products across 9 top-level categories including Electronics, Computers and Accessories, and Home and Kitchen. Source: Kaggle.