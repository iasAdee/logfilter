
import dash
from dash import html
from dash.dependencies import Input, Output
from styles import external_stylesheets, nav_style
from components import nav_content8
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc

page_10_layout = html.Div(
	className="app-container", 



	children=[
	html.Div(style=nav_style, children=[nav_content8]),

	html.Div([
	dbc.Container([
	    html.H1("IMO - Dangerous Goods Declaration", className="mb-4"),
	    
	    # Excel Upload Section
	    dbc.Card([
	        dbc.CardHeader("Step 1: Excel hochladen"),
	        dbc.CardBody([
	            dcc.Upload(
	                id='upload-data72',
	                children=html.Div([
	                    'Drag and Drop or ',
	                    html.A('Excel Datei auswählen ')
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
	                    'margin': '10px 0'
	                },
	                multiple=False
	            ),
	            html.Div(id='status10'),
	            dcc.Store(id='stored-data-72'),
	        ])
	    ], className="mb-4"),
	    
	    # Word Template Upload Section
	    dbc.Card([
	        dbc.CardHeader("Step 2: IMO hochladen "),
	        dbc.CardBody([
	            dcc.Upload(
	                id='upload-doc',
	                children=html.Div([
	                    'Drag and Drop or ',
	                    html.A('Word Datei auswählen optional')
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
	                    'margin': '10px 0'
	                },
	                accept='.docx'
	            ),
	            html.Div(id='output-upload'),
	            dcc.Store(id='stored-data-input_8'),
	        ])
	    ], className="mb-4"),
	    
	    # Process and Download Section
	    dbc.Card([
	        dbc.CardHeader("Step 3: Dokument generieren "),
	        dbc.CardBody([
	            html.Div(id='status11'),
	            html.Button(
	                " Daten verarbeiten", 
	                id="process-excel", 
	                className="btn btn-primary",
	                disabled=True
	            ),
	            dcc.Download(id="download-docx")
	        ])
	    ])
	], fluid=True)

	],
	style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}

	)


	])
