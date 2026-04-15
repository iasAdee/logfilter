# layouts/main_layout.py
from dash import html, dcc
from layouts.upload_layout import get_upload_layout


def get_card(title, icon, page_link, color="#4A90E2",description=""):
    """Create a clickable card component with modern design."""
    return dcc.Link(
        href=page_link,
        style={'textDecoration': 'none', 'color': 'inherit'},
        children=[
            html.Div([
                # Icon container with gradient background
                html.Div(
                    icon, 
                    style={
                        'fontSize': '42px',
                        'marginBottom': '18px',
                        'width': '80px',
                        'height': '80px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'background': f'linear-gradient(135deg, {color}20, {color}40)',
                        'borderRadius': '16px',
                        'margin': '0 auto 18px'
                    }
                ),
                html.H3(title, style={
                    'margin': '0 0 12px 0',
                    'fontSize': '18px',
                    'fontWeight': '600',
                    'color': 'rgb(75, 75, 75)',
                    'lineHeight': '1.3'
                }),
                html.P(description, style={
                    'margin': '0',
                    'fontSize': '13px',
                    'color': 'rgb(124, 124, 124)',
                    'lineHeight': '1.6'
                })
            ], style={
                'padding': '28px 24px',
                'backgroundColor': 'rgb(255, 255, 255)',
                'borderRadius': '12px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                'cursor': 'pointer',
                'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                'height': '100%',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'flex-start',
                'alignItems': 'center',
                'textAlign': 'center',
                'border': '1px solid rgb(230, 230, 230)',
                'position': 'relative',
                'overflow': 'hidden'
            }, className='card-hover')
        ]
    )


def get_home_layout():
    """Return the home page layout with modern design."""
    return html.Div([
        # Header Section with gradient background
        html.Div([
            html.Div([
                html.H1("Logfilter", style={
                    "margin": "0 0 12px 0",
                    "color": "rgb(255, 255, 255)",
                    "fontSize": "36px",
                    "fontWeight": "700",
                    "letterSpacing": "-0.5px"
                }),
                html.P("Excel / CSV / PDF Verarbeitungsplattform", style={
                    "margin": "0",
                    "color": "rgba(255, 255, 255, 0.9)",
                    "fontSize": "16px",
                    "fontWeight": "400"
                })
            ], style={
                'textAlign': 'center',
                'padding': '60px 20px 40px',
            })
        ], style={
            'background': 'linear-gradient(135deg, rgb(110, 149, 178) 0%, rgb(80, 117, 141) 100%)',
            'marginBottom': '40px',
            'boxShadow': '0 4px 20px rgba(80, 117, 141, 0.15)'
        }),
        
        # Upload Section
        html.Div([
            get_upload_layout()
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto 50px',
            'padding': '0 20px'
        }),
        
        # Cards Section
        html.Div([
            html.Div([
                html.H2("", style={
                    "margin": "0 0 10px 0",
                    "color": "rgb(75, 75, 75)",
                    "fontSize": "28px",
                    "fontWeight": "600",
                    "textAlign": "center"
                }),
                html.P("Wählen Sie ein Modul zur Verarbeitung Ihrer Daten", style={
                    "margin": "0 0 40px 0",
                    "color": "rgb(124, 124, 124)",
                    "fontSize": "15px",
                    "textAlign": "center"
                })
            ]),
            
            # Cards Grid
            html.Div([
                get_card(
                    title="Neuer Filter",
                    #description="Analyze your uploaded data with statistical tools and insights",
                    icon="📊",
                    page_link="/analysis",
                    color="rgb(142, 177, 212)"
                ),
                get_card(
                    title="M7 Kundenbestellungen",
                    #description="Create interactive charts and graphs from your data",
                    icon="📈",
                    page_link="/analysis",
                    color="rgb(110, 149, 178)"
                ),
                get_card(
                    title="Wareneingänge",
                    #description="Clean, transform, and prepare your data for processing",
                    icon="🔄",
                    page_link="/analysis",
                    color="rgb(145, 189, 188)"
                ),
                get_card(
                    title="Dangerous Goods Declaration",
                    #description="Generate reports and export data in various formats",
                    icon="⚠️",
                    page_link="/ML",
                    color="rgb(216, 40, 47)"
                ),
                get_card(
                    title="Bestandsüberprüfung",
                    #description="Apply ML models and predictions to your dataset",
                    icon="🤖",
                    page_link="/analysis",
                    color="rgb(245, 179, 37)"
                ),
                get_card(
                    title="Bilderkennung",
                    #description="Upload and check image matching capabilities",
                    icon="🖼️",
                    page_link="/visualization",
                    color="rgb(85, 157, 151)"
                ),
                get_card(
                    title="DE30 Bestandsart",
                    #description="Browse and filter your uploaded data in table format",
                    icon="📋",
                    page_link="/analysis",
                    color="rgb(185, 210, 209)"
                ),
                get_card(
                    title="Feuerwehrliste DE01",
                    #description="Fire department list management and reporting",
                    icon="🚒",
                    page_link="/analysis",
                    color="rgb(216, 40, 47)"
                ),
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fill, minmax(260px, 1fr))',
                'gap': '24px',
                'marginBottom': '60px'
            })
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 20px'
        }),
        
        # Footer
        html.Div([
            html.P("© 2025 Logfilter. Alle Rechte vorbehalten.", style={
                'margin': '0',
                'color': 'rgb(164, 164, 164)',
                'fontSize': '13px',
                'textAlign': 'center'
            })
        ], style={
            'padding': '30px 20px',
            'borderTop': '1px solid rgb(230, 230, 230)',
            'marginTop': '40px'
        })
    ], style={
        'minHeight': '100vh',
        'backgroundColor': 'rgb(248, 249, 250)',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    })


# Add CSS for hover effects
def get_custom_css():
    """Return custom CSS for card hover effects."""
    return """
    <style>
        .card-hover:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
            border-color: rgb(110, 149, 178) !important;
        }
        
        .card-hover:active {
            transform: translateY(-2px);
        }
    </style>
    """
