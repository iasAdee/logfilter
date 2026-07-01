
# file_loader.py
import base64
import io
from typing import Any, Dict
import pandas as pd


class FileLoader:
    """Load Excel, CSV, or PDF files safely without xlrd."""
    
    @staticmethod
    def _load_csv(decoded: bytes) -> pd.DataFrame:
        encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252", "iso-8859-1"]
        delimiters = [",", ";", "\t"]
        for enc in encodings:
            for sep in delimiters:
                try:
                    df = pd.read_csv(io.BytesIO(decoded), encoding=enc, sep=sep)
                    if df.shape[1] > 1 or len(df) > 0:
                        return df
                except Exception:
                    continue
        try:
            return pd.read_csv(io.BytesIO(decoded))
        except Exception:
            return pd.DataFrame()

    @staticmethod
    def _load_excel(decoded: bytes) -> pd.DataFrame:
        try:
            return pd.read_excel(io.BytesIO(decoded), sheet_name=0, engine='openpyxl')
        except Exception:
            try:
                return pd.read_excel(io.BytesIO(decoded), sheet_name=0)
            except Exception:
                return pd.DataFrame()

    @staticmethod
    def _load_pdf(decoded: bytes) -> Dict[str, Any]:
        return {"page_count": -1, "size_bytes": len(decoded)}

    @staticmethod
    def load_from_contents(contents: str, filename: str) -> Dict[str, Any]:
        if not contents:
            return {"type": "none", "data": None, "filename": filename}
        
        content_type, content_string = contents.split(",", 1)
        decoded = base64.b64decode(content_string)
        filename_lower = (filename or "").lower()

        if filename_lower.endswith(".csv"):
            df = FileLoader._load_csv(decoded)
            df.columns = df.columns.astype(str).str.strip()
            return {"type": "table", "data": df, "filename": filename}

        if filename_lower.endswith(('.xls', '.xlsx')):
            df = FileLoader._load_excel(decoded)
            df.columns = df.columns.astype(str).str.strip()
            return {"type": "table", "data": df, "filename": filename}

        if filename_lower.endswith('.pdf'):
            info = FileLoader._load_pdf(decoded)
            return {"type": "pdf", "data": info, "filename": filename}

        return {"type": "unknown", "data": None, "filename": filename}
