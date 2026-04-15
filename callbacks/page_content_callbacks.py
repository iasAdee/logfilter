import pandas as pd
import plotly.express as px
from dash import Input, Output, html, dash_table, State,dcc
import dash
import fitz

from algorithms.pdf import calculate_pdf_scores
from algorithms.ocrllm import get_results
from algorithms.excel_to_word import load_docx_and_print_tables,get_results_word
import base64



def register_page_content_callbacks(app, data_manager):
    """Register callbacks that populate page content with uploaded data."""
    
    # Analysis Page Content
    @app.callback(
        Output('analysis-content', 'children'),
        Output("download-docx", "data"),
        Input('uploaded-cache-key', 'data'),
        Input('url', 'pathname')
    )
    def update_analysis_content(cache_key, pathname):
        print(pathname)

        if pathname != '/analysis' or not cache_key:
            raise dash.exceptions.PreventUpdate
        
        if not cache_key:
            return html.Div([
                html.Div([
                    html.Div("⚠️", style={'fontSize': '48px', 'marginBottom': '20px'}),
                    html.H3("Keine Daten verfügbar", style={
                        'color': 'rgb(75, 75, 75)',
                        'marginBottom': '10px'
                    }),
                    html.P("Bitte laden Sie eine PDF-Datei von der Startseite hoch.", style={
                        'color': 'rgb(124, 124, 124)',
                        'fontSize': '14px'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '60px 20px',
                    'backgroundColor': 'rgb(255, 255, 255)',
                    'borderRadius': '12px',
                    'border': '2px dashed rgb(208, 208, 208)',
                    'maxWidth': '500px',
                    'margin': '40px auto'
                })
            ]),None
        
        df = data_manager.get_dataframe(cache_key)
        if df is None:
            return html.Div([
                html.Div([
                    html.Div("❌", style={'fontSize': '48px', 'marginBottom': '20px'}),
                    html.H3("Data Not Found", style={
                        'color': 'rgb(75, 75, 75)',
                        'marginBottom': '10px'
                    }),
                    html.P("The data has expired or could not be loaded.", style={
                        'color': 'rgb(124, 124, 124)',
                        'fontSize': '14px'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '60px 20px',
                    'backgroundColor': 'rgb(255, 255, 255)',
                    'borderRadius': '12px',
                    'border': '2px solid rgb(216, 40, 47)',
                    'maxWidth': '500px',
                    'margin': '40px auto'
                })
            ]),None
        
        # Generate analysis
        if(len(df) > 0):
            print(df)
            list_of_kgs, list_of_kgs2, list_of_strings = get_results_word(df)

            docx_file_path1 = 'wlayouts/IMO_Layout_new.docx'
            docx_file_path2 = 'wlayouts/IMO_Layout_2.docx'
            docx_file_path3 = 'wlayouts/IMO_Layout_3.docx'  
            docx_file_path4 = 'wlayouts/IMO_Layout_4.docx'  
            docx_file_path5 = 'wlayouts/IMO_Layout_5.docx'


            print("Length of list: ", len(list_of_strings))
            list_of_strings=[val for val in list_of_strings if val !=""]

            if(len(list_of_strings) == 1):
                with open(docx_file_path1, "rb") as f:
                    word_content = f.read()
            if(len(list_of_strings) == 2):
                with open(docx_file_path2, "rb") as f:
                    word_content = f.read()
            if(len(list_of_strings) == 3):
                with open(docx_file_path3, "rb") as f:
                    word_content = f.read()
            if(len(list_of_strings) == 4):
                with open(docx_file_path4, "rb") as f:
                    word_content = f.read()
            if(len(list_of_strings) == 5):
                with open(docx_file_path5, "rb") as f:
                    word_content = f.read()

            modified_docx_bytes = load_docx_and_print_tables(word_content, list_of_strings, list_of_kgs, list_of_kgs2)    
            if modified_docx_bytes:
                return html.Div([
                    # Header
                    html.Div([
                        html.H2("Document Processed and Downloaded Check your downloads", style={
                            'color': 'rgb(255, 255, 255)',
                            'margin': '0',
                            'fontSize': '28px',
                            'fontWeight': '600'
                        }),
                    ], style={
                        'background': 'linear-gradient(135deg, rgb(110, 149, 178) 0%, rgb(80, 117, 141) 100%)',
                        'padding': '40px 20px',
                        'marginBottom': '30px'
                    }),
                    
                ], style={
                    'width': '100%'
                }), dcc.send_bytes(
                    modified_docx_bytes,
                    "IMO_Formular.docx"
                )                                        

        return html.Div([
            # Header
            html.Div([
                html.H2("Document Process Failed", style={
                    'color': 'rgb(255, 255, 255)',
                    'margin': '0',
                    'fontSize': '28px',
                    'fontWeight': '600'
                }),
            ], style={
                'background': 'linear-gradient(135deg, rgb(110, 149, 178) 0%, rgb(80, 117, 141) 100%)',
                'padding': '40px 20px',
                'marginBottom': '30px'
            }),
            
        ], style={
            'width': '100%',
            'minHeight': '100vh',
            'backgroundColor': 'rgb(248, 249, 250)'
        }), None
    

    
    @app.callback(
    Output("download-dataframe-pdf", "data"),
    Input('download', 'n_clicks'),
    State('stored_results', 'data'),
    prevent_initial_call=True
    )
    def save_data(n_clicks,data1):
        if not n_clicks:
            raise dash.exceptions.PreventUpdate
        if(n_clicks != None):
            df = pd.DataFrame(data1)
            #df.to_csv("sped_data.csv", index=False)
            return dcc.send_data_frame(df.to_csv, "pdf_details.csv", index=False)
        
        
    # Visualization Page Content
    @app.callback(
        Output('visualization-content', 'children'),
        Output('stored_results', 'data'),
        Input('viz-button', 'n_clicks'),  
        State('uploaded-cache-key', 'data'),
        State('url', 'pathname'),
        State('api_input', 'value'),
        State('algorithm_selector', 'value'),
        prevent_initial_call=True
    )
    def update_visualization_content(n_clicks, cache_key, pathname, api_input, selected_model):

        if not n_clicks:
            raise dash.exceptions.PreventUpdate
        
        if pathname != '/visualization':
            raise dash.exceptions.PreventUpdate
        if not cache_key:
            return html.Div([
                html.Div([
                    html.Div("📊", style={'fontSize': '48px', 'marginBottom': '20px'}),
                    html.H3("Keine Daten verfügbar", style={
                        'color': 'rgb(75, 75, 75)',
                        'marginBottom': '10px'
                    }),
                    html.P("Bitte laden Sie eine PDF-Datei von der Startseite hoch.", style={
                        'color': 'rgb(124, 124, 124)',
                        'fontSize': '14px'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '60px 20px',
                    'backgroundColor': 'rgb(255, 255, 255)',
                    'borderRadius': '12px',
                    'border': '2px dashed rgb(208, 208, 208)',
                    'maxWidth': '500px',
                    'margin': '40px auto'
                })
            ]),pd.DataFrame().to_dict('records')
        


        print("Cache key for image processing: ", cache_key)
        obj = data_manager.get_data(cache_key)
        pdf_doc = fitz.open(stream=obj["bytes"], filetype="pdf")

        if(api_input == ""):
            return html.Div([
                html.Div([
                    html.Div("📊", style={'fontSize': '48px', 'marginBottom': '20px'}),
                    html.H3("Keine Daten verfügbar", style={
                        'color': 'rgb(75, 75, 75)',
                        'marginBottom': '10px'
                    }),
                    html.P("Bitte laden Sie eine PDF-Datei von der Startseite hoch.", style={
                        'color': 'rgb(124, 124, 124)',
                        'fontSize': '14px'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '60px 20px',
                    'backgroundColor': 'rgb(255, 255, 255)',
                    'borderRadius': '12px',
                    'border': '2px dashed rgb(208, 208, 208)',
                    'maxWidth': '500px',
                    'margin': '40px auto'
                })
            ]),pd.DataFrame().to_dict('records')


        # Handle PDF
        if(selected_model == "ocrllm"):
            df = get_results(pdf_doc, api_key=api_input)
        else:
            df = calculate_pdf_scores(pdf_doc, api_key=api_input)

        correct = len(df[df['Match'] == 'übereinstimmend'])
        incorrect = len(df[df['Match'] == 'nicht übereinstimmend'])#(df['Match'] == '')

        if isinstance(obj, dict) and 'page_count' in obj:

            html_data = html.Div([
                    # Header
                    html.Div([
                        html.H2("PDF Ergebnisanalyse", style={
                            'color': 'rgb(255, 255, 255)',
                            'margin': '0',
                            'fontSize': '28px',
                            'fontWeight': '600'
                        }),
                        html.P(f"Dokument enthält {obj.get('page_count', '?')} Seiten | Größe: {obj.get('size_bytes', 0):,} bytes", style={
                            'color': 'rgba(255, 255, 255, 0.9)',
                            'margin': '8px 0 0 0',
                            'fontSize': '14px'
                        },),
                        html.P(f"nicht übereinstimmend: {incorrect} übereinstimmend: {correct}", style={
                            'color': 'rgba(255, 255, 255, 0.9)',
                            'margin': '8px 0 0 0',
                            'fontSize': '14px'
                        })

                    ], style={
                        'background': 'linear-gradient(135deg, rgb(110, 149, 178) 0%, rgb(80, 117, 141) 100%)',
                        'padding': '40px 20px',
                        'marginBottom': '30px'
                    }),
                    
                    # Data Table
                    dash_table.DataTable(
                        id='page-datatable_image',
                        columns=[{'name': c, 'id': c} for c in df.columns],
                        data=df.to_dict('records'),
                        page_current=0,
                        page_size=20,
                        page_action='native',
                        sort_action='native',
                        filter_action='native',
                        style_table={
                            'overflowX': 'auto',
                            'width': '100%'
                        },
                        style_cell={
                            'textAlign': 'left',
                            'minWidth': '100px',
                            'maxWidth': '300px',
                            'padding': '14px 16px',
                            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                            'fontSize': '14px',
                            'border': 'none',
                            'borderBottom': '1px solid rgb(240, 240, 240)',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis'
                        },
                        style_header={
                            'backgroundColor': 'rgb(110, 149, 178)',
                            'color': 'white',
                            'fontWeight': '600',
                            'textTransform': 'uppercase',
                            'fontSize': '12px',
                            'letterSpacing': '0.5px',
                            'padding': '16px',
                            'border': 'none'
                        },
                        style_data={
                            'backgroundColor': 'rgb(255, 255, 255)',
                            'color': 'rgb(75, 75, 75)'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 249, 250)'
                            },
                            {
                                'if': {'state': 'active'},
                                'backgroundColor': 'rgba(110, 149, 178, 0.1)',
                                'border': '1px solid rgb(110, 149, 178)'
                            }
                        ],
                        tooltip_data=[
                            {
                                column: {'value': str(value), 'type': 'markdown'}
                                for column, value in row.items()
                            } for row in df.to_dict('records')
                        ],
                        tooltip_duration=None
                    )
                ], style={
                    'width': '100%',
                    'minHeight': '100vh',
                    'backgroundColor': 'rgb(248, 249, 250)',
                    'paddingBottom': '40px'
                })
            return html_data, df.to_dict('records')
        
        return html.Div(""), pd.DataFrame().to_dict('records')
    
    
