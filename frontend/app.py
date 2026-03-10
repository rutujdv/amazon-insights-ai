import streamlit as st
import requests
import plotly.io as pio
import json

st.set_page_config(
    page_title="Amazon Insights AI",
    page_icon="📦",
    layout="wide"
)

st.markdown("## Amazon Insights AI")
st.caption("Ask plain-English questions about 1,465 Amazon products — powered by GPT-4o + PostgreSQL")
st.divider()

with st.expander("Try these questions"):
    st.markdown("""
    - Which product category has the highest average discount?
    - What are the top 10 products by value score?
    - Show me products with rating above 4.5 and more than 10,000 reviews
    - Which category has the best average rating?
    - What is the average savings across all Electronics products?
    - Show me the distribution of ratings across Home and Kitchen
    """)

if "history" not in st.session_state:
    st.session_state.history = []

question = st.chat_input("Ask anything about the Amazon product data...")

if question:
    with st.spinner("Generating SQL and analyzing..."):
        try:
            res  = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question},
                timeout=180
            )
            data = res.json()
            st.session_state.history.append(data)
        except Exception as e:
            st.error(f"Backend error: {e}")

for item in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.write(item["question"])

    with st.chat_message("assistant"):
        st.write(item["answer"])

        if item.get("chart"):
            fig = pio.from_json(json.dumps(item["chart"]))
            st.plotly_chart(fig, use_container_width=True)
            if item.get("chart_reasoning"):
                st.caption(f"Chart rationale: {item['chart_reasoning']}")

        col1, col2 = st.columns([1, 1])
        with col1:
            if item.get("sql_generated"):
                with st.expander("View generated SQL"):
                    st.code(item["sql_generated"], language="sql")
        with col2:
            if item.get("row_count"):
                st.caption(f"{item['row_count']} rows returned")