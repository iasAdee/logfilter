from dash import Input, Output, html, State
from layouts.page_layouts import (
    get_analysis_page_layout,
    get_visualization_page_layout,
    get_cleaning_page_layout,
    get_export_page_layout,
    get_ml_page_layout,
    get_table_page_layout
)
from layouts.login_layout import login_layout
from layouts.main_layout import get_home_layout

        
def register_routing_callbacks(app):

    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname'),
        Input('auth-store', 'data')
    )
    def route_pages(pathname, auth):
        logged_in = auth.get('logged_in', False)

        # 🔒 Not logged in → always show login
        if not logged_in:
            return login_layout()

        # ✅ Logged in → normal routing
        if pathname in ['/', '/home']:
            return get_home_layout()

        elif pathname == '/analysis':
            return get_analysis_page_layout()

        elif pathname == '/visualization':
            return get_visualization_page_layout()
        
        elif pathname == '/ML':
            return get_ml_page_layout()

        elif pathname == '/table':
            return get_table_page_layout()

        return html.Div("404 - Page not found")
