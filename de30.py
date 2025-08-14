
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
			html.H6("Results"),
			),

		html.Div(
			id='De30_Table',
			style={"height": "500px", 'width': '100%'}
			),
		html.Div(
		    dcc.Graph(id='plot_de30',
		        ),
		    
		    style={"height": "100%", 'width': '100%', 'float': 'right','padding': '10px'}
		),

		],

	style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
	),
	]
)