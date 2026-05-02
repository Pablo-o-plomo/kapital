from app.services.subject_parser import parse_subject

def test_r02_subject():
    s='[SOCHI] R02 Закупочные цены 2026-04-20_2026-04-26'
    r=parse_subject(s)
    assert r['restaurant_code']=='SOCHI' and r['report_code']=='R02'

def test_r01_subject():
    r=parse_subject('[ROSTOV] R01 Продажи за период 2026-05-01')
    assert r['report_code']=='R01'

def test_unknown_code():
    r=parse_subject('[ROSTOV] XYZ 2026-05-01')
    assert r['report_code']=='UNKNOWN'
