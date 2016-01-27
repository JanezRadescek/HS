import re
import csv


strani = ""
with open('pureHTML2.txt', 'r', encoding="utf-8") as f:      #################################################    <- test  popravi v pureHTML
    strani = f.read()                                  #spet preberemo

vzorec_deck = r'(.*?)kappa123xyz'
strani_decki = re.findall(vzorec_deck, strani, re.DOTALL)       #locimo decke

vzorec_hero = r'span class="class class-(\w+?)">'
vzorec_type = r'deck-type">(\w+?)<'                             #vzorci
vzorec_cost = r'craft-cost">(\d+)'
vzorec_cards = r'<aside class=(.*?)<\/aside'                     #zozimo iskanje (lahko se pojavijo v besedilu)
vzorec_cards30 = r'(.*)<span class="icon-mana"'
vzorec_card = r'<a href="\/cards.*?-(.*?)"'
vzorec_curve = r'<li id="deck-bar.*?data-count="(\d+?)"'



slovar1 = {}
slovar_curve = {}
slovar_cards = []       #z slovarji so problemi pri pisanju ne da se mi useh popravljat
ID = 1
for deck in strani_decki:
    id = ID
    try:                    #nekateri decki so lahko cisto pokvarjeni
        hero = re.search(vzorec_hero, deck, re.DOTALL).group(1)
        type = re.search(vzorec_type, deck, re.DOTALL).group(1)
        cost = re.search(vzorec_cost, deck, re.DOTALL).group(1)
        cards = re.search(vzorec_cards, deck, re.DOTALL).group(1)
        cards30 = re.search(vzorec_cards30, cards, re.DOTALL).group(1)
    except:
        continue
    curve = []
    for a in re.findall(vzorec_curve, deck, re.DOTALL):
        curve.append(a)
    card = []
    for a in re.findall(vzorec_card, cards30, re.DOTALL):
        card.append(a)
    d = len(card)
    for a in range(30-d):
        card.append(None)

    slovar1[id] = [id, hero, type, cost]
    slovar_curve[id] = [id] + curve
    slovar_cards.append([id] + card)

    ID += 1

with open('CSV1.csv', 'w') as csvfile:
    fieldnames = ['id', 'hero', 'type', 'cost']
    wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
    wr.writeheader()
    for id in slovar1:
        wr.writerow({'id': slovar1[id][0], 'hero': slovar1[id][1], 'type': slovar1[id][2], 'cost': slovar1[id][3]})

with open('CSV_curve.csv', 'w') as csvfile:
    fieldnames = ['id', '0', '1', '2', '3', '4', '5','6', '7']
    wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
    wr.writeheader()
    for id in slovar_curve:
        wr.writerow({'id': slovar_curve[id][0], '0': slovar_curve[id][1], '1': slovar_curve[id][2], '2': slovar_curve[id][3],
                     '3': slovar_curve[id][4], '4': slovar_curve[id][5], '5': slovar_curve[id][6], '6': slovar_curve[id][7], '7': slovar_curve[id][8]  })


with open('CSV_cards.csv', 'w') as csvfile:
    fieldnames = ['id']
    for a in range(30):
        fieldnames.append(str(a+1))
    wr = csv.writer(csvfile)
    wr.writerow(fieldnames)
    wr.writerows(slovar_cards)
