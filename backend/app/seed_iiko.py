from app.db.session import SessionLocal
from app.models.iiko_mvp import IikoRestaurant

def run():
    db=SessionLocal()
    for code,name in [('SOCHI','Klevo Sochi'),('ROSTOV','Klevo Rostov'),('SAKHALIN','Klevo Sakhalin')]:
        if not db.query(IikoRestaurant).filter_by(code=code).first():
            db.add(IikoRestaurant(code=code,name=name))
    db.commit(); db.close(); print('seeded')

if __name__=='__main__': run()
