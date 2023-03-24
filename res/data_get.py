from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from parse import Countres

engine = create_engine('mysql://root:password@localhost:3306/countres')
DBSession = sessionmaker(bind=engine)
session = DBSession()

"""regions = session.query(Countres.region).filter(Countres.id != None).group_by(Countres.region).all()
print (regions)

"""
for regions in session.query(Countres.region, func.max(Countres.population), func.min(Countres.population), func.sum(Countres.population)).group_by(Countres.region).all():
    print (regions[0])
    print (regions[3])
    print(session.query(Countres.country).filter(regions[1] == Countres.population).filter(regions[0] == Countres.region).first()[0])
    print (regions[1])
    print(session.query(Countres.country).filter(regions[2] == Countres.population).filter(regions[0] == Countres.region).first()[0])
    print (regions[2])
    print("..............")
