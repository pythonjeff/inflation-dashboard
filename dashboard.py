import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
from dash_extensions.enrich import DashProxy, ServersideOutputTransform
import dash.exceptions
import pandas as pd

# Load inflation & policy data
inflation_df = pd.read_csv("data/inflation_data.csv", index_col=0, parse_dates=True)
policy_df = pd.read_csv("data/policy_data.csv", index_col=0, parse_dates=True)

# Define the start dates for each presidency
PRESIDENTIAL_TERMS = {
    "Obama (2009 - 2012)": ("2009-01-01", "2013-12-01"),
    "Obama (2013 - 2016)": ("2013-01-01", "2017-12-01"),
    "Trump (2017 - 2020)": ("2017-01-01", "2021-12-01"),
    "Biden (2021 - 2024)": ("2021-01-01", "2024-12-01")  # Future date assumed
}

def filter_term_data(start_date, end_date, column, dataset):
    """Filters inflation or policy data for a specific presidential term."""
    df = inflation_df if dataset == "inflation" else policy_df
    if end_date == "Present":
        return df.loc[start_date:, column]
    return df.loc[start_date:end_date, column]

def make_line_chart(series, chart_title, yaxis_label):
    """Creates a standard line chart with consistent formatting."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series.index,
            y=series,
            mode="lines",
            name=chart_title
        )
    )
    fig.update_layout(
        title=chart_title,
        xaxis_title="Year",
        yaxis_title=yaxis_label,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_cpi_percent_change_number(president):
    """
    Returns the overall percent change in CPI (start to end of term) as a string
    with a '+' or '−' sign. E.g., '+3.45%' or '-2.10%'.
    """
    start, end = PRESIDENTIAL_TERMS[president]
    cpi_data = filter_term_data(start, end, "CPI", dataset="inflation")
    
    if cpi_data.empty or len(cpi_data) < 2:
        return "N/A"

    start_val = cpi_data.iloc[0]
    end_val = cpi_data.iloc[-1]
    percent_change = (end_val / start_val - 1) * 100

    if percent_change > 0:
        return f"+{percent_change:.2f}%"
    elif percent_change < 0:
        return f"{percent_change:.2f}%"
    else:
        return "0.00%"

def create_term_chart(indicator_name, president, dataset="policy"):
    """
    Creates a line chart for a specific economic indicator for a president's term.
    """
    start, end = PRESIDENTIAL_TERMS[president]
    term_data = filter_term_data(start, end, indicator_name, dataset=dataset)
    title = f"{indicator_name} During {president}"
    return make_line_chart(term_data, chart_title=title, yaxis_label=indicator_name)

# Initialize Dash app
app = DashProxy(__name__, external_stylesheets=[dbc.themes.MORPH], transforms=[ServersideOutputTransform()])

def create_president_card(president):
    """
    Creates a flippable card for a president with:
    - President name on both front and back
    - Minimize button on the back to flip back
    """
    return dbc.Card(
        [
            # Front side
            dbc.CardBody(
                html.Div(
                    [
                        html.H4(president, className="text-center", style={"color": "#2A2A2A"}),
                        html.P("Click this card to see data", className="text-center"),
                    ],
                    id=f"{president}-front",
                    style={"cursor": "pointer"}
                ),
                style={"backgroundColor": "#FFFFFF", "textAlign": "center"}
            ),

            # Back side
            dbc.CardBody(
                html.Div(
                    [
                        # President's name again
                        html.H4(president, style={"color": "#2A2A2A"}),
                        
                        # Minimize button to flip back
                        dbc.Button(
                            "Minimize", 
                            id=f"{president}-close", 
                            color="primary", 
                            style={"marginBottom": "20px"}
                        ),
                        
                        html.H5("CPI Percent Change Over This Term:", style={"color": "#2A2A2A"}),
                        html.H2(
                            create_cpi_percent_change_number(president),
                            style={
                                "fontWeight": "bold",
                                "marginBottom": "20px",
                                "color": "#BA0C2F"
                            }
                        ),
                        html.Hr(),
                        
                        dcc.Graph(figure=create_term_chart("PPI", president, dataset="inflation")),
                        dcc.Graph(figure=create_term_chart("Unemployment Rate", president, dataset="policy")),
                        dcc.Graph(figure=create_term_chart("Fed Funds Rate", president, dataset="policy")),
                        dcc.Graph(figure=create_term_chart("30-Year Mortgage Rate", president, dataset="policy")),
                        dcc.Graph(figure=create_term_chart("Government Spending", president, dataset="policy")),
                    ]
                ),
                id=f"{president}-back",
                style={"display": "none", "backgroundColor": "#FFFFFF"}
            ),
        ],
        className="flip-card",
        style={
            "border": "3px solid #BA0C2F",
            "boxShadow": "0 0 10px rgba(0,0,0,0.3)",
            "borderRadius": "8px",
            "overflow": "hidden"
        }
    )

# Layout
app.layout = dbc.Container(
    [
        html.H1(
            "Interactive Inflation & Policy Dashboard",
            className="text-center mb-4",
            style={"color": "#FFFFFF", "textShadow": "2px 2px #000000"}
        ),

        # SINGLE ROW: each president card side-by-side for easier comparison
        dbc.Row(
            [
                dbc.Col(create_president_card(p), width=3)
                for p in PRESIDENTIAL_TERMS.keys()
            ],
            justify="center",
            className="g-4"
        ),
    ],
    fluid=True,
    style={
        # Simple gradient background
        "background": "linear-gradient(to bottom right, #E8F0FA, #FFFFFF)",
        "minHeight": "100vh",
        "paddingBottom": "50px",
        "overflowY": "auto"
    }
)

# Callback to handle flipping & minimizing
for president in PRESIDENTIAL_TERMS.keys():
    def make_flip_callback(president_name):
        @app.callback(
            [
                Output(f"{president_name}-front", "style"),
                Output(f"{president_name}-back", "style")
            ],
            [
                Input(f"{president_name}-front", "n_clicks"),  # Clicking front expands
                Input(f"{president_name}-close", "n_clicks")   # Clicking 'Minimize' on back
            ],
            prevent_initial_call=True
        )
        def flip_card(front_clicks, close_clicks):
            # In case neither is clicked yet
            if front_clicks is None and close_clicks is None:
                raise dash.exceptions.PreventUpdate

            # Determine which input triggered the callback
            triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

            if triggered_id == f"{president_name}-front":
                # "Expand": Hide front, show back
                return {"display": "none"}, {"display": "block"}
            elif triggered_id == f"{president_name}-close":
                # "Minimize": Show front, hide back
                return {"display": "block"}, {"display": "none"}

            # Default case
            raise dash.exceptions.PreventUpdate

        return flip_card
    
    make_flip_callback(president)

if __name__ == "__main__":
    app.run_server(debug=True)
