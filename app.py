from dash import Dash, dcc, html
from flask_caching import Cache
from dash import Input, Output, html, dash_table
from data_manager import DataManager
from callbacks.upload_callbacks import register_upload_callbacks
from callbacks.routing_callbacks import register_routing_callbacks
from callbacks.page_content_callbacks import register_page_content_callbacks
from callbacks.auth_callbacks import register_auth_callbacks
import pandas as pd



# Initialize Dash app with URL routing
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Setup cache
cache = Cache(
    server,
    config={
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 60 * 60
    }
)

# Initialize data manager
data_manager = DataManager(cache)

# Main app layout with routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(
        id='auth-store',
        storage_type='session',
        data={'logged_in': False}
    ),
    dcc.Store(id='uploaded-cache-key'),
	dcc.Store(id="stored_results"),
	dcc.Download(id="download-dataframe-pdf"),
    html.Div(id='page-content')
])

# Register all callbacks
register_auth_callbacks(app)
register_upload_callbacks(app, data_manager)  
register_routing_callbacks(app)
register_page_content_callbacks(app, data_manager)





if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8060)
