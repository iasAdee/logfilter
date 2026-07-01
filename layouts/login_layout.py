from dash import html, dcc

def login_layout():
    return html.Div(
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'height': '100vh',
            'background': 'linear-gradient(135deg, rgb(80, 117, 141) 0%, rgb(110, 149, 178) 100%)',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
        },
        children=[
            html.Div(
                style={
                    'width': '400px',
                    'padding': '40px',
                    'background': 'rgb(255, 255, 255)',
                    'borderRadius': '12px',
                    'boxShadow': '0 10px 40px rgba(0, 0, 0, 0.15)',
                },
                children=[
                    # Logo or title section
                    html.Div(
                        style={
                            'textAlign': 'center',
                            'marginBottom': '30px'
                        },
                        children=[
                            html.Div(
                                style={
                                    'width': '60px',
                                    'height': '60px',
                                    'background': 'linear-gradient(135deg, rgb(110, 149, 178), rgb(80, 117, 141))',
                                    'borderRadius': '50%',
                                    'margin': '0 auto 15px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center',
                                    'fontSize': '24px',
                                    'color': 'white',
                                    'fontWeight': 'bold'
                                },
                                children='LF'
                            ),
                            html.H2(
                                "Willkommen zurück",
                                style={
                                    'color': 'rgb(75, 75, 75)',
                                    'margin': '0',
                                    'fontSize': '24px',
                                    'fontWeight': '600'
                                }
                            ),
                            html.P(
                                "Bitte melden Sie sich bei Ihrem Konto an",
                                style={
                                    'color': 'rgb(124, 124, 124)',
                                    'margin': '8px 0 0 0',
                                    'fontSize': '14px'
                                }
                            )
                        ]
                    ),

                    # Username field
                    html.Div(
                        style={'marginBottom': '20px'},
                        children=[
                            html.Label(
                                "Benutzername",
                                style={
                                    'display': 'block',
                                    'marginBottom': '8px',
                                    'color': 'rgb(75, 75, 75)',
                                    'fontSize': '14px',
                                    'fontWeight': '500'
                                }
                            ),
                            dcc.Input(
                                id='login-username',
                                type='text',
                                placeholder='Geben Sie Ihren Benutzernamen ein',
                                style={
                                    'width': '100%',
                                    'padding': '12px 16px',
                                    'border': '2px solid rgb(208, 208, 208)',
                                    'borderRadius': '8px',
                                    'fontSize': '14px',
                                    'outline': 'none',
                                    'transition': 'border-color 0.3s',
                                    'boxSizing': 'border-box'
                                }
                            )
                        ]
                    ),

                    # Password field
                    html.Div(
                        style={'marginBottom': '25px'},
                        children=[
                            html.Label(
                                "Passwort",
                                style={
                                    'display': 'block',
                                    'marginBottom': '8px',
                                    'color': 'rgb(75, 75, 75)',
                                    'fontSize': '14px',
                                    'fontWeight': '500'
                                }
                            ),
                            dcc.Input(
                                id='login-password',
                                type='password',
                                placeholder='Geben Sie Ihr Passwort ein',
                                style={
                                    'width': '100%',
                                    'padding': '12px 16px',
                                    'border': '2px solid rgb(208, 208, 208)',
                                    'borderRadius': '8px',
                                    'fontSize': '14px',
                                    'outline': 'none',
                                    'transition': 'border-color 0.3s',
                                    'boxSizing': 'border-box'
                                }
                            )
                        ]
                    ),

                    # Remember me and forgot password
                    html.Div(
                        style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center',
                            'marginBottom': '25px'
                        },
                        children=[
                            html.Label(
                                [
                                    dcc.Checklist(
                                        id='remember-me',
                                        options=[{'label': ' Angemeldet bleiben', 'value': 'remember'}],
                                        style={'display': 'inline-block'}
                                    )
                                ],
                                style={
                                    'fontSize': '13px',
                                    'color': 'rgb(124, 124, 124)'
                                }
                            ),
                            html.A(
                                "Passwort vergessen?",
                                href='#',
                                style={
                                    'fontSize': '13px',
                                    'color': 'rgb(80, 117, 141)',
                                    'textDecoration': 'none',
                                    'fontWeight': '500'
                                }
                            )
                        ]
                    ),

                    # Login button
                    html.Button(
                        "Anmelden",
                        id='login-button',
                        n_clicks=0,
                        style={
                            'width': '100%',
                            'padding': '14px',
                            'background': 'linear-gradient(135deg, rgb(110, 149, 178), rgb(80, 117, 141))',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '8px',
                            'fontSize': '16px',
                            'fontWeight': '600',
                            'cursor': 'pointer',
                            'transition': 'transform 0.2s, box-shadow 0.2s',
                            'boxShadow': '0 4px 12px rgba(80, 117, 141, 0.3)'
                        }
                    ),

                    # Error message
                    html.Div(
                        id='login-error',
                        style={
                            'color': 'rgb(216, 40, 47)',
                            'marginTop': '15px',
                            'textAlign': 'center',
                            'fontSize': '14px',
                            'fontWeight': '500'
                        }
                    ),

                    # Sign up link
                    html.Div(
                        style={
                            'textAlign': 'center',
                            'marginTop': '25px',
                            'paddingTop': '25px',
                            'borderTop': '1px solid rgb(230, 230, 230)'
                        },
                        children=[
                            html.Span(
                                "Sie haben noch kein Konto?",
                                style={
                                    'fontSize': '14px',
                                    'color': 'rgb(124, 124, 124)'
                                }
                            ),
                            html.A(
                                "Registrieren",
                                href='#',
                                style={
                                    'fontSize': '14px',
                                    'color': 'rgb(80, 117, 141)',
                                    'textDecoration': 'none',
                                    'fontWeight': '600'
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )