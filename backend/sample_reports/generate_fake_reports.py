import pandas as pd
from pathlib import Path
p=Path(__file__).parent
pd.DataFrame([{'Выручка':100000,'Количество чеков':420,'Гости':500,'Средний чек':238}]).to_csv(p/'sales.csv',index=False)
pd.DataFrame([{'Поставщик':'FishPro','Накладная':'INV-1','Товар':'Краб клешня','Количество':10,'Ед. изм.':'кг','Цена':2500,'Сумма':25000}]).to_csv(p/'purchases.csv',index=False)
pd.DataFrame([{'Товар':'Лосось','Причина списания':'Порча','Количество':2,'Сумма':3000,'Подразделение':'Кухня'}]).to_csv(p/'writeoffs.csv',index=False)
pd.DataFrame([{'Склад':'Основной','Товар':'Краб клешня','Остаток количество':-1,'Остаток сумма':-2500}]).to_csv(p/'stocks.csv',index=False)
print('generated')
