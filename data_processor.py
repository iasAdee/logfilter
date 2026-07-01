import pandas as pd
from typing import Dict, Any, List


class DataProcessor:
    """Example module for processing uploaded data."""
    
    @staticmethod
    def get_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics for a DataFrame."""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_columns": df.select_dtypes(include=['number']).columns.tolist()
        }
    
    @staticmethod
    def filter_data(df: pd.DataFrame, conditions: Dict[str, Any]) -> pd.DataFrame:
        """Filter DataFrame based on conditions."""
        filtered = df.copy()
        for col, value in conditions.items():
            if col in filtered.columns:
                filtered = filtered[filtered[col] == value]
        return filtered
    
    @staticmethod
    def aggregate_data(df: pd.DataFrame, group_by: List[str], agg_cols: Dict[str, str]) -> pd.DataFrame:
        """Aggregate data by grouping columns."""
        if not group_by or not agg_cols:
            return df
        return df.groupby(group_by).agg(agg_cols).reset_index()
