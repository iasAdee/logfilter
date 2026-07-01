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

        #print(self.data.columns)
        data_req = self.data[["verursach_", "werk", "klf", "brutto", "plzwempf","versandbed"]]

        #data_req = data_req[data_req["brutto"].notna()]
        data_req = data_req.reset_index(drop=True)

        #print("I am inside calc_2")
        #print(data_req)
        ls = []
        for i in range(len(data_req)):
            x = data_req["klf"][i]
            so = data_req["verursach_"][i]
            
            #we = data_req["plzwempf"][i] #postal code (we_plz) will not use it in this graph
            wr = data_req["werk"][i] # werk
            versandbed = data_req["versandbed"][i] # werk

            if(versandbed == 35 or versandbed == 36 or versandbed == 37):
                #no toff we only  need to check  it to Dachser and diretk with same formala below. 
                if(x == "X"):
                    dat = data_req[data_req["verursach_"] == so]
                    sum_tocheck = sum(dat["brutto"])

                    if(wr == "DE01" or wr == "DE10"):
                        if(sum_tocheck < 50):
                            ls.append("Dachser") #
                        elif(sum_tocheck < 2500):
                            ls.append("Direkt")
                        elif(sum_tocheck >=2500):
                            ls.append("Dachser")
                    else:
                        if(sum_tocheck < 80):
                            ls.append("Dachser") # correct
                        if(sum_tocheck > 80 and sum_tocheck < 2500):
                            ls.append("Direkt") # correct
                        if(sum_tocheck >= 2500):
                            ls.append("Dachser")
                else:
                    sum_tocheck = data_req["brutto"][i] #singular value

                    if(wr == "DE01" or wr == "DE10"):
                        if(sum_tocheck < 50):
                            ls.append("Dachser")
                        if(sum_tocheck > 50 and sum_tocheck < 2000):
                            ls.append("Direkt")
                        if(sum_tocheck >= 2500):
                            ls.append("Dachser")
                    else:
                        if(sum_tocheck < 80):
                            ls.append("Dachser")
                        if(sum_tocheck > 80 and sum_tocheck < 2000):
                            ls.append("Direkt")
                        if(sum_tocheck >= 2500):
                            ls.append("Dachser")
            elif(x == "X"):
                dat = data_req[data_req["verursach_"] == so]
                sum_tocheck = sum(dat["brutto"])

                if(wr == "DE01" or wr == "DE10"):
                    if(sum_tocheck < 50):
                        ls.append("TOF") # correct
                    if(sum_tocheck > 50 and sum_tocheck < 2500):
                        ls.append("Dachser") # correct
                    if(sum_tocheck >= 2500):
                        ls.append("Direkt") # correct
                else:
                    if(sum_tocheck < 80):
                        ls.append("TOF") # correct
                    if(sum_tocheck > 80 and sum_tocheck < 2500):
                        ls.append("Dachser") # correct
                    if(sum_tocheck >= 2500):
                        ls.append("Direkt")
            else:
                sum_tocheck = data_req["brutto"][i] #singular value

                if(wr == "DE01" or wr == "DE10"):
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
                        
        data_req["Gesamt"] = ls

        fig = go.Figure()

        value_counts = data_req['Gesamt'].value_counts()
        colors = ['#F5B323', 'dimgrey', 'gainsboro']
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
            xaxis_title='Anzahl',
            yaxis_title='Summe',
            template='plotly_white',
            height=350,
        )


        return data_req.to_dict('records'), fig


    def get_calculated_results(self, input=False):

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


        #print(self.data.columns())
        if(input  == False):
            data_required = self.data[["offene_mng", "me", "bme", "bereit_dat", "zhler",
                                  "positionsbezeichnung", "material", "gelmenge",
                                 "verursach_", "werk", "klf", "brutto", "plzwempf","best_mg","namewarenempfnger","ortwempf","kzazu"]]
        else:
            data_required = self.data[["offene_mng", "me", "bme", "bereit_dat",
                                  "positionsbezeichnung", "material", "gelmenge","best_mg","namewarenempfnger","ortwempf","kzazu",
                                  "werk"]]
    

        for i in range(len(data_required)):
            data_required["SKU_Zähler"] = 1
            data_required["zhler"] = 1


        with open("data.json", "r") as json_file:
            loaded_data = json.load(json_file)


        with open("data2.json", "r") as json_file:
            loaded_data2 = json.load(json_file)

        
        data_collection = []
        data_collection2 = []
        ls2 = []

        keys_to_check=list(loaded_data2.keys())#+list(loaded_data.keys())


        data_required["material"] = data_required["material"].astype(str)
        #print("Length of data before:", len(data_required))
        data_required = data_required[data_required["material"].isin(keys_to_check)].reset_index(drop=True)
        #print("Length of data after:", len(data_required))

        for i in range(len(data_required)):

            ame = data_required["me"][i].strip()
            bme = data_required["bme"][i].strip()
            order = data_required["offene_mng"][i]

            

            pallet = data_required["zhler"][i]
            #print("order: ", order, "zheler: ", pallet, type(order), type(pallet))
            date = data_required["bereit_dat"][i]
            positionsbezeichnung = data_required["positionsbezeichnung"][i]
            material = str(data_required["material"][i])
            SKU_Zähler = data_required["SKU_Zähler"][i]
            wr = data_required["werk"][i]
            ab = data_required["best_mg"][i]
            wn = data_required["namewarenempfnger"][i]
            ws = data_required["ortwempf"][i]
            kzu =data_required["kzazu"][i]



            kzu_check_zero = data_required["brutto"][i]

            if(pd.isna(material) or material == "nan"):
                continue
            else:
                material = str(int(float(material)))
            
            if(material not in loaded_data.keys()):
                #pallet = data_required["zhler"][i]
                continue

            if(material in loaded_data2.keys() and material in loaded_data.keys()):
                pallet = loaded_data[material] #/ loaded_data2[material]
                if(ame == "ST" and bme == "ST"):
                    order = data_required["offene_mng"][i]
                    #order = order/loaded_data2[material]
                    pallet = loaded_data[material]# / loaded_data2[material]
                if(ame == "KG" and bme == "KG"):
                    pallet = loaded_data[material]

            elif(material in loaded_data.keys()):
                pallet = loaded_data[material]
            else:
                continue
                #pallet = data_required["zhler"][i]

            ls = []
            nodata = False

            kzu_check_zero = 0 if pd.isna(kzu_check_zero) else kzu_check_zero

            if kzu_check_zero == 0:
                com = data_required['gelmenge'][i]
                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, 0, 0,wr,ab,wn,ws,kzu])
            elif(ame == "ST" and bme == "ST"):
                com = data_required['gelmenge'][i]

                if(pd.isna(order) or pd.isna(pallet) or pd.isna(pallet)):
                    continue
                if(order < pallet):
                    ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, order, 0,wr,ab,wn,ws,kzu])
                else:
                    pallet_ = int(order / pallet)
                    pieces = abs(int(order / pallet) * pallet - order)

                    ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(pieces), pallet_,wr,ab,wn,ws,kzu])
                data_collection2.append(ls[0].copy())
                nodata = True
            elif(ame == "KAR" and bme == "ST"):
                order = data_required["offene_mng"][i]
                
                com = data_required['gelmenge'][i]
                pallet_val = data_required["SKU_Zähler"][i]

                if(pd.isna(order) or pd.isna(pallet) or pd.isna(pallet_val)):
                    continue

                comparison = pallet / pallet_val
                if(order < comparison):
                    ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, order, 0,wr,ab,wn,ws,kzu])
                else:
                    pallet_ = int(order / comparison)
                    pieces = abs(int(order / comparison) * comparison - order)

                    ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(pieces), pallet_,wr,ab,wn,ws,kzu])
                data_collection2.append(ls[0].copy())
                nodata = True
            elif(ame == "KG" and bme == "KG"):
                order = data_required["offene_mng"][i]

                com = data_required['gelmenge'][i]
                if(pd.isna(order) or pd.isna(pallet)):
                    #print("Getting continued: ",order, pallet)
                    continue

                text = data_required["positionsbezeichnung"][i]
                kg = get_number(text)
                if(kg == 0):
                    continue
                else:
                    order_actual = order / kg #300000/15 = 20000
                    pallet_actual = pallet / kg #450/15 = 30 

                    if(order_actual < pallet_actual):
                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, order_actual, 0,wr,ab,wn,ws,kzu])
                    else:
                        #print(material, pallet_actual)
                        pallet_ = int(order_actual / pallet_actual)
                        #print(pallet_)
                        pieces = abs(int(order_actual / pallet_actual) * pallet_actual - order_actual)

                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(pieces), pallet_,wr,ab,wn,ws,kzu])
                data_collection2.append(ls[0].copy())
                nodata = True

            elif(ame == "KG" and bme == "ST"):
                order = data_required["offene_mng"][i]
                
                com = data_required['gelmenge'][i]
                if(pd.isna(order) or pd.isna(pallet)):
                    continue

                text = data_required["positionsbezeichnung"][i]
                kg = get_number(text)
                if(kg == 0):
                    continue
                else:
                    req_num = pallet * kg
                    if(order < req_num):
                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, order, 0,wr,ab,wn,ws,kzu])
                    else:
                        pallet_ = int(order / req_num)
                        pieces = abs(int(order / req_num) * req_num - order)

                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(pieces), pallet_,wr,ab,wn,ws,kzu])

                data_collection2.append(ls[0].copy())
                nodata = True
            elif(ame == "L" and bme == "ST"):
                order = data_required["offene_mng"][i]
                com = float(data_required['gelmenge'][i])
                
                text = data_required["positionsbezeichnung"][i]
                n1, n2 = get_number2(text)

                if(com != 0):
                    #print(type(com), com)

                    num = int(order / com)
                    if(num < pallet):
                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(num), 0,wr,ab,wn,ws,kzu])
                    else:
                        pallet_ = int(num / pallet)
                        pieces = abs(int(num / pallet) * pallet - num)

                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(pieces), pallet_,wr,ab,wn,ws,kzu])
                    data_collection2.append(ls[0])

                elif(n1 != 0 and n2 != 0):
                    nu = (int(n1) * int(n2)) / 1000
                    num = int(order / nu)
                    pallet1 = pallet / nu
                    if(num < pallet1):
                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(num), 0,wr,ab,wn,ws,kzu])
                    else:
                        pallet_ = int(num / pallet)
                        pieces = abs(int(num / pallet) * pallet - num)

                        ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, positionsbezeichnung, material, int(pieces), pallet_,wr,ab,wn,ws,kzu])
                    data_collection2.append(ls[0].copy())
                    nodata = True


            if(nodata == True and input == False):
                #nls = ls[0].copy()
                #data_collection2.append(nls)

                x = data_required["klf"][i]
                so = data_required["verursach_"][i]
                we = data_required["plzwempf"][i]
                wr = data_required["werk"][i]


                if(x == "X"):
                    dat = data_required[data_required["verursach_"] == so]
                    sum_tocheck = sum(dat["brutto"])
                    if(wr == "DE01" or we == "DE10"):
                        if(sum_tocheck < 50):
                            ls[0].extend([x, so, we,"TOF"])
                        if(sum_tocheck > 50 and sum_tocheck < 2500):
                            ls[0].extend([x, so, we,"Dachser"])
                        if(sum_tocheck >= 2500):
                            ls[0].extend([x, so, we,"Direkt"])
                    else:
                        if(sum_tocheck < 80):
                            ls[0].extend([x, so, we,"TOF"])
                        if(sum_tocheck > 80 and sum_tocheck < 2500):
                            ls[0].extend([x, so, we,"Dachser"])
                        if(sum_tocheck >= 2500):
                            ls[0].extend([x, so, we,"Direkt"])
                else:
                    sum_tocheck = self.data["brutto"][i]

                    if(wr == "DE01" or we == "DE10"):
                        if(sum_tocheck < 50):
                            ls[0].extend([x, so, we,"TOF"])
                        if(sum_tocheck > 50 and sum_tocheck < 2000):
                            ls[0].extend([x, so, we,"Dachser"])
                        if(sum_tocheck >= 2000):
                            ls[0].extend([x, so, we,"Direkt"])
                    else:
                        if(sum_tocheck < 80):
                            ls[0].extend([x, so, we,"TOF"])
                        if(sum_tocheck > 80 and sum_tocheck < 2000):
                            ls[0].extend([x, so, we,"Dachser"])
                        if(sum_tocheck >= 2000):
                            ls[0].extend([x, so, we,"Direkt"])

                data_collection.append(ls[0])

        #print(data_collection2)

        if(input == False):
            datahalf = pd.DataFrame(data_collection2, columns=["me", "bme", "gelmenge", "offene_mng",
                                                                  "zhler", "bereit_dat","SKU_Zähler",
                                                                  "positionsbezeichnung", "material", "Picks", "Pallets","werk","best_mg","namewarenempfnger","ortwempf","kzu"])

            datextracted = pd.DataFrame(data_collection, columns=["me", "bme", "gelmenge", "offene_mng",
                                                                  "zhler", "bereit_dat","SKU_Zähler",
                                                                  "positionsbezeichnung", "material", "Picks", "Pallets","werk","best_mg","namewarenempfnger","ortwempf","kzu", "klf", "verursach_", "plzwempf", "Gesamt"])

        else:
            datahalf = pd.DataFrame(data_collection2, columns=["me", "bme", "gelmenge", "offene_mng",
                                                                  "zhler", "bereit_dat","SKU_Zähler",
                                                                  "positionsbezeichnung", "material", "Picks", "Pallets","werk","best_mg","namewarenempfnger","ortwempf","kzu"])

        """datextracted = datextracted[["me", "bme", "com", "offene_mng",
                                                                                      "zhler", "bereit_dat",
                                                                                       "material", "Picks", "Pallets", "klf", "verursach_", "plzwempf", "werk", "new_col"]]
                        
                        
                                datahalf = datahalf[["me", "bme", "com", "offene_mng",
                                                                                      "zhler", "bereit_dat","SKU_Zähler",
                                                                                       "material", "Picks", "Pallets"]]                                                   """
        ls = []

        #print(datahalf)
        #print(datextracted)


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
            'backgroundColor': 'white',
            
            },
            style_header={
                'backgroundColor': 'darkslategrey',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'border': '1px solid black'
            }),html.Hr()])
        )

        if(input == False):
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
                'backgroundColor': 'white',
                
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


        value_counts = datahalf['me'].value_counts()
        colors = ['#F5B323', 'dimgrey', 'black', 'gainsboro']
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
            title='me Distribution',
            xaxis_title='Anzahl',
            yaxis_title='Summe',
            template='plotly_white',
            height=350,
        )


        fig10 = go.Figure()

        value_counts = data_required['werk'].value_counts()
        text_positions = ['inside' if y >= 200 else 'outside' for y in value_counts.values]

        # Create the bar plot with Plotly
        fig10 = go.Figure(data=[
            go.Bar(
                x=value_counts.index,  # Bar labels
                y=value_counts.values,  # Bar heights
                #marker_color = colors,
                text=value_counts.values,  # Text annotations on bars
                textposition=text_positions,  # Position annotations outside the bars
                marker_color='#F5B323'
            )
        ])

        # Update layout to match the styling of the Matplotlib plot
        fig10.update_layout(
            title='werk Distribution',
            xaxis_title='werk',
            yaxis_title='Summe',
            template='plotly_white',
            height=350,
        )


        fig2 = go.Figure()

        value_counts = datahalf['bme'].value_counts()

        #print(value_counts)

        colors = ['#F5B323', 'dimgrey', 'black', 'gainsboro']
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
            title='bme Distribution',
            xaxis_title='Anzahl',
            yaxis_title='Summe',
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,

            # Set axis labels and title color to white
            font=dict(color='black'),
        )


        
        #data_required["bereit_dat"] = pd.to_datetime(data_required["bereit_dat"])

        if(input == False):
            datahalf["date"] = pd.to_datetime(datahalf["bereit_dat"], format="%d.%m.%Y", errors="coerce")
        else:
            datahalf["date"] = pd.to_datetime(datahalf["bereit_dat"], errors="coerce")


        datahalf_picks = datahalf[datahalf["Picks"] > 0]
        datahalf_pallets = datahalf[datahalf["Pallets"] > 0]

        datahalf_picks = datahalf_picks.sort_values(by="date")
        datahalf_pallets = datahalf_pallets.sort_values(by="date")

        # Create a bar chart using Plotly Express
        fig3 = px.bar(
            datahalf_picks, 
            x="date", 
            y="Picks", 
            labels={"date": "Datum", "Picks": "Picks"},
            title="Picks Balkendiagramm",
            color_discrete_sequence=["#F5B323"]

        )

        # Update layout to adjust x-axis labels
        fig3.update_layout(
            xaxis_tickformat="%Y-%m-%d", # Format for the date display
            xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
        )


        # Create a bar chart using Plotly Express
        fig4 = px.bar(
            datahalf_pallets, 
            x="date", 
            y="Pallets", 
            labels={"date": "Datum", "Pallets": "PAL"},
            title="Pal Balkendiagramm",
            color_discrete_sequence=["#F5B323"]
        )

        # Update layout to adjust x-axis labels
        fig4.update_layout(
            xaxis_tickformat="%Y-%m-%d", # Format for the date display
            xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
        )


        if(input == False):
            #datextracted["date"] = pd.to_datetime(datextracted["bereit_dat"])
            datextracted["date"] = pd.to_datetime(datextracted["bereit_dat"], format="%d.%m.%Y", errors="coerce")
            datextracted = datextracted.sort_values(by="date")

            #print(datextracted)

            # Create a bar chart using Plotly Express
            fig5 = px.bar(
                datextracted, 
                x="date", 
                y="Picks", 
                color="Gesamt", 
                labels={"date": "Datum", "Picks": "Picks"},
                title="Picks Balkendiagramm",
                color_discrete_map={
                "Direkt": "#F5B323",  
                "Dachser": "black",  
                "TOF": "dimgrey",  
                }
            )

            # Update layout to adjust x-axis labels
            fig5.update_layout(
                xaxis_tickformat="%Y-%m-%d", # Format for the date display
                xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
            )


            # Create a bar chart using Plotly Express
            fig6 =px.bar(
                datextracted, 
                x="date", 
                y="Pallets", 
                color="Gesamt",
                labels={"date": "Datum", "Pallets": "PAL"},
                title="Pal Balkendiagramm",
                color_discrete_map={
                "Direkt": "#F5B323",  
                "Dachser": "black",  
                "TOF": "dimgrey",  
                }
            )

            # Update layout to adjust x-axis labels
            fig6.update_layout(
                xaxis_tickformat="%Y-%m-%d", # Format for the date display
                xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
            )

        datahalf["Picks"] = datahalf["Picks"].astype(int)
        datahalf["Pallets"] = datahalf["Pallets"].astype(int)

        grouped_data = pd.DataFrame(datahalf.groupby('werk')[["Pallets", "Picks"]].sum()).reset_index()
        grouped_data["Picks"] = grouped_data["Picks"].astype(int)
        grouped_data["Pallets"] = grouped_data["Pallets"].astype(int)


        ## Komi pal logic
        datextracted["Auftragsmenge_Bestätigt_float"] = datextracted["best_mg"]
        datextracted["Picks_per_Unit"] = datextracted["Picks"] / datextracted["Auftragsmenge_Bestätigt_float"]
        filtted_rows =datextracted[["namewarenempfnger", "ortwempf", "Picks", "Pallets", "Auftragsmenge_Bestätigt_float", "Picks_per_Unit","kzu","werk"]]


        grouped = filtted_rows.groupby(["namewarenempfnger", "ortwempf"])
        Names_list = []
        komi_Pal =[]
        for (name, city), group in grouped:
            filtered_data = filtted_rows[(filtted_rows["namewarenempfnger"] == name) & (filtted_rows["ortwempf"] == city)]
            
            #print(set(filtered_data["werk"]))

            group_with_x = filtered_data[filtered_data["kzu"] == "X"]
            total_picks_per_unit = group_with_x["Picks_per_Unit"].sum()

            komi_pal = np.ceil(total_picks_per_unit).astype(int)

            group_with_none = group[group["kzu"].isna()]
            for idx, row in group_with_none.iterrows():
                nan_sum =np.ceil(row["Picks_per_Unit"]).astype(int)
                komi_pal+=nan_sum

            #Names_list.append(f"{name} \n {city}")
            Names_list.append(list(set(filtered_data["werk"]))[0])
            komi_Pal.append(komi_pal)


        komipal_df = pd.DataFrame()
        komipal_df["Names"] = Names_list
        komipal_df["komi"] = komi_Pal
        grouped_final = pd.DataFrame(komipal_df.groupby("Names")["komi"].sum()).reset_index()
        #print(grouped_final)
        grouped_final["komi"] = grouped_final["komi"].astype(int)



        fig20 = go.Figure()

        # Add Pallets bar
        fig20.add_trace(go.Bar(
            x=grouped_data['werk'],
            y=grouped_data['Pallets'],
            text=grouped_data['Pallets'],  
            texttemplate='%{text:d}',     
            hoverinfo='text',   
            name='Pallets',
            marker_color='black'
        ))

        # Add Picks bar
        fig20.add_trace(go.Bar(
            x=grouped_data['werk'],
            y=grouped_data['Picks'],
            name='Picks',
            marker_color='#F5B323',
            text=grouped_data['Picks'],  
            texttemplate='%{text:d}',    
            hoverinfo='text'  
        ))

        fig20.add_trace(go.Bar(
            x=grouped_final['Names'],
            y=grouped_final['komi'],
            name='KomiPAL',
            marker_color='#F50323',
            text=grouped_final['komi'],  
            texttemplate='%{text:d}',    
            hoverinfo='text'  
        ))

        fig20.update_layout(
            title='PAL & Picks je werk ',
            xaxis=dict(title='werk'),
            yaxis=dict(title='Werte'),
            barmode='group',  
            #template='plotly',
            plot_bgcolor='white',
            paper_bgcolor='white',
        )

        if(input == False):
            return ls, ls2, datahalf.to_dict('records'), datextracted.to_dict('records') , fig, fig2, fig3, fig4, fig5, fig6, fig10, fig20
        else:
            return ls, [], datahalf.to_dict('records'), pd.DataFrame().to_dict('records') , fig, fig2, fig3, fig4, {}, {}, fig10, fig20



    def get_absenders(self):

        def make_sender_dict(data):

            #print(data.columns)
            all_senders = set(data["auftrgeber"])
            sender_dict = {}
            for sender in all_senders:
                first = data[data["auftrgeber"] == sender]

                recivers =first["warenempf_"]
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
            marker_color='#F5B323',
            width=width
        ))

        fig.add_trace(go.Bar(
            x=[str(d) for d in keys_sorted],
            y=values_2_sorted,
            name='Eigene',
            marker_color='black',
            width=width
        ))

        fig.update_layout(
            title='Top 50 abSenders',
            xaxis_title='abSenders',
            yaxis_title='Gesmate gesendete',
            barmode='group',  
            xaxis_tickangle=-90,  
            template='plotly_white',
            legend_title='Type',

        )

        return fig

    def make_customized_plot(self, user):
        def make_sender_dict(data):

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


        colors = ['#F5B323', 'dimgrey', 'black', 'gainsboro']
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


        fig.update_layout(
            xaxis_tickformat="%Y-%m-%d", # Format for the date display
            xaxis_tickangle=45,           # Rotate x-axis labels by 45 degrees
            plot_bgcolor='white',
            paper_bgcolor='white',
            

        )

        return fig
        



