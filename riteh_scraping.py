import requests
from bs4 import BeautifulSoup

def scrape_me():
    page = requests.get("http://www.riteh.uniri.hr/")
    soup = BeautifulSoup(page.content, 'html.parser')
    naslovi = soup.find_all('h3')
    opisi = soup.findAll("div", {"class": "summary"})
    datumi = soup.find_all('dd')
    file = open("data.txt", "w")
    file.write("###\n") #kao neki delimiter između novih vijesti
    for i in range(len(naslovi)):
        vijest = datumi[i].get_text() + naslovi[i].get_text() + opisi[i].get_text() + "\n" + "###\n"
        file.write(vijest)
    file.close()

scrape_me()