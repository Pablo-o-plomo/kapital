from app.services.alerts import evaluate_price_trend

def test_yellow(): assert evaluate_price_trend(100,108)[0]=='yellow'
def test_red(): assert evaluate_price_trend(100,116)[0]=='red'
def test_positive(): assert evaluate_price_trend(100,94)[0]=='positive'
