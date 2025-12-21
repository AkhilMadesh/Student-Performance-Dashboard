import dash
from dash import dcc, html, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import requests

app = dash.Dash(__name__)

# ---------------- DATA ----------------
def load_data():
    try:
        r = requests.get("http://127.0.0.1:5000/students")
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

# ---------------- LAYOUT ----------------
app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #667eea, #764ba2)",
        "padding": "30px",
        "fontFamily": "Segoe UI"
    },
    children=[

        html.H1(
            "Student Performance Dashboard",
            style={
                "textAlign": "center",
                "color": "white",
                "marginBottom": "30px"
            }
        ),

        # Graph selector
        html.Div(
            style={
                "background": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 10px rgba(0,0,0,0.15)",
                "marginBottom": "20px"
            },
            children=[
                dcc.Dropdown(
                    id="graph_selector",
                    options=[
                        {"label": "📊 Combined Bar (All Students)", "value": "combined"},
                        {"label": "👤 Student-wise Bar", "value": "student"},
                        {"label": "🥧 Subject-wise Pie", "value": "pie"},
                        {"label": "📈 Subject-wise Line", "value": "line"},
                        {"label": "📋 Marks Table", "value": "table"}
                    ],
                    value="combined",
                    style={"borderRadius": "8px"}
                ),

                html.Br(),

                dcc.Dropdown(
                    id="student_filter",
                    placeholder="Select Student (for student-wise graph)",
                    style={"borderRadius": "8px"}
                )
            ]
        ),

        # Graph sections
        html.Div(dcc.Graph(id="combined_bar"), id="combined_div"),
        html.Div(dcc.Graph(id="student_bar"), id="student_div"),
        html.Div(dcc.Graph(id="subject_pie"), id="pie_div"),
        html.Div(dcc.Graph(id="subject_line"), id="line_div"),

        # Table section
        html.Div(
            id="table_div",
            style={
                "background": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 10px rgba(0,0,0,0.15)"
            },
            children=[
                html.H3("📋 Complete Marks Table"),
                dash_table.DataTable(
                    id="marks_table",
                    columns=[
                        {"name": "Name", "id": "name"},
                        {"name": "Subject", "id": "subject"},
                        {"name": "Marks", "id": "marks"}
                    ],
                    style_cell={
                        "textAlign": "center",
                        "padding": "10px"
                    },
                    style_header={
                        "backgroundColor": "#667eea",
                        "color": "white",
                        "fontWeight": "bold"
                    },
                    style_table={"overflowX": "auto"}
                )
            ]
        )
    ]
)

# ---------------- CALLBACK ----------------
@app.callback(
    Output("student_filter", "options"),
    Output("combined_bar", "figure"),
    Output("student_bar", "figure"),
    Output("subject_pie", "figure"),
    Output("subject_line", "figure"),
    Output("marks_table", "data"),

    Output("combined_div", "style"),
    Output("student_div", "style"),
    Output("pie_div", "style"),
    Output("line_div", "style"),
    Output("table_div", "style"),

    Input("graph_selector", "value"),
    Input("student_filter", "value")
)
def update_dashboard(graph_type, student):
    df = load_data()

    hide = {"display": "none"}
    show = {"display": "block"}

    if df.empty:
        return [], {}, {}, {}, {}, [], hide, hide, hide, hide, hide

    student_options = [
        {"label": s, "value": s}
        for s in sorted(df["name"].unique())
    ]

    combined_bar = px.bar(
        df, x="name", y="marks", color="subject",
        title="All Students – Subject-wise Marks",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    if student:
        df_student = df[df["name"] == student]
        student_bar = px.bar(
            df_student, x="subject", y="marks",
            title=f"{student}'s Performance",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    else:
        student_bar = {}

    pie_df = df.groupby("subject")["marks"].mean().reset_index()
    subject_pie = px.pie(
        pie_df, names="subject", values="marks",
        title="Average Marks by Subject",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    subject_line = px.line(
        pie_df, x="subject", y="marks",
        title="Subject-wise Performance Trend",
        markers=True
    )

    styles = {
        "combined": (show, hide, hide, hide, hide),
        "student": (hide, show, hide, hide, hide),
        "pie": (hide, hide, show, hide, hide),
        "line": (hide, hide, hide, show, hide),
        "table": (hide, hide, hide, hide, show)
    }

    return (
        student_options,
        combined_bar,
        student_bar,
        subject_pie,
        subject_line,
        df.to_dict("records"),
        *styles[graph_type]
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
