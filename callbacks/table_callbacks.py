import dash
import pandas as pd
from dash import html, Input, Output, dash_table


def register_table_callbacks(app, data_manager):
    """Register all table display callbacks."""
    
    @app.callback(
        Output('table-container', 'children'),
        Input('uploaded-cache-key', 'data'),
        Input('page-size', 'value'),
        Input('clear-cache', 'n_clicks')
    )
    def show_table(cache_key, page_size, clear_clicks):
        ctx_trigger = dash.callback_context.triggered
        if ctx_trigger and ctx_trigger[0]['prop_id'].startswith('clear-cache'):
            data_manager.clear_cache()
            return html.Div("Cache cleared.")

        if not cache_key:
            return html.Div("No data to display.")

        obj = data_manager.get_data(cache_key)
        if obj is None:
            return html.Div("Cached item not found or expired.")

        if isinstance(obj, pd.DataFrame):
            df = obj
        elif isinstance(obj, dict):
            return html.Div([
                html.H4("PDF loaded"),
                html.Div(f"Pages: {obj.get('page_count', '?')}"),
                html.Div(f"Size (bytes): {obj.get('size_bytes', '?')}"),
            ])
        else:
            return html.Div("Unsupported cached object format.")

        page_size = int(page_size or 10)
        columns = [{'name': c, 'id': c} for c in df.columns]
        table = dash_table.DataTable(
            id='datatable',
            columns=columns,
            data=df.to_dict('records'),
            page_current=0,
            page_size=page_size,
            page_action='native',
            sort_action='native',
            filter_action='native',
            style_table={'overflowX': 'auto', 'maxHeight': '600px'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'whiteSpace': 'normal'},
        )
        summary = html.Div([
            html.Div(f"Rows: {len(df)}"), 
            html.Div(f"Columns: {len(df.columns)}")
        ], style={'marginTop':'8px'})
        
        return html.Div([table, summary])