import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = ["#0EA5E9", "#6366F1", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
DARK_BG = "#0f1117"
FONT_COLOR = "#e2e8f0"

def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor=DARK_BG, paper_bgcolor=DARK_BG,
        font=dict(color=FONT_COLOR, family="IBM Plex Mono"),
        title=dict(font=dict(size=17, color="#f8fafc"), x=0.02),
        margin=dict(l=50, r=30, t=65, b=50),
        height=430
    )
    fig.update_xaxes(gridcolor="#1e293b", tickcolor="#475569")
    fig.update_yaxes(gridcolor="#1e293b", tickcolor="#475569")
    return fig

def render_chart(decision: dict, data: list) -> go.Figure | None:
    if not decision.get("needs_chart") or not data:
        return None

    df = pd.DataFrame(data)
    ct    = decision["chart_type"]
    x     = decision["x_column"]
    y     = decision["y_column"]
    title = decision["title"]

    if df[x].dtype == object:
        df[x] = df[x].str[:35]

    if ct == "bar":
        df = df.sort_values(y, ascending=False).head(15)
        fig = px.bar(df, x=x, y=y, title=title,
                     color_discrete_sequence=COLORS, template="plotly_dark")
        fig.update_layout(xaxis_tickangle=-35)

    elif ct == "line":
        fig = px.line(df, x=x, y=y, title=title,
                      color_discrete_sequence=["#0EA5E9"],
                      markers=True, template="plotly_dark")
        fig.update_traces(line=dict(width=2.5),
                          marker=dict(size=7, color="#38bdf8"))

    elif ct == "pie":
        df = df.head(6)
        fig = px.pie(df, names=x, values=y, title=title,
                     color_discrete_sequence=COLORS, template="plotly_dark")
        fig.update_traces(textposition="inside", textinfo="percent+label")

    elif ct == "scatter":
        fig = px.scatter(df, x=x, y=y, title=title,
                         color_discrete_sequence=["#6366F1"],
                         template="plotly_dark", trendline="ols",
                         hover_data=df.columns.tolist()[:4])
    else:
        return None

    return apply_dark_theme(fig)