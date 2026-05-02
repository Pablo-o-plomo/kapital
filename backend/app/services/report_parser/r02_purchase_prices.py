from datetime import datetime
import pandas as pd
from app.services.report_parser.base import to_num, normalize_col

class R02PurchasePricesParser:
    def parse(self, file_path: str):
        df = pd.read_excel(file_path, header=None) if file_path.endswith(('xlsx','xls')) else pd.read_csv(file_path, header=None)
        metadata_rows=[]
        header_idx=0
        for i,row in df.iterrows():
            vals=[str(v) for v in row.tolist()]
            if any('товар' in normalize_col(v) for v in vals):
                header_idx=i; break
            metadata_rows.append(vals)
        headers=[normalize_col(v) for v in df.iloc[header_idx].tolist()]
        data=df.iloc[header_idx+1:].copy(); data.columns=headers
        col=lambda *names: next((c for c in data.columns for n in names if n in c), None)
        c_prod=col('товар'); c_code=col('артикул'); c_dt=col('дата и время'); c_supplier=col('поставщик'); c_doc=col('номер документа')
        c_sup_prod=col('продукт поставщика'); c_price=col('цена за ед. с ндс','цена с ндс, р.'); c_price2=col('цена с ндс, р.'); c_unit=col('фасовка'); c_pl=col('цена по прайс'); c_dev_r=col('отклонение цены, р'); c_dev_p=col('отклонение цены, %')
        data[c_prod]=data[c_prod].ffill(); data[c_code]=data[c_code].ffill()
        out=[]
        for _,r in data.iterrows():
            raw=r.to_dict()
            if any('всего' in str(v).lower() for v in raw.values()):
                continue
            if pd.isna(r.get(c_dt)): continue
            price=to_num(r.get(c_price)) or to_num(r.get(c_price2))
            if price is None: continue
            out.append({
                'product_name': r.get(c_prod), 'product_code': r.get(c_code),
                'arrival_datetime': pd.to_datetime(r.get(c_dt), dayfirst=True, errors='coerce').to_pydatetime() if pd.notna(r.get(c_dt)) else None,
                'supplier_name': r.get(c_supplier), 'invoice_number': r.get(c_doc), 'supplier_product_name': r.get(c_sup_prod), 'unit': r.get(c_unit),
                'price_with_vat': to_num(r.get(c_price2)), 'unit_price_with_vat': price, 'pricelist_price': to_num(r.get(c_pl)), 'price_deviation_rub': to_num(r.get(c_dev_r)), 'price_deviation_percent': to_num(r.get(c_dev_p)), 'raw_data': raw,
            })
        return {'rows': out, 'raw_metadata': {'header_rows': metadata_rows}}
