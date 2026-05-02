from datetime import datetime, date
from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.iiko_mvp import *
from app.services.subject_parser import parse_subject
from app.services.report_parser.parsers import parse_rows
from app.services.report_parser.r02_purchase_prices import R02PurchasePricesParser
from app.services.alerts import evaluate_price_trend

router=APIRouter(tags=['iiko-mvp'])
UPLOAD_DIR=Path('uploads'); UPLOAD_DIR.mkdir(exist_ok=True)
WRITE_OFF_MARKERS=('списание','акт списания','удаление со списанием','порча','комплимент','питание персонала','переработка','проработка')

@router.get('/restaurants')
def get_restaurants(db:Session=Depends(get_db)): return db.query(IikoRestaurant).all()

@router.post('/restaurants')
def create_restaurant(name:str=Form(...), code:str=Form(...), city:str=Form(None), timezone:str=Form('UTC'), db:Session=Depends(get_db)):
    r=IikoRestaurant(name=name, code=code.upper(), city=city, subject_code=code.upper()); setattr(r,'timezone',timezone) if hasattr(r,'timezone') else None
    db.add(r); db.commit(); db.refresh(r); return r

@router.post('/imports/manual-upload')
def manual_upload(restaurant_code:str=Form(...), report_code:str=Form(...), report_date_start:date|None=Form(None), report_date_end:date|None=Form(None), file:UploadFile=File(...), db:Session=Depends(get_db)):
    rest=db.query(IikoRestaurant).filter_by(code=restaurant_code.upper()).first()
    if not rest: raise HTTPException(404,'Restaurant not found')
    if not file.filename.lower().endswith(('.xlsx','.xls','.csv')): raise HTTPException(400,'Unsupported file format')
    meta=parse_subject(f'[{restaurant_code}] {report_code} {report_date_start or date.today()}', file.filename)
    dst=UPLOAD_DIR/f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    with dst.open('wb') as f: shutil.copyfileobj(file.file,f)
    imp=ReportImport(restaurant_id=rest.id, report_type=None, report_date=report_date_start, source='manual', original_filename=file.filename, stored_file_path=str(dst), status=ImportStatus.pending, raw_metadata=meta or {})
    imp.report_name_ru=report_code if hasattr(imp,'report_name_ru') else None
    db.add(imp); db.flush()
    try:
        if report_code=='R02':
            parsed=R02PurchasePricesParser().parse(str(dst))
            imp.raw_metadata=parsed['raw_metadata']
            for row in parsed['rows']:
                db.add(PurchasePriceEvent(restaurant_id=rest.id, report_import_id=imp.id, **row))
            # alerts by product+supplier+unit
            groups={}
            for row in parsed['rows']:
                k=(row.get('product_code'),row.get('product_name'),row.get('supplier_name'),row.get('unit'))
                groups.setdefault(k,[]).append(row)
            for k,vals in groups.items():
                vals=sorted(vals,key=lambda x:x.get('arrival_datetime') or datetime.min)
                first,last=vals[0]['unit_price_with_vat'],vals[-1]['unit_price_with_vat']
                sev,delta=evaluate_price_trend(first,last)
                if sev in ('yellow','red'):
                    db.add(Alert(restaurant_id=rest.id,severity=AlertSeverity[sev],alert_type='purchase_price_growth',title='Рост закупочной цены',message=f"{k[1]}: {first} -> {last} ({delta:.1f}%)",data={'product':k[1],'supplier':k[2]}))
        else:
            key={'R01':'sales','R03':'purchases','R04':'osv','R05':'movement'}.get(report_code)
            if not key:
                imp.status=ImportStatus.unknown; db.commit(); return {'status':'unknown','import_id':imp.id}
            rows=parse_rows(str(dst), key)
            for row in rows:
                if report_code=='R01': db.add(SalesDaily(restaurant_id=rest.id, report_import_id=imp.id, business_date=report_date_start or date.today(), revenue_total=row.get('revenue_total') or 0, orders_count=int(row['orders_count']) if row.get('orders_count') else None, guests_count=int(row['guests_count']) if row.get('guests_count') else None, average_check=row.get('average_check'), raw_data=row['raw_data']))
                elif report_code=='R03': db.add(PurchaseItem(restaurant_id=rest.id, report_import_id=imp.id, business_date=report_date_start or date.today(), **{k:row.get(k) for k in ['supplier_name','invoice_number','product_name','product_code','category','quantity','unit','price','amount','vat']}, raw_data=row['raw_data']))
                elif report_code=='R04':
                    q=row.get('quantity') or 0; a=row.get('amount') or 0
                    db.add(OsvItem(restaurant_id=rest.id, report_import_id=imp.id, business_date=report_date_start or date.today(), is_negative=(q<0 or a<0), **{k:row.get(k) for k in ['warehouse','product_name','product_code','category','quantity','unit','amount']}, raw_data=row['raw_data']))
                elif report_code=='R05':
                    marker=(f"{row.get('operation_type','')} {row.get('document_type','')}").lower()
                    db.add(MovementItem(restaurant_id=rest.id, report_import_id=imp.id, business_date=report_date_start or date.today(), is_writeoff=any(m in marker for m in WRITE_OFF_MARKERS), **{k:row.get(k) for k in ['warehouse','product_name','category','operation_type','document_type','quantity','unit','amount']}, raw_data=row['raw_data']))
        imp.status=ImportStatus.parsed; imp.processed_at=datetime.utcnow(); db.commit()
    except Exception as e:
        imp.status=ImportStatus.failed; imp.error_message=str(e); db.commit(); raise HTTPException(422, f'Parse failed: {e}')
    return {'import_id':imp.id,'status':imp.status.value}

@router.get('/restaurants/{id}/alerts')
def restaurant_alerts(id:int,db:Session=Depends(get_db)): return db.query(Alert).filter_by(restaurant_id=id).order_by(Alert.created_at.desc()).limit(100).all()

@router.post('/email/check-now')
def check_now(): return {'status':'queued'}
@router.get('/restaurants/{id}/imports')
def imports(id:int,db:Session=Depends(get_db)): return db.query(ReportImport).filter_by(restaurant_id=id).order_by(ReportImport.created_at.desc()).limit(100).all()
@router.get('/restaurants/{id}/dashboard')
def dashboard(id:int,db:Session=Depends(get_db)): return {'restaurant_id':id,'latest_imports':db.query(ReportImport).filter_by(restaurant_id=id).count()}
@router.post('/telegram/test-alert/{restaurant_id}')
def t(restaurant_id:int, db:Session=Depends(get_db)):
    a=Alert(restaurant_id=restaurant_id,severity=AlertSeverity.yellow,alert_type='test',title='Test alert',message='Telegram integration placeholder',is_sent=False)
    db.add(a); db.commit(); return {'status':'created'}
