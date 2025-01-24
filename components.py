# components.py

from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from datetime import datetim# components.py

from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from datetime import datetime, timedelta




current_date = datetime.now().date()
next_date = current_date + timedelta(days=1)


nav_content = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H2("LogFilter",id="headings", style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

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
            'borderColor': '#F5B323',
            'textAlign': 'center',
            'margin': '10px',
            'color':'black'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status"),

    html.Button('Start', id='update-button', n_clicks=None,style={'backgroundColor': '#F5B323'}),
    html.Hr(style={'backgroundColor': 'orange'}),


    #navigation controls

    html.H5("Navigation",style={'color': 'black'}),
    html.Hr(style={'backgroundColor': '#F5B323'}),
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
    html.Hr(style={'backgroundColor': '#F5B323'}),


    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Wareneingänge', href='/page_input',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    html.Br(),
    dcc.Link('Bestandsüberprüfung', href='/page_filter',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
])


nav_content5 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H2("Wareneingänge ",id="headings2", style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

    dcc.Upload(
        id='upload-data2',
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
            'borderColor': '#F5B323',
            'textAlign': 'center',
            'margin': '10px',
            'color':'black'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status20"),

    html.Button('Start', id='update-button2', n_clicks=None,style={'backgroundColor': '#F5B323'}),
    html.Hr(style={'backgroundColor': '#F5B323'}),




    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    html.Br(),
    dcc.Link('Bestandsüberprüfung', href='/page_filter',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
])


nav_content6 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H3("Bestandsüberprüfung ",id="headings6", style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

    dcc.Upload(
        id='upload-data6',
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
            'borderColor': '#F5B323',
            'textAlign': 'center',
            'margin': '10px',
            'color':'black'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status6"),
    html.H6(id="status7"),

    dcc.Upload(
        id='upload-data7',
        children=html.Div([
            'New Drag & Drop or ',
            html.A('Datei auswählen')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'borderColor': '#F5B323',
            'textAlign': 'center',
            'margin': '10px',
            'color':'black'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.H6(id="status8"),

    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    
])

e, timedelta




current_date = datetime.now().date()
next_date = current_date + timedelta(days=1)


nav_content = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H2("LogFilter",id="headings", style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

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
            'borderColor': '#F5B323',
            'textAlign': 'center',
            'margin': '10px',
            'color':'black'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status"),

    html.Button('Start', id='update-button', n_clicks=None,style={'backgroundColor': '#F5B323'}),
    html.Hr(style={'backgroundColor': 'orange'}),


    #navigation controls

    html.H5("Navigation",style={'color': 'black'}),
    html.Hr(style={'backgroundColor': '#F5B323'}),
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
    html.Hr(style={'backgroundColor': '#F5B323'}),


    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Wareneingänge', href='/page_input',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    
])


nav_content5 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H2("Wareneingänge ",id="headings2", style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

    dcc.Upload(
        id='upload-data2',
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
            'borderColor': '#F5B323',
            'textAlign': 'center',
            'margin': '10px',
            'color':'black'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H6(id="status20"),

    html.Button('Start', id='update-button2', n_clicks=None,style={'backgroundColor': '#F5B323'}),
    html.Hr(style={'backgroundColor': '#F5B323'}),




    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    
])


