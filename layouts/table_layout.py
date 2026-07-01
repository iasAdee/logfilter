from dash import dcc, html


def get_table_controls():
    """Return the table controls layout."""
    return html.Div(id='table-controls', children=[
        html.Label("Rows per page:"),
        dcc.Dropdown(
            id='page-size', 
            options=[10, 20, 50, 100], 
            value=10, 
            clearable=False,
            style={'width':'160px'}
        ),
        html.Button("Clear Cache", id='clear-cache', n_clicks=0, style={'marginLeft':'12px'}),
        html.Button("Process Data", id='process-btn', n_clicks=0, style={'marginLeft':'12px'})
    ], style={'display':'flex', 'gap':'12px', 'alignItems':'center'})


def get_table_layout():
    """Return the table display section layout."""
    return html.Div([
        get_table_controls(),
        html.Hr(),
        html.Div(id='processing-output'),
        html.Hr(),
        html.Div(id='table-container')
    ], style={"maxWidth": "1100px", "margin": "20px auto"})
