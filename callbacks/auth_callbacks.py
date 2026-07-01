from dash import Input, Output, State
from dash.exceptions import PreventUpdate

def register_auth_callbacks(app):

    @app.callback(
        Output('auth-store', 'data'),
        Output('login-error', 'children'),
        Input('login-button', 'n_clicks'),
        State('login-username', 'value'),
        State('login-password', 'value'),
        prevent_initial_call=True
    )
    def login(n_clicks, username, password):
        # 🔐 Replace with real auth later
        if username == "admin" and password == "admin":
            return {'logged_in': True}, ""

        return {'logged_in': False}, "Ungültige Anmeldedaten"
