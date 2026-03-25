import pandas as pd
from dash import html, Input, Output, State
from file_loader import FileLoader
import base64
import io
import fitz  # PyMuPDF

def register_upload_callbacks(app, data_manager):
    """Register all upload-related callbacks."""
    
    @app.callback(
        Output('upload-output-message', 'children'),
        Output('uploaded-cache-key', 'data'),
        Input('file-upload', 'contents'),
        State('file-upload', 'filename'),
    )
    def handle_upload(contents, filename):
        if not contents:
            return "Kein Dateien upload.", None

        # ----------------------------
        # Decode contents and detect type
        # ----------------------------
        content_type, content_string = contents.split(',')
        file_bytes = base64.b64decode(content_string)

        # Table files
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes))
            file_type = 'table'
            data_to_store = df

        elif filename.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(file_bytes))
            file_type = 'table'
            data_to_store = df

        # PDF files
        elif filename.lower().endswith('.pdf'):
            doc = fitz.open(stream=file_bytes, filetype='pdf')
            file_type = 'pdf'
            data_to_store = {
                "bytes": file_bytes,          # 🔥 Store actual PDF content
                "page_count": doc.page_count,
                "size_bytes": len(file_bytes)
            }

        else:
            return f"Unsupported file: {filename}", None

        # ----------------------------
        # Store metadata
        # ----------------------------
        metadata = {
            "filename": filename,
            "type": file_type,
            "upload_time": pd.Timestamp.now().isoformat()
        }

        if file_type == 'table':
            metadata["rows"] = len(data_to_store)
            metadata["columns"] = len(data_to_store.columns)

        if file_type == 'pdf':
            metadata["size_bytes"] = data_to_store["size_bytes"]

        # ----------------------------
        # Store in cache
        # ----------------------------
        key = data_manager.store_data(data_to_store, metadata)

        # ----------------------------
        # Return message
        # ----------------------------
        if file_type == 'table':
            return html.Div([
                f"Loaded table: {filename} — rows: {metadata['rows']}, columns: {metadata['columns']}",
                html.Div(f"Cache key: {key}", style={'fontSize':'12px','color':'gray'})
            ]), key

        if file_type == 'pdf':
            return html.Div([
                f"Loaded PDF: {filename} — size: {metadata['size_bytes']} bytes",
                html.Div(f"Cache key: {key}", style={'fontSize':'12px','color':'gray'})
            ]), key
