import pandas as pd
import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import re
import numpy as np
import json

class DataPreprocessing:
	def __init__(self, data):
		self.data = data

	def clac_2(self):
		data_req = self.data[["SalesOrder", "Werk", "KomplettLF_KZ", "Summe von BrGew_Offen", "WE_PLZ"]]

		data_req = data_req[data_req["Summe von BrGew_Offen"].notna()]
		data_req = data_req.reset_index(drop=True)

		#print(data_req.isnull().sum())

		#print(data_req)

		#print(data_req)
		#data_req["Summe von BrGew_Offen"] = data_req["Summe von BrGew_Offen"].astype(int)
		ls = []
		for i in range(len(data_req)):
			x = data_req["KomplettLF_KZ"][i]
			so = data_req["SalesOrder"][i]
			we = data_req["WE_PLZ"][i]
			wr = data_req["Werk"][i]


			if(x == "X"):
			    dat = data_req[data_req["SalesOrder"] == so]
			    sum_tocheck = sum(dat["Summe von BrGew_Offen"])
			    if(wr == "DE01" or we == "DE10"):
			        if(sum_tocheck < 50):
			            ls.append("TOF")
			        if(sum_tocheck > 50 and sum_tocheck < 2500):
			            ls.append("Dachser")
			        if(sum_tocheck >= 2500):
			            ls.append("Direkt")
			    else:
			        if(sum_tocheck < 80):
			            ls.append("TOF")
			        if(sum_tocheck > 80 and sum_tocheck < 2500):
			            ls.append("Dachser")
			        if(sum_tocheck >= 2500):
			            ls.append("Direkt")
			else:
			    sum_tocheck = data_req["Summe von BrGew_Offen"][i]

			    if(wr == "DE01" or we == "DE10"):
			        if(sum_tocheck < 50):
			            ls.append("TOF")
			        if(sum_tocheck > 50 and sum_tocheck < 2000):
			            ls.append("Dachser")
			        if(sum_tocheck >= 2000):
			            ls.append("Direkt")
			    else:
			        if(sum_tocheck < 80):
			            ls.append("TOF")
			        if(sum_tocheck > 80 and sum_tocheck < 2000):
			            ls.append("Dachser")
			        if(sum_tocheck >= 2000):
			            ls.append("Direkt")
			            
		    #print(i, x, len(ls), sum_tocheck)

		data_req["new_col"] = ls


		ls = []
		ls.append(html.Div([
		dash_table.DataTable(
		    style_table={'height': '400px','overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=data_req.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in data_req.columns],
		    #editable=True,
		    #filter_action="native",
		    sort_action="native",
		    style_data={
            'backgroundColor': 'lightcyan',
            
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

		fig = go.Figure()

		value_counts = data_req['new_col'].value_counts()

		colors = ['darkkhaki', 'indianred', 'lightseagreen']
		# Create the bar plot with Plotly
		fig = go.Figure(data=[
		    go.Bar(
		        x=value_counts.index,  # Bar labels
		        y=value_counts.values,  # Bar heights
		        marker_color=colors,
		        text=value_counts.values,  # Text annotations on bars
		        textposition='inside'  # Position annotations outside the bars
		    )
		])

		# Update layout to match the styling of the Matplotlib plot
		fig.update_layout(
			title='Picks Distribution',
			xaxis_title='Selected values',
			yaxis_title='Summe',
			template='plotly_white',
			plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',
			height=350,
		)


		return data_req.to_dict('records'), ls, fig




	def get_calculated_results(self):

		def get_number(sentence):
		    match1 = re.search(r'\((\d+)\)\s*KG', sentence)
		    if match1:
		        number1 = match1.group(1)
		        return int(number1)
		    else:
		        match2 = re.search(r'HO(\d+)KG', sentence)
		        if match2:
		            number2 = match2.group(1)
		            return int(number2)
		        else:
		            return 0

		def get_number2(sentence):
		    pattern = r'(\d+)x(\d+)'
		    matches1 = re.findall(pattern, sentence)
		    for match in matches1:
		        return match[0], match[1]
		    else:
		        return 0, 0

		"""def make_sender_dict(data):
								    all_senders = set(data["AG-ID"])
								    sender_dict = {}
								    for sender in all_senders:
								        first = data[data["AG-ID"] == sender]
						
								        recivers =first["WE-ID"]
								        same_occurances = list(recivers).count(sender)
								        total_recivers = len(recivers)
								        other = abs(total_recivers - same_occurances)
						
								        sender_dict[sender] = [other, same_occurances]
									    
								    return sender_dict"""


		data_required = self.data[["Auftragsmenge_Offen", "AME", "BME", "BereitStellDat", "Zähler",
		                      "MatBez", "MatNr", "Auftragsmenge_bereits_geliefert",
		                     "SalesOrder", "Werk", "KomplettLF_KZ", "Summe von BrGew_Offen", "WE_PLZ"]]


		ls = []
		for i, val in enumerate(data_required["Auftragsmenge_Offen"]):
		    ls.append(float(str(val).strip().replace(",", ".").replace(".","")))

		data_required["Auftragsmenge_Offen"] = ls

		for i in range(len(data_required)):
			data_required["SKU_Zähler"] = 1


		with open("data.json", "r") as json_file:
			loaded_data = json.load(json_file)

		

		data_collection = []
		data_collection2 = []
		ls2 = []

		for i in range(len(data_required)):
		    ame = data_required["AME"][i]
		    bme = data_required["BME"][i]
		    order = data_required["Auftragsmenge_Offen"][i]

		    pallet = data_required["Zähler"][i]
		    date = data_required["BereitStellDat"][i]
		    #matrial = data_required["Material"][i]
		    MatBez = data_required["MatBez"][i]
		    MatNr = str(data_required["MatNr"][i])
		    SKU_Zähler = data_required["SKU_Zähler"][i]

		    
		    
		    if(MatNr not in loaded_data.keys()):
		    	continue

		    loaded_data
		    pallet = loaded_data[MatNr]

		    ls = []
		    nodata = False

		    if(ame == "ST" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]

		        if(pd.isna(order) or pd.isna(pallet) or pd.isna(pallet)):
		            continue
		        if(order < pallet):
		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order, 0])
		        else:
		            pallet_ = int(order / pallet)
		            pieces = abs(int(order / pallet) * pallet - order)

		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "KAR" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]
		        pallet_val = data_required["SKU_Zähler"][i]

		        if(pd.isna(order) or pd.isna(pallet) or pd.isna(pallet_val)):
		            continue

		        comparison = pallet / pallet_val
		        if(order < comparison):
		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order, 0])
		        else:
		            pallet_ = int(order / comparison)
		            pieces = abs(int(order / comparison) * comparison - order)

		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "KG" and bme == "KG"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]
		        if(pd.isna(order) or pd.isna(pallet)):
		            continue

		        text = data_required["MatBez"][i]
		        kg = get_number(text)
		        if(kg == 0):
		            continue
		        else:
		            order_actual = order / kg
		            pallet_actual = pallet / kg

		            if(order_actual < pallet_actual):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order_actual, 0])
		            else:
		                pallet_ = int(order_actual / pallet_actual)
		                pieces = abs(int(order_actual / pallet_actual) * pallet_actual - order_actual)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "KG" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]
		        if(pd.isna(order) or pd.isna(pallet)):
		            continue

		        text = data_required["MatBez"][i]
		        kg = get_number(text)
		        if(kg == 0):
		            continue
		        else:
		            req_num = pallet * kg
		            if(order < req_num):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order, 0])
		            else:
		                pallet_ = int(order / req_num)
		                pieces = abs(int(order / req_num) * req_num - order)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])

		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "L" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        com = float(data_required['Auftragsmenge_bereits_geliefert'][i])
		        
		        text = data_required["MatBez"][i]
		        n1, n2 = get_number2(text)

		        if(com != 0):
		            print(type(com), com)

		            num = int(order / com)
		            if(num < pallet):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, int(num), 0])
		            else:
		                pallet_ = int(num / pallet)
		                pieces = abs(int(num / pallet) * pallet - num)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		            data_collection2.append(ls[0])

		        elif(n1 != 0 and n2 != 0):
		            nu = (int(n1) * int(n2)) / 1000
		            num = int(order / nu)
		            pallet1 = pallet / nu
		            if(num < pallet1):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, int(num), 0])
		            else:
		                pallet_ = int(num / pallet)
		                pieces = abs(int(num / pallet) * pallet - num)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		            data_collection2.append(ls[0].copy())
		            nodata = True


		    if(nodata == True):
		        #nls = ls[0].copy()
		        #data_collection2.append(nls)

		        x = data_required["KomplettLF_KZ"][i]
		        so = data_required["SalesOrder"][i]
		        we = data_required["WE_PLZ"][i]
		        wr = data_required["Werk"][i]


		        if(x == "X"):
		            dat = data_required[data_required["SalesOrder"] == so]
		            sum_tocheck = sum(dat["Summe von BrGew_Offen"])
		            if(wr == "DE01" or we == "DE10"):
		                if(sum_tocheck < 50):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 50 and sum_tocheck < 2500):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck >= 2500):
		                    ls[0].extend([x, so, we, wr,"Direkt"])
		            else:
		                if(sum_tocheck < 80):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 80 and sum_tocheck < 2500):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck >= 2500):
		                    ls[0].extend([x, so, we, wr,"Direkt"])
		        else:
		            sum_tocheck = self.data["Summe von BrGew_Offen"][i]

		            if(wr == "DE01" or we == "DE10"):
		                if(sum_tocheck < 50):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 50 and sum_tocheck < 2000):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck >= 2000):
		                    ls[0].extend([x, so, we, wr,"Direkt"])
		            else:
		                if(sum_tocheck < 80):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 80 and sum_tocheck < 2000):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck >= 2000):
		                    ls[0].extend([x, so, we, wr,"Direkt"])

		        data_collection.append(ls[0])

		#print(data_collection2)
		datahalf = pd.DataFrame(data_collection2, columns=["AME", "BME", "com", "Auftragsmenge_Offen",
		                                                      "Zähler", "BereitStellDat","SKU_Zähler",
		                                                      "MatBez", "MatNr", "Picks", "Pallets"])

		datextracted = pd.DataFrame(data_collection, columns=["AME", "BME", "com", "Auftragsmenge_Offen",
		                                                      "Zähler", "BereitStellDat","SKU_Zähler",
		                                                      "MatBez", "MatNr", "Picks", "Pallets", "KomplettLF_KZ", "SalesOrder", "WE_PLZ", "Werk", "new_col"])

		"""datextracted = datextracted[["AME", "BME", "com", "Auftragsmenge_Offen",
								                                                      "Zähler", "BereitStellDat",
								                                                       "MatNr", "Picks", "Pallets", "KomplettLF_KZ", "SalesOrder", "WE_PLZ", "Werk", "new_col"]]
						
						
								datahalf = datahalf[["AME", "BME", "com", "Auftragsmenge_Offen",
								                                                      "Zähler", "BereitStellDat","SKU_Zähler",
								                                                       "MatNr", "Picks", "Pallets"]]                                                   """
		ls = []
		ls.append(html.Div([
		dash_table.DataTable(
		    style_table={'height': '400px', 'overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=datahalf.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in datahalf.columns],
		    #editable=True,
		    filter_action="native",
		    sort_action="native",
		    #page_action="native",
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


		ls2 = []
		ls2.append(html.Div([
		dash_table.DataTable(
		    style_table={'height': '400px', 'overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=datextracted.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in datextracted.columns],
		    #editable=True,
		    filter_action="native",
		    sort_action="native",
		    #page_action="native",
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

		fig = go.Figure()


		value_counts = datahalf['AME'].value_counts()
		colors = ['darkkhaki', 'indianred', 'lightseagreen', 'mediumpurple']
		text_positions = ['inside' if y >= 200 else 'outside' for y in value_counts.values]

		# Create the bar plot with Plotly
		fig = go.Figure(data=[
		    go.Bar(
		        x=value_counts.index,  # Bar labels
		        y=value_counts.values,  # Bar heights
		        marker_color = colors,
		        text=value_counts.values,  # Text annotations on bars
		        textposition=text_positions  # Position annotations outside the bars
		    )
		])

		# Update layout to match the styling of the Matplotlib plot
		fig.update_layout(
		    title='AME Distribution',
		    xaxis_title='Selected values',
		    yaxis_title='Summe',
		    template='plotly_white',
		    plot_bgcolor='lightcyan',
		    paper_bgcolor='lightcyan',
		    height=350,
		)


		fig2 = go.Figure()

		value_counts = datahalf['BME'].value_counts()

		#print(value_counts)

		colors = ['darkkhaki', 'indianred']
		text_positions = ['inside' if y >= 100 else 'outside' for y in value_counts.values]

		# Create the bar plot with Plotly
		fig2 = go.Figure(data=[
		    go.Bar(
		        x=value_counts.index,  # Bar labels
		        y=value_counts.values,  # Bar heights
		        marker_color = colors,
		        text=value_counts.values,  # Text annotations on bars
		        textposition=text_positions  
		    )
		])

		# Update layout to match the styling of the Matplotlib plot
		fig2.update_layout(
			title='BME Distribution',
			xaxis_title='Selected values',
			yaxis_title='Summe',
			template='plotly_white',
			plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',
			height=350,

			# Set axis labels and title color to white
			font=dict(color='black'),
		)


		
		#data_required["BereitStellDat"] = pd.to_datetime(data_required["BereitStellDat"])
		datahalf["date"] = pd.to_datetime(datahalf["BereitStellDat"], format="%d.%m.%Y", errors="coerce")

		datahalf = datahalf.sort_values(by="date")

		# Create a bar chart using Plotly Express
		fig3 = px.bar(
			datahalf, 
			x="date", 
			y="Picks", 
			labels={"date": "Datum", "Picks": "Picks"},
			title="Picks Bar Chart"
		)

		# Update layout to adjust x-axis labels
		fig3.update_layout(
			xaxis_tickformat="%Y-%m-%d", # Format for the date display
			xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
			plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',
			height=350,
		)


		# Create a bar chart using Plotly Express
		fig4 = px.bar(
			datahalf, 
			x="date", 
			y="Pallets", 
			labels={"date": "Datum", "Picks": "Pallets"},
			title="Pallets Bar Chart"
		)

		# Update layout to adjust x-axis labels
		fig4.update_layout(
			xaxis_tickformat="%Y-%m-%d", # Format for the date display
			xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
			plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',
			height=350,
		)


		#datextracted["date"] = pd.to_datetime(datextracted["BereitStellDat"])
		datextracted["date"] = pd.to_datetime(datextracted["BereitStellDat"], format="%d.%m.%Y", errors="coerce")
		datextracted = datextracted.sort_values(by="date")

		print(datextracted)

		# Create a bar chart using Plotly Express
		fig5 = px.bar(
			datextracted, 
			x="date", 
			y="Picks", 
			color="new_col", 
			labels={"date": "Datum", "Picks": "Picks"},
			title="Picks Bar Chart"
		)

		# Update layout to adjust x-axis labels
		fig5.update_layout(
			xaxis_tickformat="%Y-%m-%d", # Format for the date display
			xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
			height=350,
			plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',
		)


		# Create a bar chart using Plotly Express
		fig6 =px.bar(
			datextracted, 
			x="date", 
			y="Pallets", 
			color="new_col",
			labels={"date": "Datum", "Picks": "Pallets"},
			title="Pallets Bar Chart"
		)

		# Update layout to adjust x-axis labels
		fig6.update_layout(
			xaxis_tickformat="%Y-%m-%d", # Format for the date display
			xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
			height=350,
			plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',
		)

		return ls, ls2, datahalf.to_dict('records'), datextracted.to_dict('records') , fig, fig2, fig3, fig4, fig5, fig6


	def get_absenders(self):

		def make_sender_dict(data):

			#print(data.columns)
			all_senders = set(data["AG-ID"])
			sender_dict = {}
			for sender in all_senders:
			    first = data[data["AG-ID"] == sender]

			    recivers =first["WE-ID"]
			    same_occurances = list(recivers).count(sender)
			    total_recivers = len(recivers)
			    other = abs(total_recivers - same_occurances)

			    sender_dict[sender] = [other, same_occurances]
			    
			return sender_dict


		sender_dict = make_sender_dict(self.data)

		sorted_data = sorted(sender_dict.items(), key=lambda item: item[1][0] + item[1][1], reverse=True)

		keys_sorted = [k for k, v in sorted_data][:50]
		values_1_sorted = [v[0] for k, v in sorted_data][:50]
		values_2_sorted = [v[1] for k, v in sorted_data][:50]


		# Create the x axis positions
		x = np.arange(len(keys_sorted))
		width = 0.4

		# Create the Plotly figure
		fig = go.Figure()

		# Add the first bar for "Other Receivers"
		fig.add_trace(go.Bar(
		    x=[str(d) for d in keys_sorted],
		    y=values_1_sorted,
		    name='Andere',
		    marker_color='slateblue',
		    width=width
		))

		fig.add_trace(go.Bar(
		    x=[str(d) for d in keys_sorted],
		    y=values_2_sorted,
		    name='Eigene',
		    marker_color='lightseagreen',
		    width=width
		))


		# Update the layout
		fig.update_layout(
		    title='Top 50 abSenders',
		    xaxis_title='abSenders',
		    yaxis_title='Gesmate gesendete',
		    barmode='group',  
		    xaxis_tickangle=-90,  
		    template='plotly_white',
		    legend_title='Type',
		    plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',

		)

		# Show the figure
		return fig

	def make_customized_plot(self, user):
		def make_sender_dict(data):

			#print("from functions")
			#print(data.columns)
			#print("from functions")


			all_senders = set(data["AG-ID"])
			sender_dict = {}


			for sender in all_senders:
			    first = data[data["AG-ID"] == sender]

			    recivers =first["WE-ID"]
			    same_occurances = list(recivers).count(sender)
			    total_recivers = len(recivers)
			    other = abs(total_recivers - same_occurances)

			    sender_dict[sender] = [other, same_occurances]
			    
			return sender_dict


		sender_dict = make_sender_dict(self.data)

		if(int(user) not in sender_dict.keys()):
			return {}
		val1 = sender_dict[int(user)][0]
		val2 = sender_dict[int(user)][1]


		colors = ['slateblue', 'lightseagreen']
		ls = ["Andere", "Eigene"]
		ls2 = [val1, val2]

		df = pd.DataFrame({'Keys': ls, 'Values': ls2})

		fig = go.Figure(data=[
		    go.Bar(
		        x=df.Keys,  # Bar labels
		        y=df.Values,  # Bar heights
		        marker_color = colors,
		        text=df.Values,  # Text annotations on bars
		        #textposition=text_positions  
		    )
		])



				# Update layout to adjust x-axis labels
		fig.update_layout(
			xaxis_tickformat="%Y-%m-%d", # Format for the date display
			xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
			plot_bgcolor='lightcyan',
			paper_bgcolor='lightcyan',
			

		)

		# Show the figure
		return fig
        



