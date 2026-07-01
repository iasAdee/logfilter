# components.py

from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from datetime import datetime, timedelta

nav_content2 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H2('Neuer Filter',style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

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
            'borderColor': '#F5B323',
            'margin': '10px',
            'color':'black'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status2"),
    html.Button('Save Tabelle', id='btn', n_clicks=None,style={'backgroundColor': '#F5B323'}),

    #html.Button('Start', id='update-button-2', n_clicks=None),
    html.Hr(style={'backgroundColor': '#F5B323'}),
    
    dcc.Link('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Wareneingänge', href='/page_input',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    html.Br(),
    dcc.Link('Bilderkennung', href='/image',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('DE30 Bestandsart', href='/de30',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
])

available_layouts1 = []
nav_content3 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H2('M7 Kundenbestellungen',style={'color': 'Black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

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
            'borderColor': '#F5B323',
            'margin': '10px',
            'color':'black'
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
    html.Hr(style={'backgroundColor': '#F5B323'}),
    
    dcc.Link('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    html.A('Wareneingänge', href='/page_input',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    html.Br(),
    dcc.Link('Bilderkennung', href='/image',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('DE30 Bestandsart', href='/de30',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
])


