# app.py

import dash
from dash import html
from dash.dependencies import Input, Output

from styles import external_stylesheets, nav_style
from components import nav_content
from components2 import nav_content2
from dash import dcc


import pandas as pd

from collections import Counter
import numpy as np
from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback



from data_processing import DataPreprocessing
#from EDA import eda
import base64
import io
import plotly.graph_objs as go

import warnings
warnings.filterwarnings('ignore') 


@callback(
	Output("download-dataframe-csv3", "data"),
	Input('stored-data1', 'data'),
	Input('sped_button', 'n_clicks'),

	)

def save_data(data1, n_clicks):
	if(n_clicks != None):
		df = pd.DataFrame(data1)
		#df.to_csv("sped_data.csv", index=False)
		return dcc.send_data_frame(df.to_csv, "sped_data.csv", index=False)


@callback(
	Output("download-dataframe-csv2", "data"),
	Input('stored-data2', 'data'),
	Input('pal_button', 'n_clicks'),

	)

def save_data(data1, n_clicks):
	if(n_clicks != None):
		df = pd.DataFrame(data1)
		#df.to_csv("pal_data.csv", index=False)
		return dcc.send_data_frame(df.to_csv, "pal_data.csv", index=False)

@callback(
	Output("download-dataframe-csv1", "data"),
	Input('stored-data3', 'data'),
	Input('ver_button', 'n_clicks'),

	)

def save_data(data1, n_clicks):
	if(n_clicks != None):
		df = pd.DataFrame(data1)
		return dcc.send_data_frame(df.to_csv, "ver_data.csv", index=False)


@callback(
	Output("download-dataframe-csv", "data"),
	Input('stored-data-3formated', 'data'),
	Input('btn', 'n_clicks'),
	)

def save_data(data1, n_clicks):
	if(n_clicks != None):
		df = pd.DataFrame(data1)
		return dcc.send_data_frame(df.to_csv, "filter_data.csv", index=False)


@callback(
    Output('inflation-plot', 'figure'),
    Output('output-data-upload2', 'children'),
    Output('plot1', 'figure'),
    Output('plot2', 'figure'),
    Output('plot3', 'figure'),
    Output('plot4', 'figure'),
    Output('inflation-plot-4', 'figure'),
    Output('inflation-plot-5', 'figure'),
    Output('inflation-plot-6', 'figure'),

    Output('output-data-upload3', 'children'),
	Output('output-data-upload4', 'children'),
    Output('update-button', 'n_clicks'),
    Output('stored-data1', 'data'),
    Output('stored-data2', 'data'),
    Output('stored-data3', 'data'),
    

    Input('stored-data', 'data'),
    Input('update-button', 'n_clicks'),
    
)

def update_graph(data, n_clicks):
	
	if(n_clicks == None):
		return {}, html.Div(),{},{},{},{},{},{},{}, html.Div(),html.Div(),None,{}, {}, {}
	else:

		df = pd.DataFrame(data)
		#print(df.head())
		
		data_preprocessor2 = DataPreprocessing(df)
		data_req, ls, fig = data_preprocessor2.clac_2()

		ls2, ls3, data1, data2, fig2, fig3, fig4, fig5, fig6, fig7 = data_preprocessor2.get_calculated_results()
		fig8 = data_preprocessor2.get_absenders()



		return fig, ls ,fig2, fig3,fig4, fig5,fig6,fig7,fig8 ,ls2 ,ls3, n_clicks, data_req, data1, data2


def format_to_int(value):
	formatted_value = value.replace('.', '').replace(',', '.')
	return int(float(formatted_value))

@callback(
    Output('data_tab', 'children'),
    Output('stored-data-3formated', 'data'),
    Output('status2', 'children'),
 
    Input('stored-data-2', 'data'),
    Input('stored-data-3', 'data'),
    )
def update_second(input1, input2):

	df1 = pd.DataFrame(input1)
	df1 = df1.iloc[:, :4]

	data_dict = {}
	for i in range(len(df1)):
		id = df1["Unnamed: 1"][i]
		if(pd.isna(id)):
			continue
		else:
			if(id.isnumeric()):
				data = df1["Unnamed: 3"][i+1]
				data_dict[id] = data
	

	df2 = pd.DataFrame(input2)
	df2 = df2.iloc[3:]

	
	if(len(df2) > 1):
		data_check = dict(zip(df2["Unnamed: 0"], df2["Unnamed: 1"]))
		ls = []
		for key in data_check:
			if(key in data_dict.keys()):
				result = data_check[key] - format_to_int(data_dict[key])
				ls.append([key, data_check[key], format_to_int(data_dict[key]), result])

		data_df = pd.DataFrame(ls, columns=["Key", "input", "in system", "Differenz"])

		#print(data_df)

		ls = []
		ls.append(html.Div([
		html.H2("Tabelle",style={'color': 'firebrick'}),
		dash_table.DataTable(
		    style_table={'height': '800px', 'overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=data_df.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in data_df.columns],
		    
		    sort_action="native",
		    style_data={
            'backgroundColor': 'lightcyan',
            
        	},
		    style_header={
		        'backgroundColor': 'darkslategrey',
		        'color': 'white',
		        'fontWeight': 'bold',
		        'textAlign': 'center',
		        'border': '1px solid black'
		    }),html.Hr()])
		)

		#print(ls)

		return ls ,data_df.to_dict('records'), "data processed successfully"



	return html.Div([html.H2("Tabelle",style={'color': 'firebrick'})]), {}, "data not uploaded"



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(children=filename,style={'text-align': 'center'}),
        #html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            style_table={'height': '300px', 'overflowY': 'auto'},
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line
    ]), df

@callback(
    #Output('output-data-upload', 'children'),
    Output('stored-data', 'data'),
     Output('status', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(list_of_contents, list_of_names, list_of_dates):

    #print(list_of_contents)
    #print(list_of_names)
    #print(list_of_dates)

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            children.append(child)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        return df_combined.to_dict('records'), "data loaded successfully"
    return {}, ""



@callback(
    #Output('output-data-upload', 'children'),
    Output('stored-data-2', 'data'),
    Output('stored-data-3', 'data'),
    [Input('upload-data-2', 'contents')],
    [State('upload-data-2', 'filename'),
     State('upload-data-2', 'last_modified')]
)
def update_output2(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            
            children.append(df)
        
        return children[0].to_dict('records'),children[1].to_dict('records')
    return {}, {}



@callback(
    Output('plot7', 'figure'),  # Update this div with the output
    Input('submit-button', 'n_clicks'),  # Trigger on button click
    Input('text-input', 'value'),  # Get the value from the text input
    Input('stored-data', 'data'),
)
def update_output(n_clicks, input_value,data):
	if n_clicks != None:  
		#print(input_value)
		df = pd.DataFrame(data)
		
		data_preprocessor2 = DataPreprocessing(df)
		fig =data_preprocessor2.make_customized_plot(input_value)
		return fig
	else:
		return {}


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


page_1_layout = html.Div(
	className="app-container", 

	children=[
	html.Div(style=nav_style, children=[nav_content]),
	dcc.Store(id='stored-data'),
	dcc.Store(id='stored-data1'),
	dcc.Store(id='stored-data2'),
	dcc.Store(id='stored-data3'),


	#dascher etc
	html.Div(id='sped',children = [
		html.H2("Spedition Tabelle",style={'color': 'firebrick'}),
		html.Button('Save Tabelle', id='sped_button', n_clicks=None,style={'backgroundColor': 'yellow','fontSize':"12px"}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(id='output-data-upload2',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(id='spedc',children = [
		html.H2("Spedition Chart",style={'color': 'firebrick'}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	dcc.Graph(id='inflation-plot',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),


	#pal and picks tables
	html.Div(id='pal',children = [
		html.H2("Pal & PU Tabelle",style={'color': 'firebrick'}),
		html.Button('Save Tabelle', id='pal_button', n_clicks=None,style={'backgroundColor': 'yellow','fontSize':"12px"}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='output-data-upload3',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='palc',children = [
		html.H2("Pal & PU Chart",style={'color': 'firebrick'}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(
		id="basic_details2",
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
		            dcc.Graph(id='plot1',
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
		            dcc.Graph(id='plot3',
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
		id="basic_details3",
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
		            dcc.Graph(id='plot2',
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
		            dcc.Graph(id='plot4',
		                #figure=fig4
		                ),
		            
		            style={"height": "100%", 'width': '60%', 'float': 'right','padding': '10px'}
		        ),]

		        ),
		])
		],
		style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),


	dcc.Download(id="download-dataframe-csv2"),
	dcc.Download(id="download-dataframe-csv3"),
	dcc.Download(id="download-dataframe-csv1"),

	##combined
	html.Div(id='ver',children = [
		html.H2("Vereint Data Tabelle",style={'color': 'firebrick'}),
		html.Button('Save Tabelle', id='ver_button', n_clicks=None,style={'backgroundColor': 'yellow','fontSize':"12px"}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='output-data-upload4',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='verc',children = [
		html.H2("Vereint Data  Chart",style={'color': 'firebrick'}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	dcc.Graph(id='inflation-plot-4',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	dcc.Graph(id='inflation-plot-5',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(id='neue',children = [
		html.H2("Neue Updated Charts",style={'color': 'firebrick'}),
		dcc.Input(
		id='text-input', 
		type='text', 
		value='3022', 
		placeholder='Enter User Id'
		),
		html.Button(
		'Submit', 
		id='submit-button', 
		n_clicks=None,style={'backgroundColor': 'yellow','fontSize':"12px"}
		),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(
		id="basic_details4",
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
		            dcc.Graph(id='inflation-plot-6',
		                #figure=fig3
		                ),
		            className="plot4",
		            style={"height": "100%", 'width': '60%', 'float': 'left','padding': '10px'}
		        ),]

		        ),

		html.Div(
		    className="left-container",
		    children=[
		        html.Div(
		            dcc.Graph(id='plot7',
		                #figure=fig4
		                ),
		            
		            style={"height": "100%", 'width': '40%', 'float': 'right','padding': '10px'}
		        ),]

		        ),
		])
		],
		style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	


	    ],
	id="theme_change"

	)

page_2_layout = html.Div([
	html.Div(style=nav_style, children=[nav_content2]),
	dcc.Store(id='stored-data-2'),
	dcc.Store(id='stored-data-3'),
	dcc.Store(id='stored-data-3formated'),

	#html.H2(id= "idd",children =["Tabelle"],style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'cadetblue'}),

	html.Div(id='data_tab',children = [
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(id= "This")
])

page_3_layout = html.Div([
	#html.Div(style=nav_style, children=[nav_content2]),


	html.Div(
	    [
	    	html.H1("Login page"),
	        html.H6("ID", style={'font-size': '13px'}),
	        dcc.Input(id='input-text1', 
	                  type='text', 
	                  value='', 
	                  style={"width": "100%"}),

	        html.H6("Password", style={'font-size': '13px'}),
	        dcc.Input(id='input-text2', 
	                  type='password', 
	                  value='', 
	                  style={"width": "100%"}),

	        html.Br(),
	        dcc.Link('Login', href='/page-2',style={'color': 'yellow','fontWeight': 'bold'}),
	        html.Div(id='success'),
	    ],
	    style={
	        "display": "flex",
	        "flexDirection": "column",
	        "alignItems": "center",
	        "justifyContent": "center",
	        "width": "300px",  # Set fixed width
	        "height": "300px",  # Set fixed height
	        "margin": "auto",  # Center horizontally
	        "position": "absolute",
	        "color":"white",
	        "top": "50%",
	        "left": "50%",
	        "transform": "translate(-50%, -50%)",
	        "border": "1px solid #ccc",
	        "padding": "20px",
	        "boxShadow": "0px 0px 10px rgba(0, 0, 0, 0.1)",
	        "borderRadius": "8px",
	        "backgroundColor": "firebrick"
	    }
	),

	#dcc.Link('New Filter', href='/page1',style={'color': 'yellow','fontWeight': 'bold'}),
	#dcc.Link('Go back to Logfilter', href='/page-2',style={'color': 'Yellow', 'fontWeight':'bold'}),

	#html.Div(id= "This")
])




# App layout
app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content'),
	dcc.Download(id="download-dataframe-csv"),
	html.Div(id='page-1-content', style={'display': 'block'}, children=[
	    page_1_layout
	]),

	html.Div(id='page-2-content', style={'display': 'none'}, children=[
	    page_2_layout
	]),

	html.Div(id='page-3-content', style={'display': 'none'}, children=[
	    page_3_layout
	])

	])


@app.callback(
    [Output('page-1-content', 'style'),
     Output('page-2-content', 'style'),
     Output('page-3-content', 'style'),
     Output('success', 'children')
     ],
    [Input('url', 'pathname'),
    Input('input-text1', 'value'),
    Input('input-text2', 'value'),
    ]
)
def display_page(pathname,id_, pass_):

	if(id_ == "log" and pass_ == "C3asar!"):
	
	    if pathname == '/page-2':
	        return {'display': 'block'}, {'display': 'none'} ,{'display': 'none'}, ""
	    elif(pathname == "/page1"):
	        return {'display': 'none'}, {'display': 'block'} ,{'display': 'none'}, ""
	    else:
	    	return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, ""
	elif(id_ == "" and pass_ == ""):
		return {'display': 'none'}, {'display': 'none'}, {'display': 'block'},"please enter id and password"
	else:
		return {'display': 'none'}, {'display': 'none'}, {'display': 'block'},""





app.css.append_css({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
})
if __name__ == '__main__':
    app.run_server(debug=True)




