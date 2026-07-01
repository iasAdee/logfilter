
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
   	#Output('status3', 'children'),
    Input('stored-data-5', 'data'),
    Input('search-input9', 'value'),
    Input('search-input10', 'value'),
    
) 
def get_new_Data(data,order_id, client_id):

	data = pd.DataFrame(data)

	if(data.empty):
		return (f"data not recived", {}, {},{},{}, [],[])

	if(len(data) > 0):

		#print(data)


		row_1_values = data.iloc[1].astype(str).tolist()  

		expected_columns = ["Menge in ErfassME", "Kunde", "Buch.dat.","LOrt"]

		#expected_columns = ["order_id", "date", "value", "client"]
		missing_columns = [col for col in expected_columns if col not in row_1_values]

		if(len(missing_columns) > 0):
		    message = "Missing columns: " + ", ".join(missing_columns)
		    default_return = (f"data recived {message}", {}, {},{},{}, [],[])
		    return default_return


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
			return "Erhaltene Daten zum verarbeiten", fig1, fig2, fig3, fig4, options,options2#,""
	else:
		return "data not recived yet for processing", {}, {},{},{}, [],[]#, ""