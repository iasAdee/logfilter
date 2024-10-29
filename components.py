# components.py

from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from datetime import datetime, timedelta

"""dropdown_options2 = [
    {'label': '訂製片', 'value': 'fig1'},
    {'label': '試賣', 'value': 'fig2'},
    {'label': '拋棄式', 'value': 'fig3'}
]
"""

"""dcc.Dropdown(id='search-input',
                             multi=False,
                             placeholder='Select Sale Type...',
                             options=dropdown_options2,
                             value='fig1', disabled=False, style={'color': 'black'}),
            """

"""html.H5("Select Input Feature files"),
        dcc.Slider(
            id='edge-slider',
            min=1,
            max=3,
            step=1,
            value=1,
            marks={
                1: {'label': '30'},
                2: {'label': '60'},
                3: {'label': '90'}
            }
        ),"""


current_date = datetime.now().date()
next_date = current_date + timedelta(days=1)


nav_content = html.Div([

    html.Hr(style={'backgroundColor': 'yellow'}),
    html.H2("LogFilter",style={'color': 'firebrick'}),

    html.Hr(style={'backgroundColor': 'yellow'}),

    dcc.Upload(
        id='upload-data',
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
            'borderColor': 'yellow',
            'textAlign': 'center',
            'margin': '10px',
            'color':'firebrick'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status"),

    html.Button('Start', id='update-button', n_clicks=None,style={'backgroundColor': 'yellow'}),
    html.Hr(style={'backgroundColor': 'yellow'}),


    #navigation controls

    html.H5("Navigation",style={'color': 'firebrick'}),
    html.Hr(style={'backgroundColor': 'yellow'}),
    html.A("Pal & PU Tabelle", href="#pal",style={'color': 'azure','fontSize':"12px"}),
    html.Br(),
    #html.Hr(style={'backgroundColor': 'yellow'}),
    html.A("Pal & PU charts", href="#palc",style={'color': 'azure','fontSize':"12px"}),
    #html.Hr(style={'backgroundColor': 'yellow'}),
    html.Br(),
    html.A("Spedition Tabelle", href="#sped",style={'color': 'azure','fontSize':"12px"}),
    #html.Hr(style={'backgroundColor': 'yellow'}),
    html.Br(),
    html.A("Spedition Charts", href="#spedc",style={'color': 'azure','fontSize':"12px"}),
    #html.Hr(style={'backgroundColor': 'yellow'}),
    html.Br(),
    html.A("Vereint Data Tabelle", href="#ver",style={'color': 'azure','fontSize':"12px"}),
    #html.Hr(style={'backgroundColor': 'yellow'}),
    html.Br(),
    html.A("Vereint data Charts", href="#verc",style={'color': 'azure','fontSize':"12px"}),
    #html.Hr(style={'backgroundColor': 'yellow'}),
    html.Br(),
    html.A("Neue Update Charts", href="#neue",style={'color': 'azure','fontSize':"12px"}),
    html.Hr(style={'backgroundColor': 'yellow'}),


    dcc.Link('New Filter', href='/page1',style={'color': 'yellow','fontWeight': 'bold'}),
    
])


