from dash import dcc, html


def get_upload_layout():
    """Return the upload section layout."""
    return html.Div([
        dcc.Upload(
            id='file-upload',
            children=html.Div(['Drag and Drop order', html.A('wähle Datei')]),
            style={
                'width': '100%', 
                'height': '80px', 
                'lineHeight': '80px',
                'borderWidth': '1px', 
                'borderStyle': 'dashed', 
                'borderRadius': '5px',
                'textAlign': 'center', 
                'marginBottom': '10px'
            },
            multiple=False
        ),
        html.Div(id='upload-output-message'),
        #dcc.Store(id='uploaded-cache-key'),
    ], style={"maxWidth": "1100px", "margin": "20px auto"})
