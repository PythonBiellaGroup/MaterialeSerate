# scrape immobiliare.it 
# Sometimes our inspection analysis is more fruitful than we can think
# teach how to use inspect Network 
# you can see whne you're going on the second page this link
# https://www.immobiliare.it/api-next/search-list/real-estates/?fkRegione=lom&idProvincia=MB&idComune=8117&idContratto=1&idCategoria=1&criterio=rilevanza&__lang=it&pag=2&paramsCount=1&path=%2Fvendita-case%2Fvillasanta%2F 
# which returns a json 
# the method is still GET --> api call 
from bs4 import BeautifulSoup
import requests 
import json 
from math import ceil
# we need to build up the url 
region = "lom"
prov = "MB"
idCom = "8117"
pag = 1 # then this can be computed 
base_url = f"""https://www.immobiliare.it/api-next/search-list/real-estates/?fkRegione={region}&idProvincia={prov}&idComune={idCom}&idContratto=1&idCategoria=1&criterio=rilevanza&__lang=it&pag={pag}&paramsCount=1&path=%2Fvendita-case%2Fvillasanta%2F"""

req = requests.get(base_url)
data = json.loads(req.text)
# from data['count'] we have the total number of properties 
# we have 25 props per page so 109/25 
tot_pages = ceil(int(data['count'])/25)

#data['results'] is a list with all the info we want 
# data['results'][NUMB]['realEstate']
# advertiser --> agency -->displayName 
# price
# properties has all the info we want 

for pages in range(2, tot_pages+1):
    # new url 
    base_url = f"""https://www.immobiliare.it/api-next/search-list/real-estates/?fkRegione={region}&idProvincia={prov}&idComune={idCom}&idContratto=1&idCategoria=1&criterio=rilevanza&__lang=it&pag={pages}&paramsCount=1&path=%2Fvendita-case%2Fvillasanta%2F"""
    req = requests.get(base_url)
    data = json.loads(req.text)
    # here for every property we can save a file