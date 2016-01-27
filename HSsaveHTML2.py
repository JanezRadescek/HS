import re
import requests

url = r'http://www.hearthpwn.com/decks?page='   #osnovna stran s katere pobiramo

stStrani = 10               #omejitev

urls = []
for a in range(1,stStrani+1):
    urls.append(url + str(a))   #straniiiiiiii

print(urls)

#deeper
#
#

vzorec = r'<a\shref="\/decks\/(.+?)">'

kon_stran = []

for a in urls:
    iskano = re.findall(vzorec, requests.get(a).text, re.DOTALL)

    print(iskano)

    for b in range(len(iskano)):

        kon_stran.append(r'http://www.hearthpwn.com/decks/' + iskano[b])


with open('pureHTML2.txt', 'w', encoding="utf-8") as f:
    for stran in kon_stran:
        f.write(requests.get(stran).text)

        f.write("kappa123xyz")         #locevanje
