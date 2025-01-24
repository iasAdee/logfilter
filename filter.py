
import dash
from dash import html
from dash.dependencies import Input, Output
from styles import external_stylesheets, nav_style
from components import nav_content6
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

page_6_layout = html.Div(
	className="app-container", 
	
	children=[

		html.Div(style=nav_style, children=[nav_content6]),
		
		html.Div(

			children=[
				dcc.Download(id="download-dataframe-csv6"),
				dcc.Download(id="download-dataframe-csv7"),
				dcc.Store(id="stored-data-6f"),
				dcc.Store(id="stored-data-7f"),
				html.Div(
					html.H6("All zero Materials"),
				),
				html.Div(id='output-data-upload6',
				),
				html.Button('Tabelle speichern', id='sped_button6', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
				html.Div(
					html.H6("Updated Materials"),
				),
				html.Div(id='output-data-upload7',),
				html.Button('Tabelle speichern', id='sped_button7', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
			],
			style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),	

	]

	)