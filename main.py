import json
from bs4 import BeautifulSoup
from unidecode import unidecode
import os
import re

class Document:

    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as file:
            self.json = json.load(file)
        # self.nom = getNom()
        # self.prenom = getPrenom()

    def getTitle(self):
        soup = BeautifulSoup(self.json['content']['rendered'], 'lxml')

        try:

            p=soup.find('h1')
            p.extract()
            return p.text.strip(" -*")

        except AttributeError:

            #print('pas de H1 pour ', self.filename) #pas de H1 pour  json/4104.json
            return ""

    def getName(self):
        title = unidecode(self.getTitle())

        if title:

            prenom = r'[A-Z][a-z]+(?:-[A-Z][a-z]+)*'
            nom = r'[A-Z]+'
            regex = rf'^({prenom}(?: {prenom})* )?({nom})'
            m = re.match(regex, title)

            try:
                return m.group(1), m.group(2)
            except AttributeError:
                return (None, None)

        else:
            return (None, None)

    def isPerson(self):
        name = any(self.getName())
        slug = self.getSlug()
        
        regex = r'^[a-z]{3,4}-\d{4}[a-z]$'

        slug_person = bool(re.match(regex, slug))

        # print(f"name: {name} | slug_person: {slug_person}")

        return name or slug_person


    def getSlug(self):
        return self.json['slug']
    
    def getDate(self):
        soup = BeautifulSoup(self.json['content']['rendered'], 'lxml')
        try:
            p=soup.find_all('h2',{"class":"has-text-align-center"})
            for h2 in p:
                #gestion br
                if "<br/>" in str(h2):
                    # print(h2)
                    datas=str(h2).split("<br/>")
                    for d in datas:
                        for m in ["janvier","février","fevrier","mars","avril","mai","juin","juillet","aout","août","septembre","octobre","novemembre","decembre","décembre"]:
                            if m in d:
                                return re.sub('<.*?>', '', d)

                h2.extract()
                txt=h2.text.strip()
                
                for m in ["janvier","février","fevrier","mars","avril","mai","juin","juillet","aout","août","septembre","octobre","novemembre","decembre","décembre"]:
                    if m in txt:
                        return txt 
            return "Inconnue"
    
        except AttributeError:
            #print('pas de H2 pour ', self.filename) 
            return None
    
    def getSaved(self):
        soup = BeautifulSoup(self.json['content']['rendered'], 'lxml')
        try:
            p=soup.find_all('h2',{"class":"has-text-align-center"})
            
            for h2 in p:
                #gestion br
                if "<br/>" in str(h2):
                    # print(h2)
                    datas=str(h2).split("<br/>")
                    for d in datas:
                        for filt in ["homme","femme","enfant","sauve","sauvé","sauvés"]:
                            if filt in d:
                                return re.sub('<.*?>', '', d)
                h2.extract()
                txt=h2.text.strip()
                for filt in ["homme","femme","enfant","sauve","sauvé","sauvés"]:
                    if filt in txt:
                        return txt 
            return "Inconnu"
    
        except AttributeError:
            #print('pas de H2 pour ', self.filename) 
            return None
    
    def getParticipants(self):
        soup = BeautifulSoup(self.json['content']['rendered'], 'lxml')
        try:
            p=soup.find('sup')
            #print("participant" in str(p).lower())
            if ("participant" in str(p).lower()):
                #print("P:",p)
                p.extract()
                txt=p.text.strip()
                #print(type(txt))
                #print("TXT :",txt) 
                txt=re.sub('<.*?>', '', txt)
                txt=re.sub('^.*:', '', txt)
                txt=txt.split("-")
                return txt
            return []
        except AttributeError:
            #print('pas de H2 pour ', self.filename) 
            return None

if __name__ == '__main__':
    print("parsing...")
    sauvetages = []
    assistances = []
    personnes = []

    for filename in os.listdir("./json"):

        doc = Document("json/"+filename)
        title = doc.getTitle().strip('-*')
        slug = doc.getSlug()
        if type(title) == str: 
            #gestion des sauvetages
            if "sauvetage" in title.lower():
                #print("SAVE",filename)

                infos = {
                    "title":title,
                    "filename":filename,
                    "slug": slug,
                    "date":doc.getDate(),
                    "saved":doc.getSaved(),
                    "participants":doc.getParticipants()
                }
                sauvetages.append(infos)
            #gestion des assitances
            elif "assistance" in title.lower(): # marqué en h4, 6503.json
                infos = {
                    "title":title,
                    "filename":filename,
                    "slug": slug
                }
                assistances.append(infos)
            elif doc.isPerson():
                prenom, nom = doc.getName()
                if prenom: prenom = prenom.strip()
                if nom: nom = nom.strip()
                print(title)
                infos = {
                    "title": title,
                    "nom": nom,
                    "prenom": prenom,
                    "filename":filename,
                    "slug": slug
                }
                personnes.append(infos)
    # the json file where the output must be stored
    # --------- SAUVETAGES
    print("saving...")
    with open("result/sauvetages.json", "w") as file:
        json.dump(sauvetages, file, indent = 4)

    with open("result/personnes.json", "w") as file:
        json.dump(personnes, file, indent = 4)
    print("done !")
    
    # print(Document("json/1285.json").getTitle())
            