
import dash
from dash import html
from dash.dependencies import Input, Output
from styles import external_stylesheets, nav_style
from components import nav_content9
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

page_11_layout = html.Div(
	className="app-container", 

	children=[
	html.Div(style=nav_style, children=[nav_content9]),

	html.Div([
	html.Div(
			children=[
			html.H6("Results"),
			html.Button('Tabelle speichern', id='de30button', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
			dcc.Download(id="download-dataframe-de30"),
			dcc.Store(id='de30_results'),]
			),

		html.Div(
			id='De30_Table',
			style={"height": "500px", 'width': '100%'}
			),

		],

	style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
	),
	]
)
