# components.py

from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from datetime import datetime, timedelta

nav_content2 = html.Div([

    html.Hr(style={'backgroundColor': 'yellow'}),
    html.H2('New Filter',style={'color': 'firebrick'}),

    html.Hr(style={'backgroundColor': 'yellow'}),

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
            'borderColor': 'yellow',
            'margin': '10px',
            'color':'firebrick'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status2"),
    html.Button('Save Tabelle', id='btn', n_clicks=None,style={'backgroundColor': 'yellow'}),

    #html.Button('Start', id='update-button-2', n_clicks=None),
    html.Hr(style={'backgroundColor': 'yellow'}),
    
    dcc.Link('Logfilter', href='/page-2',style={'color': 'Yellow', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': 'Yellow', 'fontWeight':'bold'}),
    
])

available_layouts1 = []
nav_content3 = html.Div([

    html.Hr(style={'backgroundColor': 'yellow'}),
    html.H2('M7 Kundenbestellungen',style={'color': 'firebrick'}),

    html.Hr(style={'backgroundColor': 'yellow'}),

    dcc.Upload(
        id='upload-data-3',
        children=html.Div([
            'Drag & Drop oder',
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
            'borderColor': 'yellow',
            'margin': '10px',
            'color':'firebrick'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status3"),
    html.H6(id="status4"),

    html.H6("wähle ArtikelNr.",style={'font-size': '13px'}),
    dcc.Dropdown(id='search-input9',
        multi=False,
        placeholder='wähle ArtikelNr.',
        options=available_layouts1,
        value='',disabled=False,style={'color': 'black','display': 'block'}),
    #html.Div(id="sc2"),

    html.H6("wähle KundenNr.",style={'font-size': '13px'}),
    dcc.Dropdown(id='search-input10',
        multi=False,
        placeholder='wähle KundenNr.',
        options=available_layouts1,
        value='',disabled=False,style={'color': 'black','display': 'block'}),

    #html.Button('Start', id='update-button-2', n_clicks=None),
    html.Hr(style={'backgroundColor': 'yellow'}),
    
    dcc.Link('Logfilter', href='/page-2',style={'color': 'Yellow', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('New filter', href='/page1',style={'color': 'Yellow', 'fontWeight':'bold'}),
    
])


