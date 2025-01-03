
import dash
from dash import html
from dash.dependencies import Input, Output
from styles import external_stylesheets, nav_style
from components import nav_content5
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

page_5_layout = html.Div(
	className="app-container", 

	


	children=[
	dcc.Store(id='stored-data-input'),
	html.Div(style=nav_style, children=[nav_content5]),
	


	#pal and picks tables
	html.Div(id='pali',children = [
		html.H2("Pal & PU Tabelle",style={'color': 'black','font-size': '13px'}),
		html.Button('Save Tabelle', id='pal_buttoni', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='output-data-upload3i',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='palci',children = [
		html.H2("Pal & PU Chart",style={'color': 'black','font-size': '13px'}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(
		id="basic_details2i",
		className="outer-container1",
		children=[
			html.Div(
			className="plots-container",
			children=[
			
				# Plot 1
				html.Div(
				    className="left-container",
				    children=[
				        html.Div(
				            dcc.Graph(id='ploti1',
				                #figure=fig3
				                ),
				            className="plot4",
				            style={"height": "100%", 'width': '40%', 'float': 'left','padding': '10px'}
				        ),]

				        ),

				html.Div(
				    className="left-container",
				    children=[
				        html.Div(
				            dcc.Graph(id='ploti3',
				                #figure=fig4
				                ),
				            
				            style={"height": "100%", 'width': '60%', 'float': 'right','padding': '10px'}
				        ),]

				        ),
			])
		],
		style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),


	html.Div(
		id="basic_details3i",
		className="outer-container1",
		children=[
		html.Div(
		className="plots-container",
		children=[
		
		# Plot 1
		html.Div(
		    className="left-container",
		    children=[
		        html.Div(
		            dcc.Graph(id='ploti2',
		                #figure=fig3
		                ),
		            className="plot4",
		            style={"height": "100%", 'width': '40%', 'float': 'left','padding': '10px'}
		        ),]

		        ),

		html.Div(
		    className="left-container",
		    children=[
		        html.Div(
		            dcc.Graph(id='ploti4',
		                #figure=fig4
		                ),
		            
		            style={"height": "100%", 'width': '60%', 'float': 'right','padding': '10px'}
		        ),]

		        ),
		])
		],
		style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	dcc.Download(id="download-dataframe-csv2i"),

	
    html.Div(
        dcc.Graph(id='inflation-plot-10i',
        style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
        ),

    ),

    html.Div(
        dcc.Graph(id='inflation-plot-11i',
        style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
        ),

    ),

	    ],
	id="theme_change2"

	)
