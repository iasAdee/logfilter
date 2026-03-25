import pandas as pd
import plotly.express as px
from dash import Input, Output, html, dash_table, State,dcc
import dash
import fitz
from algorithms.pdf import calculate_pdf_scores
from algorithms.ocrllm import get_results


def register_page_content_callbacks(app, data_manager):
    """Register callbacks that populate page content with uploaded data."""
    
    # Analysis Page Content
    @app.callback(
        Output('analysis-content', 'children'),
        Input('uploaded-cache-key', 'data'),
        Input('url', 'pathname')
    )
    def update_analysis_content(cache_key, pathname):
        
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
            ])
        
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
            ])
        
        # Generate analysis
        stats = {
            'Total Rows': len(df),
            'Total Columns': len(df.columns),
            'Numeric Columns': len(df.select_dtypes(include=['number']).columns),
            'Text Columns': len(df.select_dtypes(include=['object']).columns),
            'Missing Values': df.isnull().sum().sum()
        }
        
        return html.Div([
            # Header
            html.Div([
                html.H2("Dataset Analysis", style={
                    'color': 'rgb(255, 255, 255)',
                    'margin': '0',
                    'fontSize': '28px',
                    'fontWeight': '600'
                }),
                html.P("Statistical overview of your uploaded data", style={
                    'color': 'rgba(255, 255, 255, 0.9)',
                    'margin': '8px 0 0 0',
                    'fontSize': '14px'
                })
            ], style={
                'background': 'linear-gradient(135deg, rgb(110, 149, 178) 0%, rgb(80, 117, 141) 100%)',
                'padding': '40px 20px',
                'marginBottom': '30px'
            }),
            
            # Statistics Cards
            html.Div([
                html.Div([
                    html.Div(str(value), style={
                        'fontSize': '36px',
                        'fontWeight': '700',
                        'color': 'rgb(110, 149, 178)',
                        'margin': '0 0 8px 0',
                        'lineHeight': '1'
                    }),
                    html.Div(key, style={
                        'fontSize': '13px',
                        'color': 'rgb(124, 124, 124)',
                        'fontWeight': '500',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    })
                ], style={
                    'padding': '28px 24px',
                    'backgroundColor': 'rgb(255, 255, 255)',
                    'borderRadius': '12px',
                    'textAlign': 'center',
                    'border': '1px solid rgb(230, 230, 230)',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.05)',
                    'transition': 'transform 0.2s',
                }) for key, value in stats.items()
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(180px, 1fr))',
                'gap': '20px',
                'marginBottom': '40px',
                'padding': '0 20px'
            }),
            
            # Column Information Section
            html.Div([
                html.H3("Column Information", style={
                    'color': 'rgb(75, 75, 75)',
                    'fontSize': '22px',
                    'fontWeight': '600',
                    'marginBottom': '20px',
                    'padding': '0 20px'
                }),
                dash_table.DataTable(
                    data=[{'Column': col, 'Type': str(dtype), 'Missing': df[col].isnull().sum()} 
                          for col, dtype in df.dtypes.items()],
                    columns=[
                        {'name': 'Column', 'id': 'Column'},
                        {'name': 'Data Type', 'id': 'Type'},
                        {'name': 'Missing Values', 'id': 'Missing'}
                    ],
                    style_table={
                        'overflowX': 'auto',
                        'width': '100%'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '14px 16px',
                        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                        'fontSize': '14px',
                        'border': 'none',
                        'borderBottom': '1px solid rgb(240, 240, 240)',
                        'whiteSpace': 'normal',
                        'height': 'auto'
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
                    ]
                )
            ], style={
                'marginBottom': '40px'
            })
        ], style={
            'width': '100%',
            'minHeight': '100vh',
            'backgroundColor': 'rgb(248, 249, 250)'
        })
    

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
    
    # Table Page Content
    @app.callback(
        Output('table-page-content', 'children'),
        Input('uploaded-cache-key', 'data'),
        Input('table-page-size', 'value'),
        Input('url', 'pathname')
    )
    def update_table_page_content(cache_key, page_size, pathname):

        if pathname != '/table':
            raise dash.exceptions.PreventUpdate
        
        if not cache_key:
            return html.Div([
                html.Div([
                    html.Div("📋", style={'fontSize': '48px', 'marginBottom': '20px'}),
                    html.H3("No Data Available", style={
                        'color': 'rgb(75, 75, 75)',
                        'marginBottom': '10px'
                    }),
                    html.P("Please upload a file from the home page to view data.", style={
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
            ])
        
        print("Printing cache from inside app call", cache_key)
        obj = data_manager.get_data(cache_key)
        if obj is None:
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
            ])
        
        # Handle PDF
        if isinstance(obj, dict) and 'page_count' in obj:
            return html.Div([
                # Header
                html.Div([
                    html.H2("PDF Document Information", style={
                        'color': 'rgb(255, 255, 255)',
                        'margin': '0',
                        'fontSize': '28px',
                        'fontWeight': '600'
                    })
                ], style={
                    'background': 'linear-gradient(135deg, rgb(110, 149, 178) 0%, rgb(80, 117, 141) 100%)',
                    'padding': '40px 20px',
                    'marginBottom': '30px'
                }),
                
                # PDF Info Cards
                html.Div([
                    html.Div([
                        html.Div("📄", style={'fontSize': '36px', 'marginBottom': '12px'}),
                        html.Div(str(obj.get('page_count', '?')), style={
                            'fontSize': '32px',
                            'fontWeight': '700',
                            'color': 'rgb(110, 149, 178)',
                            'marginBottom': '6px'
                        }),
                        html.Div("Total Pages", style={
                            'fontSize': '13px',
                            'color': 'rgb(124, 124, 124)',
                            'fontWeight': '500'
                        })
                    ], style={
                        'padding': '32px 24px',
                        'backgroundColor': 'rgb(255, 255, 255)',
                        'borderRadius': '12px',
                        'textAlign': 'center',
                        'border': '1px solid rgb(230, 230, 230)',
                        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.05)'
                    }),
                    html.Div([
                        html.Div("💾", style={'fontSize': '36px', 'marginBottom': '12px'}),
                        html.Div(f"{obj.get('size_bytes', 0):,}", style={
                            'fontSize': '32px',
                            'fontWeight': '700',
                            'color': 'rgb(110, 149, 178)',
                            'marginBottom': '6px'
                        }),
                        html.Div("Bytes", style={
                            'fontSize': '13px',
                            'color': 'rgb(124, 124, 124)',
                            'fontWeight': '500'
                        })
                    ], style={
                        'padding': '32px 24px',
                        'backgroundColor': 'rgb(255, 255, 255)',
                        'borderRadius': '12px',
                        'textAlign': 'center',
                        'border': '1px solid rgb(230, 230, 230)',
                        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.05)'
                    })
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
                    'gap': '20px',
                    'padding': '0 20px'
                })
            ], style={
                'width': '100%',
                'minHeight': '100vh',
                'backgroundColor': 'rgb(248, 249, 250)',
                'paddingBottom': '40px'
            })
        
        # Handle DataFrame
        if isinstance(obj, pd.DataFrame):
            df = obj
            page_size = int(page_size or 20)
            
            return html.Div([
                # Header
                html.Div([
                    html.H2("Data Table View", style={
                        'color': 'rgb(255, 255, 255)',
                        'margin': '0',
                        'fontSize': '28px',
                        'fontWeight': '600'
                    }),
                    html.P(f"Showing {len(df)} rows × {len(df.columns)} columns", style={
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
                    id='page-datatable',
                    columns=[{'name': c, 'id': c} for c in df.columns],
                    data=df.to_dict('records'),
                    page_current=0,
                    page_size=page_size,
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
        
        return html.Div("Unsupported data format.")