import re
import csv

from bottle import *
import auth
import csv
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki




strani = ""
with open('pureHTML2.txt', 'r', encoding="utf-8") as f:      #################################################    <- test  popravi v pureHTML
    strani = f.read()                                  #spet preberemo

#vzorci za RE
if True:
    vzorec_deck = r'(.*?)kappa123xyz'
    strani_decki = re.findall(vzorec_deck, strani, re.DOTALL)       #locimo decke

    vzorec_hero = r'span class="class class-(\w+?)">'                         #vzorci
    vzorec_cost = r'craft-cost">(\d+)'
    vzorec_cards = r'<aside class=(.*?)<\/aside'                     #zozimo iskanje (lahko se pojavijo v besedilu)
    vzorec_cards30 = r'(.*)<span class="icon-mana"'
    vzorec_card = r'<a href="\/cards.*?-(.*?)"'
    vzorec_curve = r'<li id="deck-bar.*?data-count="(\d+?)"'
    vzorec_mana = r'class="col-cost">(\d+?)<span'
    vzorec_stevilo = r'×\s(\d)\s*?</td><td class="col'

#slovar herojev
if True:
    heros = {}
    heros["druid"] = 1
    heros["hunter"] = 2
    heros["mage"] = 3
    heros["paladin"] = 4
    heros["priest"] = 5
    heros["rogue"] = 6
    heros["shaman"] = 7
    heros["warlock"] = 8
    heros["warrior"] = 9
    heros["vsi"] = 123

slovar1 = {}
ID = 1
for deck in strani_decki:
    try:                    #nekateri decki so lahko cisto pokvarjeni
        hero1 = re.search(vzorec_hero, deck, re.DOTALL).group(1)
        hero = heros[hero1]
        cost = re.search(vzorec_cost, deck, re.DOTALL).group(1)
        cards = re.search(vzorec_cards, deck, re.DOTALL).group(1)
        cards30 = re.search(vzorec_cards30, cards, re.DOTALL).group(1)

    except:
        continue

    card = []
    for ime,mana,stevilo in zip(re.findall(vzorec_card, cards30, re.DOTALL),re.findall(vzorec_mana,cards30,re.DOTALL),re.findall(vzorec_stevilo,cards30, re.DOTALL)):
        card.append((ime,mana,stevilo))

    slovar1[ID] = [ID, hero, cost, card]

    ID += 1







#ponjenje baze

#vrne zadni id se pravi id decka, ki smo ga ravnokar not dali
def getIDdecka():
    cur.execute("SELECT id FROM deck ORDER BY id desc LIMIT 1")
    for id in cur:
        return id

#vzame ime in vrne id karte
def getIDkarte(imekarte):
    imekarte = re.sub('-','',imekarte)
    cur.execute("SELECT id FROM karte WHERE regexp_replace(lower(ime), '[^a-zA-Z0-9]+', '', 'g') = (%s)",[imekarte])
    for id in cur:
        return id



conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogocimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


for a in slovar1:
    #vnesemo ime v bazo. rabimo id za to da lahko napolnimo tabelo jevdecku
    row = slovar1[a]  #a je samo ključ
    slabdeck = False
    karte = []
    for karta1 in row[3]: #v 3 so karte
        imekarte = karta1[0]
        IDkarte = getIDkarte(imekarte)
        if IDkarte is None:
            slabdeck = True
            break
        karte.append([IDkarte[0],karta1[2]])


    if slabdeck:
        pass
    else:
        cur.execute("INSERT INTO deck (ime,avtor) VALUES (%s,%s);", ['unknown', 'unknown'])
        IDdecka = getIDdecka()
        for karta1 in karte:
            cur.execute("INSERT INTO jevdecku (karta,deck,stevilo) VALUES (%s,%s,%s);",
                        [karta1[0], IDdecka[0], karta1[1]])
