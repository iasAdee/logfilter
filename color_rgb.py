
import dash
from dash import html
from dash.dependencies import Input, Output
from styles import external_stylesheets, nav_style
from components import nav_content10
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

page_12_layout = html.Div(
	className="app-container", 
	
	children=[

		html.Div(style=nav_style, children=[nav_content10]),
		
		html.Div(

			children=[
				#dcc.Download(id="download-dataframe-csv6"),
				dcc.Store(id="cc"),

				html.Div(html.H6("FullTable"),),
				html.Div(id='results_rgb',),
				html.Button('Tabelle speichern', id='sped_buttonrgb', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
				html.Div(id='results_counter',),
				html.Div(id='results_g',),
				html.Div(id='results_o',),,
				html.Div(id='results_r',),
			],
			style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),	

	]

	)