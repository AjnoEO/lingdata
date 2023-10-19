import re

dosiernomo = "cxu_vi_kuiras_cxine.txt"
plena_nomaro = []
vokaloj = "aeiou"
akcentaj_vokaloj = "áéíóú"

def normaligi(vorto):
    for akcenta_vokalo in akcentaj_vokaloj:
        if akcenta_vokalo in vorto:
            vokalo = vokaloj[akcentaj_vokaloj.index(akcenta_vokalo)]
            vorto = re.sub(r"([A-ZĈĜĤĴŜŬa-zĉĝĥĵŝŭ]+)" + re.escape(akcenta_vokalo) + r"(.*)", r"\1" + vokalo + r"\2" + "'", vorto)
    if vorto[-1] == "'":
        vorto = vorto[:-1] + "o"
    if vorto[-1] == "n" and vorto[-2] in vokaloj + "j":
        vorto = vorto[:-1]
    if vorto[-1] == "j" and vorto[-2] in vokaloj:
        vorto = vorto[:-1]
    return vorto

with open(dosiernomo, encoding="utf-8") as d:
    teksto = d.read()
    alineoj = teksto.split("\n")
    n = 0
    for alineo in alineoj:
        n += 1
        nomoj = re.findall(r"(?<=[A-ZĈĜĤĴŜŬa-zĉĝĥĵŝŭáéíóú'-,] )([A-ZĈĜĤĴŜŬ][a-zĉĝĥĵŝŭáéíóú']+(?:-[A-ZĈĜĤĴŜŬ][a-zĉĝĥĵŝŭáéíóú']+)?)", alineo)
        if len(nomoj) > 0:
            print(str(n) + ": ")
            for nomo in nomoj:
                nomo = normaligi(nomo)
                print("- " + nomo)
                if nomo not in plena_nomaro:
                    plena_nomaro.append(nomo)

print(plena_nomaro)

with open("nomaro.txt", encoding="utf-8", mode="w") as d:
    for nomo in plena_nomaro:
        d.write(nomo + "\n")