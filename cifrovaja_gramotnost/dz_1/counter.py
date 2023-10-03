import math
import re

def normaligi(linio: str):
    '''Forigas la sanktavalajn dialektaĵojn kaj la superfluajn apostrofojn / Убирает диалектные черты Санктавало и излишние апострофы'''
    rezulto = linio
    # Korekto de la sanktavala skribmaniero / Исправление санктавальского стиля записи
    rezulto = re.sub(r"á(\w+)\b", r"a\1o", rezulto)
    rezulto = re.sub(r"í(\w+)\b", r"i\1o", rezulto)
    rezulto = re.sub(r"ú(\w+)\b", r"u\1o", rezulto)
    rezulto = re.sub(r"é(\w+)\b", r"e\1o", rezulto)
    rezulto = re.sub(r"ó(\w+)\b", r"o\1o", rezulto)
    # Senapostrofigo / Избавление от апострофов
    rezulto = re.sub(r"\bl'", r"la ", rezulto)
    rezulto = re.sub(r"\bdank'al", r"danke al", rezulto)
    rezulto = re.sub(r"'st(i|as|is|os|us|u)\b", r"est\1", rezulto)
    rezulto = re.sub(r"\b(\w+)'", r"\1o ", rezulto)
    return rezulto

def longigi(linio: str):
    '''Relongigas la mallongigojn s-ro/s-ino, f-ino k d-ro / Восстанавливает сокращения s-ro/s-into, f-ino и d-ro'''
    rezulto = linio
    rezulto = re.sub(r"\bd-ro", r"doktoro", rezulto)
    rezulto = re.sub(r"\bs-ro", r"sinjoro", rezulto)
    rezulto = re.sub(r"\bs-ino", r"sinjorino", rezulto)
    rezulto = re.sub(r"\bf-ino", r"fraŭlino", rezulto)
    return rezulto

def vortaraFormo(vorto: str):
    '''Rezultigas la vortaran formon de minuskla vorto / Возвращает словарную форму слова в нижнем регистре'''
    rezulto = vorto
    rezulto = re.sub(r'\b([mncvlŝĝs]i|ili|oni)n\b', r'\1', rezulto)
    # Forigo de markiloj de akuzativo ĉe personaj pronomoj
    # Убираем показатели винительного падежа у личных местоимений
    if len(re.findall(r'[aiueo]', rezulto)) >= 2:
        rezulto = re.sub(r'((?<!\btam)e|[oau])j?n?\b', r'\1', rezulto)
        # Forigo de markiloj de pluralo kaj akuzativo ĉe substantivoj, adjektivoj, adverboj kaj kelkaj korelativoj
        # Убираем показатели множественного числа и винительного падежа у имён, наречий и некоторых местоимений
        rezulto = re.sub(r'(?<!\bki)(?<!\bti)(?<!\bi)(?<!\bĉi)(?<!\bneni)(?<!\bun)(as|is|os|us|u)\b', r'i', rezulto)
        # Forigo de markiloj de tenso kaj modo ĉe verboj (= formado de la infinitivo)
        # Убираем показатели времени и наклонения у глаголов (= формируем инфинитив)
    return rezulto

fVortetoj = open("D:/Universitato/Korpusoj/vortetoj.txt", encoding="utf-8")
vortetoj = fVortetoj.readlines() # Listo de ignorindaj vortetoj / Список стоп-слов
fVortetoj.close()

fTeksto = open("D:/Universitato/Korpusoj/cxu_vi_kuiras_cxine.txt", encoding="utf-8")
alineoj = fTeksto.readlines() # Listo de la alineoj / Список абзацев
fTeksto.close()

vortaro = {} # La vortoj en la tekstodosiero / Словарь слов из текстового файла

k = 0
for alineo in alineoj:
    alineo = longigi(normaligi(alineo.lower()))
    k += 1
    vortoj = re.split(r'[^\w-]+', alineo) # дефисы соединяют части слова в эсперанто
    for v in vortoj:
        v = vortaraFormo(v)
        if f"{v}\n" in vortetoj or v == "":
            continue
        if v in vortaro:
            vortaro[v] += 1
        else:
            vortaro[v] = 1

vortaro = sorted(vortaro.items(), key=lambda x: x[1], reverse=True) # Ordigo / Сортировка
k = 0
for lemo in vortaro:
    k += 1
    print(f'{" "*(3-math.floor(math.log10(k)))}{k}. "{lemo[0]}" renkontiĝas {lemo[1]} fojo{"j" if lemo[1]>1 else ""}n | встречается {lemo[1]} раз{"a" if lemo[1] % 10 > 1 and lemo[1] % 10 < 5 and lemo[1] % 100 // 10 != 1 else ""}')