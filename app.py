# app.py

import dash
from dash import html
from dash.dependencies import Input, Output

from styles import external_stylesheets, nav_style
from components import nav_content
from components2 import nav_content2,nav_content3
from dash import dcc


import pandas as pd

from collections import Counter
import numpy as np
from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback, ctx



from data_processing import DataPreprocessing
#from EDA import eda
import base64
import io
import plotly.graph_objs as go
from input import page_5_layout
from filter import page_6_layout
from image import page_7_layout



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
	Output("download-dataframe-csv6", "data"),
	
	Input('stored-data-6f', 'data'),
	Input('sped_button6', 'n_clicks'),

	)

def save_data(data1, n_clicks):
	if(n_clicks != None):
		df = pd.DataFrame(data1)
		#df.to_csv("sped_data.csv", index=False)
		return dcc.send_data_frame(df.to_csv, "allzeros.csv", index=False)

@callback(
	Output("download-dataframe-csv7", "data"),
	
	Input('stored-data-7f', 'data'),
	Input('sped_button6', 'n_clicks'),

	)

def save_data(data1, n_clicks):
	if(n_clicks != None):
		df = pd.DataFrame(data1)
		#df.to_csv("sped_data.csv", index=False)
		return dcc.send_data_frame(df.to_csv, "checked_zeros.csv", index=False)



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
	Output("download-dataframe-csv2i", "data"),
	Input('stored-data2i', 'data'),
	Input('pal_buttoni', 'n_clicks'),

	)

def save_data(data1, n_clicks):
	if(n_clicks != None):
		df = pd.DataFrame(data1)
		#df.to_csv("pal_data.csv", index=False)
		return dcc.send_data_frame(df.to_csv, "pal_data_input.csv", index=False)

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
    Output('inflation-plot-10', 'figure'),
    Output('inflation-plot-11', 'figure'),

    Output('output-data-upload3', 'children'),
	Output('output-data-upload4', 'children'),
    Output('update-button', 'n_clicks'),
    Output('stored-data1', 'data'),
    Output('stored-data2', 'data'),
    Output('stored-data3', 'data'),
    Output('stored-data4', 'data'),
    

    Input('stored-data', 'data'),
    Input('update-button', 'n_clicks'),
    
)


def update_graph(data, n_clicks):
	
	if(n_clicks == None):
		return {}, html.Div(),{},{},{},{},{},{},{},{},{}, html.Div(),html.Div(),None,{}, {}, {}, []
	else:

		df = pd.DataFrame(data)

		if("Bestellmengeneinheit" in df.columns):
			#print(df)

			return {}, html.Div(),{},{},{},{},{},{},{},{},{}, html.Div(),html.Div(),None,{}, {}, {}, []


			"""Sales Order = bestellmenge 
												MatBez = kurztext 
												Werk = Werk
												MatNr = Material
												AME = Bestellmengeneinheit
												BME = Bestellpreis-ME
												BereitStellDat = Lieferdatum
												Auftragsmenge_Offen = Bestellmenge"""





		names_update_lower = {key.lower(): value for key, value in names_update.items()}
		#print(names_update_lower)
		df.columns = [names_update_lower.get(col.lower().strip(), col) for col in df.columns]

		


		ls = []
		for i, val in enumerate(df["Summe von BrGew_Offen"]):
		    ls.append(float(str(val).strip().replace(",", ".").replace(".","")))

		df["Summe von BrGew_Offen"] = ls

		#print(df.columns)
		data_preprocessor2 = DataPreprocessing(df)
		data_req, ls, fig = data_preprocessor2.clac_2()
		ls2, ls3, data1, data2, fig2, fig3, fig4, fig5, fig6, fig7, fig10, fig20 = data_preprocessor2.get_calculated_results(input=False)
		fig8 = data_preprocessor2.get_absenders()



		return fig, ls ,fig2, fig3,fig4, fig5,fig6,fig7,fig8, fig10,fig20 ,ls2 ,ls3, n_clicks, data_req, data1, data2,data



@callback(
    Output('ploti1', 'figure'),
    Output('ploti2', 'figure'),
    Output('ploti3', 'figure'),
    Output('ploti4', 'figure'),
    Output('inflation-plot-10i', 'figure'),
    Output('inflation-plot-11i', 'figure'),
    Output('output-data-upload3i', 'children'),
    Output('stored-data2i', 'data'),
    
    Input('stored-data-input', 'data'),
    Input('update-button2', 'n_clicks'),
    
)


def update_graph2(data, n_clicks):
	if(n_clicks == None):
		return {},{},{},{}, {}, {}, [], {}
	else:
		df = pd.DataFrame(data)


		col_updates={
		"kurztext":"MatBez", 
		"Werk":"Werk",
		"Material":"MatNr",
		"Bestellmengeneinheit":"AME",
		"Bestellpreis-ME":"BME",
		"Lieferdatum":"BereitStellDat",
		"Bestellmenge":"Auftragsmenge_Offen",
		"noch zu liefern (Menge)":"Auftragsmenge_bereits_geliefert"}


		col_updates = {key.lower(): value for key, value in col_updates.items()}
		df.columns = [col_updates.get(col.lower().strip(), col) for col in df.columns]

		data_preprocessor2 = DataPreprocessing(df)
		ls2, ls3, data1, data2, fig2, fig3, fig4, fig5, fig6, fig7, fig10, fig20 = data_preprocessor2.get_calculated_results(input=True)

		return fig2,fig3,fig4,fig5, fig10, fig20, ls2, data1


def format_to_int(value):
	formatted_value = value.replace('.', '').replace(',', '.')
	return int(float(formatted_value))



names_update = {
	"VStl": "Versandstelle",
	"Route": "Route",
	"Spediteur": "Forwarder",
	"VkOrg": "VKOrg",
	"VWeg": "VWEG",
	"SP": "Sparte",
	"VkBür": "VKBüro",
	"Angel.von": "SO_angelegt_von",
	"AuftrGeber": "AG-ID",
	"Warenempf.": "WE-ID",
	"Adresse": "WE-tatsächlich_ID",
	"Verursach.": "SalesOrder",
	"Eint": "SO_ATP_Einteilung",
	"AuftrMenge": "Auftragsmenge",
	"Bestä.Mg": "Auftragsmenge_Bestätigt",
	"Offene Mng": "Auftragsmenge_Offen",
	"gelMenge": "Auftragsmenge_bereits_geliefert",
	"ME": "AME",
	"BME": "BME",
	"KumAuMenge": "Auftragsmenge_Gesamt",
	"Werk": "Werk",
	"Kundenreferenz": "BestellNr_Kunde",
	"Versandbed": "Versandbedingung",
	"Zähler": "Zähler",
	"SKU_Nenner": "SKU_Nenner",
	"Bereit.Dat": "BereitStellDat",
	"Name/Warenempfänger": "WE-Name",
	"Ort/Warenempfänger": "WE-Stadt",
	"LS": "Liefersperre",
	"Brutto": "Summe von BrGew_Offen",
	"KLF": "KomplettLF_KZ",
	"LfG": "LF-Gruppe",
	"VArt": "SO_Art",
	"Belegtyp": "BelegStatus",
	"Material": "MatNr",
	"Positionsbezeichnung": "MatBez",
	"Charge": "Charge_aus_SO",
	"Etyp": "ATP_Eint_Typ",
	"FS": "Fakturasperre",
	"IncTm": "Inco1",
	"Incoterms 2": "Inco2",
	"BDAr": "ATP_Bedarfsart",
	"Plz/WEMPF": "WE_PLZ"
}



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
		html.H2("Tabelle",style={'color': 'black','font-size': '13px'}),
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



	return html.Div([html.H2("Tabelle",style={'color': 'black','font-size': '13px'})]), {}, "data not uploaded"



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-16')), delimiter='\t')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

        elif 'xlsx' in filename.lower():
            # Assume that the user uploaded an excel file
            #print("I am here")
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

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            children.append(child)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        return df_combined.to_dict('records'), "Daten erfolgreich geladen"
    return {}, ""

@callback(
    #Output('output-data-upload', 'children'),
    Output('stored-data-input', 'data'),
     Output('status20', 'children'),
    [Input('upload-data2', 'contents')],
    [State('upload-data2', 'filename'),
     State('upload-data2', 'last_modified')]
)
def update_output20(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            children.append(child)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        return df_combined.to_dict('records'), "Daten erfolgreich geladen"
    return {}, ""


@callback(
    #Output('output-data-upload', 'children'),
    Output('stored-data-5', 'data'),
     Output('status3', 'children'),
    [Input('upload-data-3', 'contents')],
    [State('upload-data-3', 'filename'),
     State('upload-data-3', 'last_modified')]
)
def update_output3(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            children.append(child)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        return df_combined.to_dict('records'), "Daten erfolgreich geladen"
    return {}, ""

@callback(
    #Output('output-data-upload', 'children'),
    Output('stored-data-6', 'data'),
     Output('status6', 'children'),
    [Input('upload-data6', 'contents')],
    [State('upload-data6', 'filename'),
     State('upload-data6', 'last_modified')]
)
def update_output6(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            children.append(child)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        return df_combined.to_dict('records'), "Daten erfolgreich geladen"
    return {}, ""

@callback(
    #Output('output-data-upload', 'children'),
    Output('stored-data-7', 'data'),
     Output('status8', 'children'),
    [Input('upload-data7', 'contents')],
    [State('upload-data7', 'filename'),
     State('upload-data7', 'last_modified')]
)
def update_output8(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            children.append(child)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        return df_combined.to_dict('records'), "Daten erfolgreich geladen"
    return {}, ""


@callback(
    Output('status7', 'children'),
    Output('output-data-upload6', 'children'),
    Output('output-data-upload7', 'children'),
    Output('stored-data-6f', 'data'),
    Output('stored-data-7f', 'data'),
    

 	Input('stored-data-6', 'data'),
 	Input('stored-data-7', 'data'),
    )
def update_second(input1, input2):
	data = pd.DataFrame(input1)
	data2 = pd.DataFrame(input2)


	if(len(data) == 0):
		return "Data Not recived Yet", [], [], [], []
	else:
		#print(data)
		data = data.dropna(subset=['Material','Gesperrt', 'Nicht freier Bestand', 'In Qualitätsprüfung' ])
		selected_rows = data[(data['Gesperrt'] > 0) | (data['Nicht freier Bestand'] > 0) | (data['In Qualitätsprüfung'] > 0)]

		
		ls = []
		ls.append(html.Div([
		dash_table.DataTable(
		    style_table={'height': '400px','overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=selected_rows.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in selected_rows.columns],
		    #editable=True,
		    #filter_action="native",
		    sort_action="native",
		    style_data={
            'backgroundColor': 'white',
            
        	},
		    #page_action="native",
		    style_header={
		        'backgroundColor': 'darkslategrey',
		        'color': 'lightcyan',
		        'fontWeight': 'bold',
		        'textAlign': 'center',
		        'border': '1px solid black'
		    }),html.Hr()])
		)

		new_dataframe = pd.DataFrame()
		if(len(data2) > 0):
			data2 = data2.dropna(subset=['Material','Gesperrt', 'Nicht freier Bestand', 'In Qualitätsprüfung'])
			data2 = data2.dropna(subset=['Material','Gesperrt', 'Nicht freier Bestand', 'In Qualitätsprüfung' ]).reset_index(drop=True)
			
			checked = []
			for i in range(len(data2)):
			    mat_id = data2["Material"][i]
			    
			    if(mat_id not in list(selected_rows.Material)):
			        continue
			        
			    if(mat_id in checked):
			        continue
			    else:
			        checked.append(mat_id)   
			        if(data2["Gesperrt"][i] == 0 and data2["Nicht freier Bestand"][i]==0 and data2["In Qualitätsprüfung"][i]==0):
			            new_dataframe = pd.concat([new_dataframe, data2.iloc[[i]]], ignore_index=True)
		ls2 = []

		if(len(new_dataframe)>0):
			ls2.append(html.Div([
			dash_table.DataTable(
			    style_table={'height': '400px','overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
			    data=new_dataframe.to_dict('records'),
			    columns=[{"name": i, "id": i} for i in new_dataframe.columns],
			    #editable=True,
			    #filter_action="native",
			    sort_action="native",
			    style_data={
	            'backgroundColor': 'white',
	            
	        	},
			    #page_action="native",
			    style_header={
			        'backgroundColor': 'darkslategrey',
			        'color': 'lightcyan',
			        'fontWeight': 'bold',
			        'textAlign': 'center',
			        'border': '1px solid black'
			    }),html.Hr()])
			)


		return "Data Recived", ls, ls2,selected_rows.to_dict('records'),new_dataframe.to_dict('records')



def process_data(data):
    column_values = []
    previous_value = ""
    for i, row in data.iterrows():
        if(i < 3):
            continue

        new_value = ""
        for j, val in enumerate(row):
            if(not pd.isna(val)):
                if(j == 5):
                    #print(j, val)
                    new_value = row[1]

        if(new_value == ""):
            column_values.append([previous_value, pd.to_datetime(row[8], format="%d.%m.%Y"),row[9], row[14]])

        else:
            previous_value = new_value 
    data_1 = pd.DataFrame(column_values,columns= ["order_id", "date", "value", "client"] ) 
    data_1 = data_1.dropna().reset_index(drop=True)
    ls = []
    for i, val in enumerate(data_1["value"]):
        ls.append(abs(float(str(val).strip().replace(",", "."))))


    data_1["value"] = ls
    
    
    
    return data_1

def make_barchart(order_id, proccessed_data):

    
    filtered_data = proccessed_data[proccessed_data['order_id'] == order_id]

    # Group by client and calculate the sum of value
    client_values = filtered_data.groupby('client')['value'].sum().reset_index()

    # Create an interactive bar chart using Plotly
    fig = px.bar(
        client_values,
        x='client',
        y='value',
        text='value',  # Display values on the bars
        labels={'client': 'Client ID', 'value': 'Total Value'},  # Customize axis labels
        title=f'Gesamte Bestellungen des Artikels {order_id} je Kunde ',
        #color_discrete_sequence=["#F5B323"]
    )

    # Customize appearance
    fig.update_traces(marker_color='#F5B323', textposition='outside')  # Bar color and text position
    fig.update_layout(
        xaxis=dict(title='KundenNr.', tickmode='linear'),
        yaxis=dict(title='Gesamtwert'),
        title=dict(font=dict(size=18), x=0.5),  # Center-align title
        template='plotly_white',  # Use a clean theme

    )

    # Show the figure
    return fig


import plotly.express as px

def make_linechart(order_id, proccessed_data):
    
    
    filtered_data = proccessed_data[proccessed_data['order_id'] == order_id]

    # Sort data by date to ensure proper line chart visualization
    filtered_data = filtered_data.sort_values(by='date')

    # Create a line chart using Plotly
    fig = px.line(
        filtered_data,
        x='date',
        y='value',
        labels={'date': 'Date', 'value': 'Value'},
        title=f'Zeitachse der Bestellungen des Artikels {order_id}',
        markers=True,  # Add markers to indicate data points
        color_discrete_sequence=["#F5B323"]
    )

    # Customize appearance
    fig.update_traces(line_color='#F5B323', marker=dict(size=8))
    fig.update_layout(
        xaxis=dict(title='Datum', tickformat='%d-%m-%y'),
        yaxis=dict(title='wert'),
        title=dict(font=dict(size=18), x=0.5),  # Center-align title
        template='plotly_white',
    )

    # Show the figure
    return fig

def make_dropdowns(lss):
	dropdown_options = []
	for value in lss:
		dropdown_options.append(
	    	{'label': value, 'value': value})
	return dropdown_options

def make_barchart_client(client_id, proccessed_data):

    
    filtered_data = proccessed_data[proccessed_data['client'] == client_id]

    # Group by client and calculate the sum of value
    client_values = filtered_data.groupby('order_id')['value'].sum().reset_index()

    # Create an interactive bar chart using Plotly
    fig = px.bar(
        client_values,
        x='order_id',
        y='value',
        text='value',  # Display values on the bars
        labels={'client': 'Client ID', 'value': 'Total Value'},  # Customize axis labels
        title=f' Gesamte Bestellungen des Kunden {client_id} je Artike',
        #color_discrete_sequence=["#F5B323"]
    )

    # Customize appearance
    fig.update_traces(marker_color='#F5B323', textposition='outside')  # Bar color and text position
    fig.update_layout(
        xaxis=dict(title='ArtikelNr.', tickmode='linear'),
        yaxis=dict(title='Gesamtwert'),
        title=dict(font=dict(size=18), x=0.5),  # Center-align title
        template='plotly_white',  # Use a clean theme

    )

    # Show the figure
    return fig


def make_linechart_client(client_id, proccessed_data):
    
    
    filtered_data = proccessed_data[proccessed_data['client'] == client_id]

    # Sort data by date to ensure proper line chart visualization
    filtered_data = filtered_data.sort_values(by='date')

    # Create a line chart using Plotly
    fig = px.line(
        filtered_data,
        x='date',
        y='value',
        labels={'date': 'Date', 'value': 'Value'},
        title=f'Gesamte Bestellungen des Kunden {client_id}',
        markers=True,  # Add markers to indicate data points,
       	#color_discrete_sequence=["#F5B323"]
    )

    # Customize appearance
    fig.update_traces(line_color='#F5B323', marker=dict(size=8))
    fig.update_layout(
        xaxis=dict(title='Datum', tickformat='%d-%m-%y'),
        yaxis=dict(title='Wert'),
        title=dict(font=dict(size=18), x=0.5),  # Center-align title
        template='plotly_white',
    )

    # Show the figure
    return fig

@callback(
    #Output('output-data-upload', 'children'),
   	Output('status4', 'children'),
   	Output('plot30', 'figure'),
   	Output('plot40', 'figure'),
   	Output('plot31', 'figure'),
   	Output('plot41', 'figure'),
   	Output('search-input9', 'options'),
   	Output('search-input10', 'options'),
    Input('stored-data-5', 'data'),
    Input('search-input9', 'value'),
    Input('search-input10', 'value'),
    
) 
def get_new_Data(data,order_id, client_id):

	data = pd.DataFrame(data)

	if(len(data) > 0):
		#print(data)
		proccessed_data = process_data(data)
		lss = set(proccessed_data.order_id)
		lss2 = set(proccessed_data.client)
		options =make_dropdowns(lss)
		options2 =make_dropdowns(lss2)
        
		if(order_id == "" or client_id == ""):
			return "wähle ArtikelNr. & KundenNr.", {}, {}, {}, {}, options, options2
		else:
			fig1 = make_barchart(order_id, proccessed_data)
			fig2 = make_linechart(order_id, proccessed_data)
			fig3 = make_barchart_client(client_id, proccessed_data)
			fig4 = make_linechart_client(client_id, proccessed_data)
			return "Erhaltene Daten zum verarbeiten", fig1, fig2, fig3, fig4, options,options2
	else:
		return "data not recived yet for processing", {}, {},{},{}, [],[]





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
    Input('stored-data4', 'data'),
)
def update_output(n_clicks, input_value,data):
	if n_clicks != None:  
		#print(input_value)
		df = pd.DataFrame(data)

		names_update_lower = {key.lower(): value for key, value in names_update.items()}
		#print(names_update_lower)
		df.columns = [names_update_lower.get(col.lower().strip(), col) for col in df.columns]

		#print(df)
		#print(input_value)
		
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
	dcc.Store(id='stored-data2i'),
	dcc.Store(id='stored-data3'),
	dcc.Store(id='stored-data4'),
	


	#dascher etc
	html.Div(id='sped',children = [
		html.H2("Spedition Tabelle",style={'color': 'black','font-size': '13px'}),
		html.Button('Tabelle speichern', id='sped_button', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(id='output-data-upload2',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div(id='spedc',children = [
		html.H2("Spedition Chart",style={'color': 'black','font-size': '13px'}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	dcc.Graph(id='inflation-plot',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),


	#pal and picks tables
	html.Div(id='pal',children = [
		html.H2("Pal & PU Tabelle",style={'color': 'black','font-size': '13px'}),
		html.Button('Tabelle speichern', id='pal_button', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='output-data-upload3',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='palc',children = [
		html.H2("Pal & PU Chart",style={'color': 'black','font-size': '13px'}),
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
		html.H2("Vereint Data Tabelle",style={'color': 'black','font-size': '13px'}),
		html.Button('Tabelle speichern', id='ver_button', n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='output-data-upload4',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(id='verc',children = [
		html.H2("Vereint Data  Chart",style={'color': 'black','font-size': '13px'}),
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
		html.H2("Neue Updated Charts",style={'color': 'black','font-size': '13px'}),
		dcc.Input(
		id='text-input', 
		type='text', 
		value='3022', 
		placeholder='Enter User Id'
		),
		html.Button(
		'Submit', 
		id='submit-button', 
		n_clicks=None,style={'backgroundColor': '#F5B323','fontSize':"12px"}
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

    html.Div(
        dcc.Graph(id='inflation-plot-10',
        style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
        ),

    ),

    html.Div(
        dcc.Graph(id='inflation-plot-11',
        style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
        ),

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

page_4_layout = html.Div([
	html.Div(style=nav_style, children=[nav_content3]),
	dcc.Store(id='stored-data-5'),

	html.Div(children = [
		html.H5("ArtikelNr. Charts"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(children = [
		html.Div(
		            dcc.Graph(id='plot30',
		                #figure=fig4
		                ),
		            style={"height": "100%", 'width': '100%', 'float': 'right','padding': '10px'}
		        ),
	
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(children = [
		html.Div(
		            dcc.Graph(id='plot40',
		                #figure=fig4
		                ),
		            
		            style={"height": "100%", 'width': '100%', 'float': 'right','padding': '10px'}
		        ),
	
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	
	html.Div(children = [
		html.H5("KundenNr. Charts"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(children = [
		html.Div(
		            dcc.Graph(id='plot31',
		                #figure=fig4
		                ),
		            
		            style={"height": "100%", 'width': '100%', 'float': 'right','padding': '10px'}
		        ),
	
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),
	html.Div(children = [
		html.Div(
		            dcc.Graph(id='plot41',
		                #figure=fig4
		                ),
		            
		            style={"height": "100%", 'width': '100%', 'float': 'right','padding': '10px'}
		        ),
	
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': 'lightgray'}
		),

	html.Div()
])



page_3_layout = html.Div([
	#html.Div(style=nav_style, children=[nav_content2]),


	html.Div(
	    [
	    	html.H1("Login", style={ "color":"black"}),
	        html.H6("ID", style={'font-size': '13px', "color":"black"}),
	        dcc.Input(id='input-text1', 
	                  type='text', 
	                  value='', 
	                  style={"width": "100%"}),

	        html.H6("Password", style={'font-size': '13px', "color":"black"}),
	        dcc.Input(id='input-text2', 
	                  type='password', 
	                  value='', 
	                  style={"width": "100%"}),

	        html.Br(),
	        dcc.Link('Login', href='/page-2',style={'color': 'firebrick','fontWeight': 'bold'}),
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
	        "backgroundColor": "#FFCC33"
	    }
	),

	#dcc.Link('New Filter', href='/page1',style={'color': 'yellow','fontWeight': 'bold'}),
	#dcc.Link('Go back to Logfilter', href='/page-2',style={'color': 'Yellow', 'fontWeight':'bold'}),

	#html.Div(id= "This")
])

import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import re
import base64

import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "AIzaSyByx1qgfrg6aPl8sTXyYKRX79LQEeZzPjc"
genai.configure(api_key=os.environ["GEMINI_API_KEY"]) 
model = genai.GenerativeModel("gemini-1.5-flash")


@app.callback(
    Output("status9", "children"),
    Output("process-btn", "disabled"),
    Output("pdf-content", "data"),
    Output("pdf-processed", "data"),
    Output("pdf_results", "children"),
    


    Input("upload-pdf", "contents"),
    Input("process-btn", "n_clicks"),
    State("pdf-content", "data"),
    State("pdf-processed", "data"),
    prevent_initial_call=True
)
def handle_pdf(upload_content, n_clicks, content, processed):
	triggered_id = ctx.triggered_id  

	if triggered_id == "upload-pdf":
		if upload_content is None:
		    return "", True, None, False  # No file uploaded, disable button
		return "File uploaded.", False, upload_content, False, []

	if triggered_id == "process-btn":
		if content is None:
		    return "No file uploaded.", dash.no_update, None, False, []

		if processed:
		    return "PDF already processed.", True, content, True , []

		if content is not None:

			#print(contents)
			content_type, content_string = content[0].split(',')
			decoded = io.BytesIO(base64.b64decode(content_string))

			# Extract text from the PDF
			doc = fitz.open(stream=decoded, filetype="pdf")
			images_list = []

			print(f"Total Pages in the document : {len(doc)}")

			prompt_list = []
			for page_number in range(len(doc)):
			    
			    if(page_number%3 != 0):
			        continue        
			        
			    page = doc[page_number]
			    text = page.get_text()
			    
			    text_data = text.split("\n")
			    
			    #print(text_data)
			    
			    text = ""
			    artikle = ""
			    for i, tex in enumerate(text_data):
			        if(tex.startswith("PO")):
			            text=tex
			            
			        if(tex.startswith("FERT-Artikel-Nummer")):
			            artikle = text_data[i+1]
			            
			    images = page.get_images(full=True) 
			    print(f"Page Number: {page_number} and {text} and artikel = {artikle}")
			    
			    text_data = text.split(":")
			    image_results = [text_data[1].strip(), artikle.strip()]
			    
			    if(len(images)<=1):
			        continue
			    
			    for img_index, img in enumerate(images):
			        xref = img[0]  
			        
			        if(img_index>=2):
			            break
			        base_image = doc.extract_image(xref)  
			        image_bytes = base_image["image"]  
			        
			        
			        image = Image.open(BytesIO(image_bytes))
			        
			        buffered = BytesIO()
			        image.save(buffered, format="JPEG")
			        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
			        
			        prompt = [
			            {
			                "mime_type": "image/jpeg",
			                "data": image_base64,
			            },
			            "Extract the exact text from this image and highlight the product name. \
			             If the image has text, return the extracted text; otherwise, return False. also extract the FERT-Artikel-Nummer vom PO"
			        ]
			        
			        try:
				        response = model.generate_content(prompt, stream=False)
				        response_text =response.text
				        textual_data =response_text.split("\n")
			        except Exception as e:
			        	return  "API error.", True, stored_content, False , []

			        if(len(textual_data) < 5):
			            continue
			            
			           
			        
			        image_artkl = ""
			        flag = False
			        for j, data in enumerate(textual_data):
			            pattern = r"\*\*(.*?)\*\*"
			            matches = re.findall(pattern, data)
			            
			            if(len(matches)>0 and flag==False):
			                image_results.append(matches[0])
			                flag=True
			            
			            if(data.startswith("Batch-No")):
			                image_artkl = textual_data[j+1]
			                image_results.append(image_artkl)
			                break
			    print(image_results)
			          
			    if(len(image_results) > 2):
			        if(image_results[1] == image_results[3] and image_results[1] == image_results[5]):
			            image_results.append("Matched")
			        else:
			            image_results.append("Not Mactched")
			    else:
			        image_results.extend(["", "Not Mactched"])
			     
			    
			    images_list.append(image_results)
			    
			    if(page_number == 6):
			        break

			data = pd.DataFrame(images_list, columns=["PO number","FERT-Artikel", "Image 1","img1-FERT-Artikel" ,  "Image 2", "img2-FERT-Artikel","Result"])
			print(data.head(10))

			ls2 = []
			ls2.append(html.Div([
				dash_table.DataTable(
				    style_table={'height': '400px','overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
				    data=data.to_dict('records'),
				    columns=[{"name": i, "id": i} for i in data.columns],
				    #editable=True,
				    #filter_action="native",
				    sort_action="native",
				    style_data={
		            'backgroundColor': 'white',
		            
		        	},
				    #page_action="native",
				    style_header={
				        'backgroundColor': 'darkslategrey',
				        'color': 'lightcyan',
				        'fontWeight': 'bold',
				        'textAlign': 'center',
				        'border': '1px solid black'
				    }),html.Hr()])
				)


			# Display the extracted text
			return  "PDF processed.", True, content, True , ls2
	else:	
		return html.Div("No file uploaded yet."), pd.DataFrame().to_dict('records'), [], True, True




# App layout
app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	#html.Div(id='page-content'),
	dcc.Download(id="download-dataframe-csv"),

	html.Div(id='page-1-content', style={'display': 'block'}, children=[
	    page_1_layout
	]),

	html.Div(id='page-2-content', style={'display': 'none'}, children=[
	    page_2_layout
	]),
	html.Div(id='page-4-content', style={'display': 'none'}, children=[
	    page_4_layout
	]),

	html.Div(id='page-3-content', style={'display': 'none'}, children=[
	    page_3_layout
	]),
	html.Div(id='page-5-content', style={'display': 'none'}, children=[
	    page_5_layout
	]),
	html.Div(id='page-6-content', style={'display': 'none'}, children=[
		dcc.Store(id='stored-data-6'),
		dcc.Store(id='stored-data-7'),
	    page_6_layout
	]),
	html.Div(id='page-7-content', style={'display': 'none'}, children=[
		dcc.Store(id='stored-data-8'),
		dcc.Store(id='stored-data-9'),
	    page_7_layout
	])

	

	])


@app.callback(
    [Output('page-1-content', 'style'),
     Output('page-2-content', 'style'),
     Output('page-3-content', 'style'),
     Output('page-4-content', 'style'),
     Output('page-5-content', 'style'),
     Output('page-6-content', 'style'),
     Output('page-7-content', 'style'),

     Output('success', 'children'),

     
     ],
    [Input('url', 'pathname'),
    Input('input-text1', 'value'),
    Input('input-text2', 'value'),
    ]
)
def display_page(pathname,id_, pass_):

    if(id_ == "log" and pass_ == "C3asar!"):#C3asar!

        if pathname == '/page-2':
            return {'display': 'block'}, {'display': 'none'} ,{'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},""
        elif(pathname == "/page1"):
            return {'display': 'none'}, {'display': 'block'} ,{'display': 'none'},{'display': 'none'},{'display': 'none'}, {'display': 'none'},{'display': 'none'},""
        elif(pathname == "/page-3"):
            return {'display': 'none'}, {'display': 'none'} ,{'display': 'none'}, {'display': 'block'},{'display': 'none'},{'display': 'none'},{'display': 'none'},""
        elif(pathname == "/page_input"):
            return {'display': 'none'}, {'display': 'none'} ,{'display': 'none'}, {'display': 'none'},{'display': 'block'},{'display': 'none'},{'display': 'none'},"" 
        elif(pathname == "/page_filter"):
            return {'display': 'none'}, {'display': 'none'} ,{'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'none'},"" 
        elif(pathname == "/image"):
            return {'display': 'none'}, {'display': 'none'} ,{'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'block'},"" 
        else:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'none'}, {'display': 'none'},{'display': 'none'},""
    elif(id_ == "" and pass_ == ""):
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},html.H6("Bitte ID und Passwort eintragen",style={"color":"black"})
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},""


app.title = "LogFilter"


app.css.append_css({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
})


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True, port="8090")




