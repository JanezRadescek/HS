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

    #nakonec dodamo none če ni 30 različnih kart
    d = len(card)
    for a in range(30-d):
        card.append(None)


    slovar1[ID] = [ID, hero, cost, card]

    ID += 1


#ponjenje baze

#vrne zadni id
def getIDdecka():
    cur.execute("SELECT id FROM deck ORDER BY id desc LIMIT 1")
    return cur[0]

def getIDkarte(imekarte):
    cur.execute("SELECT id FROM karte WHERE ime = (%s)",[imekarte])
    return cur[0]



conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogocimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

ime = 1
for row in slovar1:
    #vnesemo ime v bazo. rabimo id za to da lahko napolnimo tabelo kartajevdecku
    cur.execute("INSERT INTO deck (ime,avtor) VALUES (%s,%s);", [str(ime),str(ime)])
    IDdecka = getIDdecka()
    for karta1 in row[3]:
        imekarte = karta1[1]
        IDkarte = getIDkarte(imekarte)
        cur.execute("INSERT INTO jevdecku (karta,deck,stevilo) VALUES (%s,%s,%s);",[IDkarte,IDdecka,karta1[2]])

    ime += 1


print("hahahah")