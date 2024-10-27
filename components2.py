# components.py

from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from datetime import datetime, timedelta

nav_content2 = html.Div([

    html.H2('New Filter'),

    html.Hr(style={'backgroundColor': 'azure'}),

    dcc.Upload(
        id='upload-data-2',
        children=html.Div([
            'Drag & Drop or ',
            html.A('Datei auswählen')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status2"),
    html.Button('Save Tabelle', id='btn', n_clicks=None),

    #html.Button('Start', id='update-button-2', n_clicks=None),
    html.Hr(style={'backgroundColor': 'azure'}),
    
    dcc.Link('Go back to Logfilter', href='/page-2',style={'color': 'azure'}),
    
])


