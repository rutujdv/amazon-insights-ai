import os
import pandas as pd
from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SYSTEM_PROMPT = """You are Amazon Insights AI, an expert e-commerce data analyst.
You have access to a PostgreSQL database with Amazon product data.

The database has exactly 3 tables:

1. fct_product_metrics (product_id, category_id, discounted_price, actual_price, discount_percentage, rating, rating_count, savings, value_score)
2. dim_products (product_id, product_name, about_product, img_link, product_link)
3. dim_categories (category_id, category_l1, category_l2, category_l3, category_l4, category_l5)

JOIN rules:
- fct_product_metrics JOIN dim_products ON fct_product_metrics.product_id = dim_products.product_id
- fct_product_metrics JOIN dim_categories ON fct_product_metrics.category_id = dim_categories.category_id

For category questions, group by category_l1 for top-level categories.
value_score = rating x rating_count.
savings = actual_price - discounted_price in Indian Rupees.
For top products, order by value_score DESC.
Never run DROP, DELETE, UPDATE or INSERT.
Always write and run the SQL query directly without markdown formatting.
"""

def build_agent():
    db = SQLDatabase.from_uri(
        DATABASE_URL,
        include_tables=["fct_product_metrics", "dim_products", "dim_categories"],
        sample_rows_in_table_info=2
    )
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    return agent

def run_query_with_data(agent, question: str) -> dict:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})

    answer = result["messages"][-1].content
    sql_query = None
    raw_data = []

    for message in result["messages"]:
        # Tool messages contain the raw SQL results
        if hasattr(message, "name") and message.name == "sql_db_query":
            # Get the SQL from the preceding tool call
            pass
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.get("name") == "sql_db_query":
                    sql_query = tool_call.get("args", {}).get("query")
                    if sql_query:
                        try:
                            with engine.connect() as conn:
                                df = pd.read_sql(text(sql_query), conn)
                                raw_data = df.to_dict(orient="records")
                        except Exception:
                            pass

    return {"answer": answer, "sql": sql_query, "data": raw_data}