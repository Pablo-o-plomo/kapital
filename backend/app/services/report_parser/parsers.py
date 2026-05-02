from app.services.report_parser.base import load_df, normalize_col, to_num
MAP = {
'sales': {'revenue_total':['выручка','revenue','sales','сумма'],'orders_count':['количество чеков','orders_count','checks'],'guests_count':['гости','guests_count'],'average_check':['средний чек','average_check']},
'purchases': {'supplier_name':['поставщик'],'invoice_number':['накладная'],'product_name':['товар'],'product_code':['код товара'],'category':['категория'],'quantity':['количество'],'unit':['ед. изм.','ед изм'],'price':['цена'],'amount':['сумма'],'vat':['ндс','vat']},
'movement': {'warehouse':['склад'],'product_name':['товар'],'category':['категория'],'operation_type':['тип операции','операция'],'document_type':['тип документа','документ'],'quantity':['количество'],'unit':['ед. изм.'],'amount':['сумма']},
'osv': {'warehouse':['склад'],'product_name':['товар'],'product_code':['код товара'],'category':['категория'],'quantity':['остаток количество','количество'],'unit':['ед. изм.'],'amount':['остаток сумма','сумма']}
}
NUM_FIELDS={'revenue_total','orders_count','guests_count','average_check','quantity','price','amount','vat'}

def parse_rows(path, key):
    df=load_df(path).dropna(how='all')
    cols={normalize_col(c):c for c in df.columns}
    out=[]
    for _,r in df.iterrows():
        row={}
        for f,variants in MAP[key].items():
            src=next((cols[v] for v in variants if v in cols),None)
            val=r[src] if src is not None else None
            row[f]=to_num(val) if f in NUM_FIELDS else val
        row['raw_data']={str(k): (None if str(v)=='nan' else v) for k,v in r.to_dict().items()}
        out.append(row)
    return out
