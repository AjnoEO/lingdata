import re
import csv

genroj = {"m": "Maskla", "f": "Femala"}
plena_nomaro = []
dubindaj_nomoj = []
homoj = {}
with open("nomaro.txt", encoding="utf-8") as d:
    for linio in d:
        if linio[-1] == "\n":
            linio = linio[:-1]
        genro = "Negrava"
        if linio[-2] == " ":
            genro = genroj[linio[-1]]
            linio = linio[:-2]
        nomoj = linio.split()
        identigilo = nomoj[0]
        if len(nomoj) > 1 and "  " not in linio:
            identigilo += " " + nomoj[1]
        homoj[identigilo] = {"nomoj": nomoj, "genro": genro}
        for nomo in nomoj:
            if nomo in plena_nomaro:
                dubindaj_nomoj.append(nomo)
            else:
                plena_nomaro.append(nomo)

with open("cxu_vi_kuiras_cxine.txt", encoding="utf-8") as d:
    alineoj = d.readlines()

vokaloj = "aeiou"
akcentaj_vokaloj = "áéíóú"

def normaligi(teksto):
    for akcenta_vokalo in akcentaj_vokaloj:
        if akcenta_vokalo in teksto:
            vokalo = vokaloj[akcentaj_vokaloj.index(akcenta_vokalo)]
            teksto = re.sub(r"([A-ZĈĜĤĴŜŬa-zĉĝĥĵŝŭ]+)" + re.escape(akcenta_vokalo) + r"(.*)", r"\1" + vokalo + r"\2" + "'", teksto)
    teksto = teksto.replace("'", "o")
    return teksto

def partoprenas(homo, alineo):
    alineo = normaligi(alineo)
    for nomo in homo["nomoj"]:
        if nomo not in dubindaj_nomoj:
            if re.search(r"\b" + re.escape(nomo) + r"n?\b", alineo):
                return True
        elif homo["genro"] == "Femala":
            if re.search(r"\b(([Ss](injor|injaŭl|-)|[Ff](raŭl|-))[ií]n[o']n?|[Gg]es(inj[oó]|-)r[o']jn?) " + re.escape(nomo) + r"n?\b", alineo):
                return True
        else:
            if re.search(r"((([Gg]e)?[Ss](inj[oó]|-)|[Dd](okt[oó]|-))r[o']j?n?) " + re.escape(nomo) + r"n?\b", alineo):
                return True
    return False

antauxnelongaj = [[] for _ in range(5)]
rilatoj = {}
for i in range(len(list(homoj))):
    for j in range(len(list(homoj))):
        rilatoj[list(homoj)[i] + "," + list(homoj)[j]] = 0
for alineo in alineoj:
    antauxnelongaj = antauxnelongaj[1:] + [[]]
    for homo in homoj:
        if partoprenas(homoj[homo], alineo):
            antauxnelongaj[-1].append(homo)
    for homo in antauxnelongaj[-1]:
        for k in range(len(antauxnelongaj)):
            for apudulo in antauxnelongaj[k]:
                if apudulo != homo:
                    rilatoj[apudulo + "," + homo] += 1 + k
                    rilatoj[homo + "," + apudulo] += 1 + k

with open("rezulto.csv", encoding='utf-8', mode="w", newline='') as csv_dosiero:
    enhavo = []
    for homo in homoj:
        csv_dosiero.write("," + homo)
    csv_dosiero.write("\n")
    for homo in homoj:
        csv_dosiero.write(homo)
        for apudulo in homoj:
            csv_dosiero.write("," + str(rilatoj[homo + "," + apudulo]))
        csv_dosiero.write("\n")