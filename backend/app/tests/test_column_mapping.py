import pandas as pd
from app.services.report_parser.parsers import parse_rows

def test_sales_mapping(tmp_path):
    p=tmp_path/'s.csv'
    pd.DataFrame([{'Выручка':'1000','Количество чеков':10,'Гости':20,'Средний чек':100}]).to_csv(p,index=False)
    rows=parse_rows(str(p),'sales')
    assert rows[0]['revenue_total']=='1000'
