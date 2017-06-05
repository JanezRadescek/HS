import re
import requests

#url = r'http://www.hearthpwn.com/decks?page='   #osnovna stran s katere pobiramo
url = r'http://www.hearthpwn.com/cards?display=1&filter-premium=1&page='

stStrani = 12               #omejitev

urls = []
for a in range(1,stStrani+1):
    urls.append(url + str(a))   #straniiiiiiii

#deeper
#
#

#vzorec = r'<a\shref="\/decks\/(.+?)">'

vzorec_rarity = r'<a class="rarity-(\d) set'
vzorec_expansion = r'set-(\d+?) manual-data'
#vzorec_ime = r'a class="rarity-(\d) set\*?>(\w+?)</a>'
vzorec_ime = r'a class="rarity-\d set(\w|\W)*?>((\w|\W)*?)</a>'
vzorec_mana = r'col-cost">(\d)<span'
vzorec_class_vsi = r'<td class="col-class">(.*?)col-cost'
vzorec_je_class = r'span class="class-(\w+?)"'


karte = []

for a in urls:
    konkretna_stran = requests.get(a).text
    imeee = re.findall(vzorec_ime, konkretna_stran, re.DOTALL)
    expansion = re.findall(vzorec_expansion, konkretna_stran, re.DOTALL)
    rarity = re.findall(vzorec_rarity, konkretna_stran, re.DOTALL)
    mana = re.findall(vzorec_mana, konkretna_stran, re.DOTALL)
    clasa = re.findall(vzorec_class_vsi, konkretna_stran, re.DOTALL)

    ime = []
    for b in imeee:
        bb = re.findall(r'(\.*?)&#x27;(\.*?)',b[1], re.DOTALL)
        cc = re.sub(r'&#x27;','\'',b[1])
        ime.append(cc)

    for b,c,d,e,f in zip(ime,expansion,rarity,mana,clasa):
        #ff je kratek izsek kjer se morda nahaja ime classe
        ff = re.findall(vzorec_je_class, f, re.DOTALL)

        if ff.__len__() == 0:
            fff = "vsi"
        else:
            fff = ff[0]

        karte.append([b,c,d,e,fff])





with open('pureHTML2_karte.txt', 'w', encoding="utf-8") as f:
    for karta in karte:
        f.write(";".join(karta))
        f.write("\n")


