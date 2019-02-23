import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.riteh.uniri.hr/")
soup = BeautifulSoup(page.content, 'html.parser')
naslovi = soup.find_all('h3')
opisi = soup.findAll("div", {"class": "summary"})
datumi = soup.find_all('dd')
file = open("C:/Users/Korisnik/PycharmProjects/SmartMirror/data.txt", "w")
file.write("###") #kao neki delimiter između novih vijesti
for i in range(len(naslovi)):
    vijest = "\n" + datumi[i].get_text() + naslovi[i].get_text() + opisi[i].get_text() + "\n" + "###"
    file.write(vijest)
file.close()

