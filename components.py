# components.py

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
    dcc.Link('Dangerous Goods Declaration', href='/excel',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('Bestandsüberprüfung', href='/page_filter',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('Bilderkennung', href='/image',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('DE30 Bestandsart', href='/de30',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
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
    dcc.Link('Dangerous Goods Declaration', href='/excel',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('Bestandsüberprüfung', href='/page_filter',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('Bilderkennung', href='/image',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('DE30 Bestandsart', href='/de30',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
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
    dcc.Link('Dangerous Goods Declaration', href='/excel',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    html.Br(),
    dcc.Link('Bilderkennung', href='/image',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('DE30 Bestandsart', href='/de30',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
])



nav_content7 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H3("Bilderkennung",id="headings7", style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

    dcc.Upload(
        id='upload-pdf',
        children=html.Div([
            'Drag & Drop | ',
            html.A('PDF hochladen')
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
        multiple=True
    ),

    dcc.Input(id='api_input', type='text', placeholder='Enter API Key...'),
    html.Br(),
    html.Button('PDF verarbeiten', id='process-btn', n_clicks=0, disabled=True),
    dcc.Store(id='pdf-content'),
    dcc.Store(id="pdf-processed", data=False),

    html.H6(id="status9"),

    #upload previous extracted file
    html.H4("Upload alt"),
    dcc.Upload(
        id='upload-existing',
        children=html.Div([
            'Drag & Drop | ',
            html.A('PDF upload hochladen')
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
        multiple=True
    ),
    html.H4("Upload neu"),
    dcc.Upload(
        id='upload-newextracted',
        children=html.Div([
            'Drag & Drop | ',
            html.A('PDF upload hochladen')
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
        multiple=True
    ),

    html.H6(id="statuson"),

    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('Dangerous Goods Declaration', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    html.Br(),
    dcc.Link('DE30 Bestandsart', href='/de30',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
])


nav_content8 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    

    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Wareneingänge', href='/page_input',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    html.Br(),
    dcc.Link('Bestandsüberprüfung', href='/page_filter',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('Bilderkennung', href='/image',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.Br(),
    dcc.Link('DE30 Bestandsart', href='/de30',style={'color': '#F5B323', 'fontWeight':'bold'}),
    
])





nav_content9 = html.Div([

    html.Hr(style={'backgroundColor': '#F5B323'}),
    html.H3("DE30 Bestandsart",id="headings11", style={'color': 'black'}),

    html.Hr(style={'backgroundColor': '#F5B323'}),

    dcc.Upload(
        id='upload-De30',
        children=html.Div([
            'Drag & Drop | hochladen',
            html.A('')
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
        multiple=True
    ),


    html.Button('verarbeiten', id='btn-DE30', n_clicks=0, disabled=True),
    dcc.Store(id="data_de30", data=False),

    html.H6(id="status_de30"),


    dcc.Link('Neuer Filter', href='/page1',style={'color': '#F5B323','fontWeight': 'bold'}),
    html.Br(),
    dcc.Link('Dangerous Goods Declaration', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    dcc.Link('M7 Kundenbestellungen', href='/page-3',style={'color': '#F5B323', 'fontWeight':'bold'}),
    html.Br(),
    html.A('Warenausgänge', href='/page-2',style={'color': '#F5B323', 'fontWeight':'bold'},target='_blank'),
    
])

