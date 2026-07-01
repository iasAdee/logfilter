from dash import html, Input, Output, State
from data_processor import DataProcessor


def register_processing_callbacks(app, data_manager):
    """Register all data processing callbacks."""
    
    @app.callback(
        Output('processing-output', 'children'),
        Input('process-btn', 'n_clicks'),
        State('uploaded-cache-key', 'data')
    )
    def process_data(n_clicks, cache_key):
        """Process uploaded data and show summary."""
        if not n_clicks or not cache_key:
            return None
        
        df = data_manager.get_dataframe(cache_key)
        if df is None:
            return html.Div("No DataFrame available to process.", style={'color': 'red'})
        
        # Use the DataProcessor module
        stats = DataProcessor.get_summary_stats(df)
        
        return html.Div([
            html.H4("Data Summary"),
            html.Div(f"Total Rows: {stats['rows']}"),
            html.Div(f"Total Columns: {stats['columns']}"),
            html.Div(f"Numeric Columns: {', '.join(stats['numeric_columns'])}"),
            html.Div(f"Columns with Missing Values: {sum(1 for v in stats['missing_values'].values() if v > 0)}")
        ], style={'padding': '10px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px'})

