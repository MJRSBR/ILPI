import numpy as np
import pandas as pd

def _safe_col(df, name):
    return df[name] if name in df.columns else pd.Series([np.nan]*len(df), index=df.index)
