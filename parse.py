import requests
from lxml import etree
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy import create_engine, func

Base = declarative_base()
engine = create_engine('mysql://root:password@localhost:3306/countres')


class Countres(Base):
    __tablename__ = "country" 
    #metadata = MetaData()   
    id = Column(Integer, primary_key=True)
    country = Column(String(50), nullable=True)
    population= Column(Integer, nullable=False)
    region = Column(String(50), nullable=True)  



engine = create_engine('mysql://root:password@localhost:3306')

print(Base.metadata.tables["country"])

with engine.connect() as conn:
    #if Base.metadata.tables["countres"] != "countres":
    conn.execute("CREATE DATABASE IF NOT EXISTS countres")
    conn.execute("USE countres")

Base.metadata.create_all(engine)    
DBSession = sessionmaker(bind=engine)
session = DBSession()

regions_url = 'https://meta.wikimedia.org/wiki/List_of_countries_by_regional_classification'
regions_r = requests.get(regions_url)
regions_html = etree.HTML(regions_r.content)
data_regions = regions_html.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody')

region_dict = {}
for i in range(1, len(data_regions[0])):
    region_dict[f"{data_regions[0][i][0].text}".replace('\n', '')] = f"{data_regions[0][i][1].text}".replace('\n', '')

country_url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
country_r = requests.get(country_url)
country_html = etree.HTML(country_r.content)
data = country_html.xpath('/html/body/div[1]/div/div[3]/main/div[3]/div[3]/div[1]/table[2]/tbody')


def region_add (_region):
    global region_dict
    try:
        region_data = region_dict[country.country]
    except KeyError:
        for k, v in region_dict.items():
            if _region[3] in k or k in _region:
                region_data = v
    return  region_data                 


for i in range(3, len(data[0])):
    country = Countres(population=data[0][i][2].text.replace(',', ''))       
    #print(country.population)

    for j in (data[0][i][1]):       
        #print(j[0])
        if j.text != None:
            country.country =j.text
            country.region = region_add (country.country)
      
        if country.region == None:
            for l in j:
                #print(l)
                if l.text != None:                    
                    country.country =l.text
                    country.region = region_add (country.country)       

    #print(country.country)
    #print(country.region)
    session.add(country)
    session.commit()



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
