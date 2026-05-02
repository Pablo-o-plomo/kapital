def evaluate_price_trend(first_price: float, last_price: float):
    if not first_price or not last_price:
        return None
    change_pct=(last_price-first_price)/first_price*100
    if change_pct>15: return 'red', change_pct
    if change_pct>7: return 'yellow', change_pct
    if change_pct<-5: return 'positive', change_pct
    return None, change_pct
