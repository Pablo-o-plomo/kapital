from dataclasses import dataclass
import pandas as pd
@dataclass
class ParsedReport:
    rows: list[dict]

def normalize_col(c:str)->str:
    return str(c).strip().lower().replace('ё','е').replace('\n',' ').replace('  ',' ')

def to_num(v):
    if v is None: return None
    s=str(v).replace('₽','').replace(' ','').replace(',','.')
    try:return float(s)
    except:return None

def load_df(path:str):
    if path.lower().endswith('.csv'):
        return pd.read_csv(path)
    return pd.read_excel(path)
