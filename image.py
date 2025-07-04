
import dash
from dash import html
from dash.dependencies import Input, Output
from styles import external_stylesheets, nav_style
from components import nav_content7
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

page_7_layout = html.Div(
	className="app-container", 

	children=[
	dcc.Store(id='pdf_data'),
	html.Div(style=nav_style, children=[nav_content7]),


	html.Div([
	html.Div(
			html.H6("Results"),
		),
		html.Div(id='pdf_results',),

		
		dcc.Store(id='stored_results'),
		dcc.Download(id="download-dataframe-pdf"),
		html.Button('Tabelle speichern', id='sped_button8', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
		html.Div(
		            dcc.Graph(id='ploti12',
		                ),
		            
		            style={"height": "100%", 'width': '100%', 'float': 'right','padding': '10px'}
		        ),

		html.Div(id='pdf_results_after_check',),

	],	
	style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
	),
	]	
)
