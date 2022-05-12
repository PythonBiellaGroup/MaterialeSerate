# why don't we add a sqlite database?
import sqlite3 
from bs4 import BeautifulSoup
import requests 
import json 
from math import ceil
import sys 

def create_database(database):
    #Database is the database name, here we will create a
    #connection to X.db

    try:
        conn = sqlite3.connect(database)
        conn.text_factory  =str
    except sqlite3.Error as e:
        print(e)
        sys.exit(-1)
    #the structure of the database is:
    #n_likes, n_comments, shortcode, username_comment, comment_text
    #the icture shortcode it's useful to understand if there have been any
    #point where the candidate has faced serious bad or very good comments
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS house( id  varchar(4000),
                                                        price float,
                                                        caption varchar(4000),
                                                        description  varchar(4000),
                                                        rooms int
                                                           );""")
    return conn

database = create_database("case.db")
# we need to build up the url 
region = "lom"
prov = "MB"
idCom = "8117"
pag = 1 # then this can be computed 
base_url = f"""https://www.immobiliare.it/api-next/search-list/real-estates/?fkRegione={region}&idProvincia={prov}&idComune={idCom}&idContratto=1&idCategoria=1&criterio=rilevanza&__lang=it&pag={pag}&paramsCount=1&path=%2Fvendita-case%2Fvillasanta%2F"""

# in this case we run a while loop, we're exploiting isResultsLimitReached
end_of_results = False 
while not end_of_results:
    req = requests.get(base_url)
    data = json.loads(req.text)
    # store the data 
    for result in data['results']:
        realEstate = result['realEstate']
        id = realEstate['id']
        price = realEstate['price']['value']
        # title
        # properties --> [0]['bathrooms']/caption/description/floor/rooms/location 
        # we coul even download photos
        property = realEstate['properties'][0]
        caption = property['caption']
        description = property['description']
        floor = property['floor']
        rooms = property['rooms']
        location = property['location']
        # send everything to the sql 
        cursor=database.cursor()
        cursor.execute('''INSERT INTO house(id,price,caption,description,rooms)
                                    VALUES (?,?,?,?,?)''',(id,
                                                            price,
                                                            caption,
                                                            description,
                                                            rooms
                                                            ) )
        database.commit()
        # check if we finished 
        end_of_results = bool(data['isResultsLimitReached'])# thank God we're using Python