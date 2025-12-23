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
            "🎓 B.Tech CSE Student Performance Dashboard",
            style={"textAlign": "center", "color": "white"}
        ),

        # -------- ADD / DELETE SECTION --------
        html.Div(
            style={
                "background": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "20px"
            },
            children=[
                html.H3("➕ Add Student Record"),

                dcc.Input(id="add_name", placeholder="Name", type="text"),
                dcc.Input(id="add_subject", placeholder="Subject", type="text"),
                dcc.Input(id="add_marks", placeholder="Marks", type="number"),
                html.Button("Add", id="add_btn", n_clicks=0),

                html.Hr(),

                html.H3("🗑 Delete Student Record"),

                dcc.Input(id="del_name", placeholder="Name", type="text"),
                dcc.Input(id="del_subject", placeholder="Subject", type="text"),
                html.Button("Delete", id="del_btn", n_clicks=0),

                html.Div(id="action_msg", style={"marginTop": "10px", "color": "green"})
            ]
        ),

        # -------- GRAPH SELECTOR --------
        html.Div(
            style={
                "background": "white",
                "padding": "20px",
                "borderRadius": "12px",
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
                    value="combined"
                ),

                html.Br(),

                dcc.Dropdown(
                    id="student_filter",
                    placeholder="Select Student (for student-wise graph)"
                )
            ]
        ),

        # -------- VISUALS --------
        html.Div(dcc.Graph(id="combined_bar"), id="combined_div"),
        html.Div(dcc.Graph(id="student_bar"), id="student_div"),
        html.Div(dcc.Graph(id="subject_pie"), id="pie_div"),
        html.Div(dcc.Graph(id="subject_line"), id="line_div"),

        html.Div(
            id="table_div",
            style={"background": "white", "padding": "20px", "borderRadius": "12px"},
            children=[
                html.H3("📋 Complete Marks Table"),
                dash_table.DataTable(
                    id="marks_table",
                    columns=[
                        {"name": "Name", "id": "name"},
                        {"name": "Subject", "id": "subject"},
                        {"name": "Marks", "id": "marks"}
                    ],
                    style_cell={"textAlign": "center"},
                    style_header={
                        "backgroundColor": "#667eea",
                        "color": "white",
                        "fontWeight": "bold"
                    }
                )
            ]
        )
    ]
)

# ---------------- MAIN CALLBACK ----------------
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

    student_options = [{"label": s, "value": s} for s in sorted(df["name"].unique())]

    combined_bar = px.bar(
        df, x="name", y="marks", color="subject",
        title="All Students – Subject-wise Marks"
    )

    if student:
        df_student = df[df["name"] == student]
        student_bar = px.bar(
            df_student, x="subject", y="marks",
            title=f"{student}'s Performance"
        )
    else:
        student_bar = {}

    pie_df = df.groupby("subject")["marks"].mean().reset_index()
    subject_pie = px.pie(
        pie_df, names="subject", values="marks",
        title="Average Marks by Subject"
    )

    subject_line = px.line(
        pie_df, x="subject", y="marks",
        title="Subject-wise Performance Trend", markers=True
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

# ---------------- ADD / DELETE CALLBACK ----------------
@app.callback(
    Output("action_msg", "children"),
    Input("add_btn", "n_clicks"),
    Input("del_btn", "n_clicks"),
    Input("add_name", "value"),
    Input("add_subject", "value"),
    Input("add_marks", "value"),
    Input("del_name", "value"),
    Input("del_subject", "value"),
    prevent_initial_call=True
)
def modify_data(add_clicks, del_clicks,
                add_name, add_subject, add_marks,
                del_name, del_subject):

    ctx = dash.callback_context
    button = ctx.triggered[0]["prop_id"].split(".")[0]

    if button == "add_btn" and add_name and add_subject and add_marks is not None:
        requests.post(
            "http://127.0.0.1:5000/add_student",
            json={"name": add_name, "subject": add_subject, "marks": add_marks}
        )
        return "✅ Student added successfully"

    if button == "del_btn" and del_name and del_subject:
        requests.post(
            "http://127.0.0.1:5000/delete_student",
            json={"name": del_name, "subject": del_subject}
        )
        return "🗑 Student record deleted"

    return "⚠️ Please fill all fields correctly"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
