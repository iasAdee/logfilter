# ============================================================================
# layouts/page_layouts.py
# ============================================================================
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
from layouts.upload_layout import get_upload_layout


def get_page_header(title, icon, description):
    """Common header for all pages."""
    return html.Div([
        html.Div([
            html.Span(icon, style={'fontSize': '48px', 'marginRight': '20px'}),
            html.Div([
                html.H2(title, style={'margin': '0', 'color': '#2c3e50'}),
                html.P(description, style={'margin': '5px 0 0 0', 'color': '#7f8c8d'})
            ])
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '30px'}),
        html.A('← Zurück zur Startseite', href='/', style={
            'textDecoration': 'none',
            'color': '#3498db',
            'fontSize': '16px',
            'marginBottom': '20px',
            'display': 'inline-block'
        })
    ])


def get_analysis_page_layout():
    """Layout for Data Analysis page."""
    return html.Div([
        get_page_header("📊 CSV, Xlsx, DOCX file will be processed", "📊", "The pages will be implemented soon!"),
        html.Hr(),
        html.Div(id='analysis-content', children=[
            html.Div("Upload a file to see analysis", style={'textAlign': 'center', 'padding': '50px'})
        ])
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})


def get_visualization_page_layout():
    """Layout for Data Visualization page."""
    return html.Div([
        get_page_header("🖼️ Bilderkennung", "🖼️", ""),
        html.Hr(),
        html.Div(
            children=[

                # ---- API input + button row ----
                html.Div(
                    children=[
                        dcc.Input(
                            id='api_input',
                            type='text',
                            placeholder='API-Schlüssel eingeben...',
                            style={
                                'padding': '10px 20px',
                                'fontSize': '16px',
                                'marginRight': '10px',
                                'width': '280px'
                            }
                        ),

                        html.Button(
                            "Visualisierung und Tabelle generieren",
                            id="viz-button",
                            n_clicks=0,
                            style={
                                'padding': '10px 24px',
                                'fontSize': '16px',
                                'cursor': 'pointer'
                            }
                        ),
                        html.Button(
                                "Tabelle speichern",
                                id="download",
                                n_clicks=0,
                                style={
                                    'padding': '10px 24px',
                                    'fontSize': '16px',
                                    'cursor': 'pointer'
                                }
                            )
                    ],
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'alignItems': 'center',
                        'gap': '10px'
                    }
                ),

                # ---- Algorithm selection ----
                html.Div(
                    children=[
                        html.Div(
                            "Algorithmus auswählen",
                            style={
                                'fontSize': '14px',
                                'fontWeight': '600',
                                'marginBottom': '6px'
                            }
                        ),

                        dcc.RadioItems(
                            id='algorithm_selector',
                            options=[
                                {'label': 'OCR+LLM (kann mehrmals aufgerufen werden)', 'value': 'ocrllm'},
                                {'label': 'LLM (nur 1 Aufruf)', 'value': 'llm'},
                            ],
                            value='ocrllm',
                            inline=True,
                            style={'fontSize': '15px'},
                            inputStyle={'marginRight': '6px', 'marginLeft': '12px'}
                        )
                    ],
                    style={
                        'marginTop': '18px',
                        'textAlign': 'center'
                    }
                )

            ],
            style={'marginBottom': '30px'}
        ),

            html.Div(id='visualization-content', children=[
                html.Div("Laden Sie eine Datei hoch, um Visualisierungen anzuzeigen", style={'textAlign': 'center', 'padding': '50px'})
        ])
    ], style={'maxWidth': '85%', 'margin': '0 auto', 'padding': '20px'})


def get_cleaning_page_layout():
    """Layout for Data Cleaning page."""
    return html.Div([
        get_page_header("🧹 Data Cleaning", "🧹", "Clean and transform your data"),
        html.Hr(),
        html.Div(id='cleaning-content', children=[
            html.Div("Upload a file to clean data", style={'textAlign': 'center', 'padding': '50px'})
        ])
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})


def get_export_page_layout():
    """Layout for Export & Reports page."""
    return html.Div([
        get_page_header("📄 Export & Reports", "📄", "Generate reports and export data"),
        html.Hr(),
        html.Div(id='export-content', children=[
            html.Div("Upload a file to export data", style={'textAlign': 'center', 'padding': '50px'})
        ])
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})


def get_ml_page_layout():
    """Layout for Machine Learning page."""
    return html.Div([
        get_page_header("🤖 Machine Learning", "🤖", "Apply ML models to your data"),
        html.Hr(),
        html.Div(id='ml-content', children=[
            html.Div("Upload a file to apply ML models", style={'textAlign': 'center', 'padding': '50px'})
        ])
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})


def get_table_page_layout():
    """Layout for View Data Table page."""
    return html.Div([
        get_page_header("📋 View Data Table", "📋", "Browse your uploaded data"),
        html.Hr(),
        html.Div([
            html.Div(id='table-page-controls', children=[
                html.Label("Rows per page:"),
                dcc.Dropdown(
                    id='table-page-size', 
                    options=[10, 20, 50, 100], 
                    value=20, 
                    clearable=False,
                    style={'width':'160px'}
                ),
            ], style={'display':'flex', 'gap':'12px', 'alignItems':'center', 'marginBottom': '20px'}),
            html.Div(id='table-page-content')
        ])
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})
