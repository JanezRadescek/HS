import re
import csv



stStrani = 3       #omejitev

strani = ""
with open('pureHTML2.txt', 'r', encoding="utf-8") as f:      #################################################    <- test  popravi v pureHTML
    strani = f.read()                                  #spet preberemo

vzorec_deck = r'(.*?)kappa123'
strani_decki = re.findall(vzorec_deck, strani, re.DOTALL)       #locimo decke

vzorec_hero = r'span class="class class-(\w+?)">'
vzorec_type = r'deck-type">(\w+?)<'                             #vzorci
vzorec_cost = r'craft-cost">(\d+)'
vzorec_cards = r'<aside class(.*?)<\/aside'                     #zozimo iskanje (lahko se pojavijo v besedilu)
vzorec_card = r'<a href="\/cards.*?-(.*?)"'
vzorec_curve = r'<li id="deck-bar.*?data-count="(\d+?)"'



slovar = {}
ID = 1
for deck in strani_decki:
    id = ID
    ID += 1
    hero = re.search(vzorec_hero, deck, re.DOTALL).group(1)
    type = re.search(vzorec_type, deck, re.DOTALL).group(1)
    cost = re.search(vzorec_cost, deck, re.DOTALL).group(1)
    curve = []
    for a in re.findall(vzorec_curve, deck, re.DOTALL):
        curve.append(a)

    cards = re.search(vzorec_cards, deck, re.DOTALL).group(1)
    card = []
    for a in re.findall(vzorec_card, cards, re.DOTALL):
        card.append(a)



    print(type)
    print(cost)
    print(curve)
    print(card)

    slovar[id]=[hero, type, cost, curve, card]

with open('CSV1.csv', 'w') as csvfile:
    fieldnames = ['hero', 'type', 'cost', 'curve', 'card']
    wr = csv.DictWriter(csvfile, fieldnames=fieldnames)

    wr.writeheader()
    for id in slovar:
        print(slovar[id])
        wr.writerow({'hero': slovar[id][0], 'type': slovar[id][1], 'cost': slovar[id][2], 'curve': slovar[id][3], 'card': slovar[id][4]})