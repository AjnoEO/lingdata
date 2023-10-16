import re
import random
import csv
from copy import deepcopy
from itertools import permutations

def opciaj_demandoj(nomo: str):
    tipo = tipo_el_nomo(nomo)
    rezulto = []
    for obj in listaro[tipo+"j"]:
        if obj[tipo] == nomo:
            break
    else:
        print("Eraro!")
        return None
    if tipo == "Dialekto":
        return [opcia_demando(obj, tipo, cela_tipo="Lingvo")]
    if obj["Familio"] == None and obj["Makrofamilio"] == None:
        for t in ["Familio", "Branĉo", "Grupo"]:
            rezulto.append(deepcopy(opcia_demando(obj, tipo, t)))
        return rezulto
    for t in obj:
        if t == "Loko":
            continue
        if obj[t] != None and t != tipo:
            rezulto.append(deepcopy(opcia_demando(obj, tipo, t)))
        if obj[t] != None and t == tipo:
            break
    return rezulto

def entajpaj_demandoj(obj: dict):
    nomo, tipo = nomo_k_tipo_el_objekto(obj)
    negrava_praulo = nomo.startswith("*")
    nomo = normaligi(nomo, (tipo != "Familio"))
    respondo = ""
    entajpendajxo = "r:^("
    for t in tipoj:
        if obj[t] == None:
            continue
        if t == tipo:
            continue
        ara_nomo = obj[t]
        if respondo != "":
            respondo += "<br>"
        respondo += normaligi(ara_nomo, True)
        if negrava_praulo:
            entajpendajxo += '(' + varianta_regespo(ara_nomo) + ')?'
        else:
            if respondo == "Афразийская макросемья":
                entajpendajxo += "^"
            entajpendajxo += varianta_regespo(ara_nomo)
        negrava_praulo = ara_nomo.startswith("*")
    entajpendajxo += ")$"
    if respondo == "" and tipo == "Lingvo":
        respondo = "Язык-изолят"
        entajpendajxo = "r:^((ЯЗЫК)?ИЗОЛЯТ|РОДСТВОНЕУСТАНОВЛЕНО|НЕУСТАНОВЛЕНН?ОЕ?РОДСТВО|НЕТ)"
    if respondo == "" and tipo == "Familio":
        respondo = "Нет"
        entajpendajxo = "r:^(НЕАФРАЗИЙСКАЯ(МАКРОСЕМЬЯ)?|НЕТ|БЕЗМАКРОСЕМЬИ|НЕОТНОСИТСЯ)"
    if respondo == "Афразийская макросемья" and tipo == "Familio":
        respondo = "Да"
        entajpendajxo = "r:^(АФРАЗИЙСКАЯ(МАКРОСЕМЬЯ)?|ДА|ОТНОСИТСЯ)"
    if respondo == "":
        return []
    return [{
        "Demando": nomo if tipo != "Familio" else f"Относится ли {nomo} к афразийской макросемье?",
        "Respondo": respondo,
        "Entajpendajxo": entajpendajxo
    }]

def lokaj_demandoj(obj: dict):
    if obj["Loko"] == None:
        return []
    nomo, tipo = nomo_k_tipo_el_objekto(obj)
    nomo = normaligi(nomo, True)
    respondo = ""
    loko = obj["Loko"]
    respondo = re.sub(r'\((север|юг|запад|восток|=.+?)\)', '', loko)
    respondo = re.sub(r'\s+(?=[^А-Яа-я(])', '', respondo)
    if ';' in respondo:
        respondoj = [("{" + r + "}") for r in respondo.split('; ')]
        respondo = ', '.join(respondoj)
        entajpendajxoj = [f"({entajpendajxo_el_loko(l)})" for l in loko.split('; ')]
        cxiuj_ordoj = list(permutations(entajpendajxoj))
        cxiuj_ordoj = ['+'.join(ordo) + '+' for ordo in cxiuj_ordoj]
        entajpendajxo = '|'.join(cxiuj_ordoj)
    else:
        entajpendajxo = entajpendajxo_el_loko(loko)
    entajpendajxo = "r:^(" + entajpendajxo + ")+$"
    return [{
        "Demando": nomo,
        "Respondo": respondo,
        "Entajpendajxo": entajpendajxo
    }]

def varianta_regespo(nomo: str):
    tipo = tipo_el_nomo(nomo)
    if nomo.startswith("*"):
        nomo = nomo[1:]
    rezulto = nomo.upper()
    rezulto = re.sub(r"\sА\s", r"\[АA\]", rezulto)
    rezulto = re.sub(r"\sБ\s", r"\[БB\]", rezulto)
    rezulto = re.sub(r"^(.+?)\((.{2,}?)\)", r"\(\1|\2\)", rezulto)
    if tipo == "Lingvo":
        rezulto = re.sub(r"ИЙ(?![А-Я])", "(ИЙ|ОГО)", rezulto)
        rezulto = re.sub(r"ЯЗЫК", "(ЯЗЫКА?)?", rezulto)
    if tipo == "Subgrupo":
        rezulto = re.sub(r"ИЕ(?![А-Я])", "(ИЕ|ИХ|АЯ|ОЙ)", rezulto)
        rezulto = re.sub(r"ЯЗЫКИ", "(ЯЗЫК(И|ОВ)|(ПОД)?ГРУПП[АЫ])", rezulto)
    if tipo == "Grupo" or tipo == "Branĉo":
        rezulto = re.sub(r"АЯ(?![А-Я])", "(ИЕ|ИХ|АЯ|ОЙ)", rezulto)
        rezulto = re.sub(r"ВЕТВЬ|ГРУППА", "(ЯЗЫК(И|ОВ)|ВЕТВ[ЬИ]|ГРУПП[АЫ])", rezulto)
    if tipo == "Familio":
        rezulto = re.sub(r"АЯ(?![А-Я])", "(ИЕ|ИХ|АЯ|ОЙ)", rezulto)
        rezulto = re.sub(r"СЕМЬЯ", "((ЯЗЫКОВ(АЯ|ОЙ))?СЕМЬ[ЯИ](ЯЗЫКОВ)?|ЯЗЫК(И|ОВ))", rezulto)
    if tipo == "Makrofamilio":
        rezulto = re.sub(r"АЯ(?![А-Я])", "(АЯ|ОЙ)", rezulto)
        rezulto = re.sub(r"МАКРОСЕМЬЯ", "(МАКРОСЕМЬ[ЯИ])?", rezulto)
    rezulto = re.sub(r"[^А-Яа-я()|?\[\]]", "", rezulto)
    rezulto = re.sub(r"\(\)", "", rezulto)
    return rezulto

def demando_pri_la_makrofamilio(nomo: str, tipo: str):
    opcioj = [nomo.capitalize()]
    while len(opcioj) < maksimuma_opciaro:
        hazarda_numero = random.randrange(ekster_la_makrofamilio[tipo+"j"])
        hazarda_parolajxo = listaro[tipo+"j"][hazarda_numero][tipo]
        hazarda_parolajxo = normaligi(hazarda_parolajxo, True)
        if hazarda_parolajxo not in opcioj:
            opcioj.append(hazarda_parolajxo)
    return {
        "Demando": 
            "Какой из нижеперечисленных языков относится к афразийской макросемье?" if tipo == "Lingvo" else
            "Какая из нижеперечисленных языковых семей относится к афразийской макросемье?",
        "Opcioj": opcioj
    }

def vortigo_de_demando(nomo: str, tipo: str, cela_tipo: str):
    nombro_de_parolajxo = "p" if (normaligi(purigi(nomo, 1)).endswith("языки") or " и " in nomo) else "s"
    if cela_tipo == "Lingvo":
        frazo = f"В каком языке выделяют {nomo}?"
    if cela_tipo == "Subgrupo":
        frazo = f"К какой подгруппе языков относ{'ит' if nombro_de_parolajxo=='s' else 'ят'}ся {nomo}?"
    if cela_tipo == "Grupo":
        frazo = f"К какой группе языков относ{'ит' if nombro_de_parolajxo=='s' else 'ят'}ся {nomo}?"
    if cela_tipo == "Branĉo":
        frazo = f"К какой ветви относ{'ит' if nombro_de_parolajxo=='s' else 'ят'}ся {nomo}?"
    if cela_tipo == "Familio":
        frazo = f"К какой языковой семье относ{'ит' if nombro_de_parolajxo=='s' else 'ят'}ся {nomo}?"
    return frazo

def entajpendajxo_el_loko(loko: str):
    rezulto = loko.replace(', ', '|').replace(' и ', '|').lower()
    #rezulto = re.sub(r'([^|]+)', r'(\1)', rezulto)
    rezulto = rezulto.replace('|др.', '')
    rezulto = re.sub(r'([^,|]+)\((север|юг|запад|восток)\)', genitivo_regespo, rezulto)
    rezulto = re.sub(r'(север|юг|запад|восток) ([^,]+?)\(=(.+?)\)', r'\1 \2(=\1 \3)', rezulto)
    rezulto = re.sub(r'\(=?(.+?)\)', r'|\1', rezulto)
    rezulto = rezulto.replace('республика', '(республика)?')
    rezulto = rezulto.replace('ские острова', '(ские острова|ы)')
    rezulto = re.sub('(?<!ские)остров', '(остров)?', rezulto)
    rezulto = re.sub(r'(север|юг)о-(запад|восток)', r'((\1о)?\2|\1)', rezulto)
    rezulto = re.sub(r'([б-джзк-нп-тф-щ])\1', r'\1+', rezulto)
    rezulto = rezulto.replace('ё', '[её]')
    rezulto = re.sub(r'[^а-яё|()\[\]?+]', r'', rezulto)
    return rezulto.upper()

def genitivo_regespo(trovo):
    loknomo = trovo.group(1)
    flanko = trovo.group(2)
    return loknomo + '|' + flanko + genitivo(loknomo)

def genitivo(linio: str):
    vortoj = re.findall(r"[А-Яа-я-]+", linio)
    for v in vortoj:
        vg = re.sub(r'ый$', 'ого', v)
        vg = re.sub(r'кий$', 'кого', vg)
        vg = re.sub(r'ий$', 'его', vg)
        vg = re.sub(r'я$', 'и', vg)
        vg = re.sub(r'(?<=[шжчщ])а$', 'и', vg)
        vg = re.sub(r'а$', 'ы', vg)
        vg = re.sub(r'([б-джзк-нп-тф-щ])$', r'\1а', vg)
        linio = linio.replace(v, vg)
    return linio
        
def opcia_demando(objekto: dict, tipo: str, cela_tipo: str):
    nomo = objekto[tipo]
    if (cela_tipo == "Makrofamilio"):
        return demando_pri_la_makrofamilio(nomo, tipo)
    else:
        if tipo == "Lingvo" and cela_tipo in ["Familio", "Branĉo", "Grupo"]:
            if objekto[cela_tipo] == None:
                opcioj = ["Ни к какой, это язык-изолят"]
            else:
                opcioj = [normaligi(objekto[cela_tipo], True)]
                if random.randint(0, (len(listaro["Lingvoj"])-1)//10) == 0:
                    opcioj.append("Ни к какой, это язык-изолят")
        else:
            opcioj = [normaligi(objekto[cela_tipo], True)]
        if re.match(r"(Западно|Южно|Северо|Восточно)", opcioj[0]):
            for pref in ["Западно", "Восточно", "Южно", "Северо"]:
                hazarda_parolajxo = re.sub(r"(Западно|Южно|Северо|Восточно)", pref, purigi(opcioj[0], 1).capitalize())
                if hazarda_parolajxo == "Северогерманская группа":
                    hazarda_parolajxo = "Северогерманская (скандинавская) группа"
                if hazarda_parolajxo not in opcioj and len(opcioj) < maksimuma_opciaro:
                    opcioj.append(hazarda_parolajxo)
        bazo = re.findall(r'(?<!\()\b([А-Яа-я]+[цс]к)(?:о|ий|ая)\b', nomo)
        if objekto["Familio"] != None and len(bazo) != 0:
            baza_radiko = str(bazo[-1])
            if cela_tipo != "Familio" or random.randint(0,1):
                hazarda_parolajxo = re.sub(r'.+\s', baza_radiko.capitalize() + f"{'ий' if cela_tipo == 'Lingvo' else 'ие' if cela_tipo == 'Subgrupo' else 'ая'} ", opcioj[0])
            else:
                hazarda_familio = random.choice(listaro["Familioj"])["Familio"]
                hazarda_parolajxo = re.sub(r'.+\s', baza_radiko.capitalize() + "о-" + hazarda_familio.split("-")[-1].lower(), opcioj[0])
            if hazarda_parolajxo not in opcioj and len(opcioj) < maksimuma_opciaro and (len(bazo) > 1 or random.randint(0, (len(listaro[cela_tipo+"j"])-1)//3) == 0):
                opcioj.append(hazarda_parolajxo)
        while len(opcioj) < maksimuma_opciaro:
            hazarda_parolajxo = random.choice(listaro[cela_tipo+"j"])
            hazarda_parolajxo = hazarda_parolajxo[cela_tipo]
            hazarda_parolajxo = normaligi(hazarda_parolajxo, True)
            if hazarda_parolajxo not in opcioj:
                opcioj.append(hazarda_parolajxo)
                if re.match(r"(Западно|Южно|Северо|Восточно)", hazarda_parolajxo):
                    for pref in ["Западно", "Восточно", "Южно", "Северо"]:
                        nova_hazarda_parolajxo = re.sub(r"(Западно|Южно|Северо|Восточно)", pref, purigi(hazarda_parolajxo, 1).capitalize())
                        if nova_hazarda_parolajxo == "Северогерманская группа":
                            nova_hazarda_parolajxo = "Северогерманская (скандинавская) группа"
                        if len(opcioj) < maksimuma_opciaro and nova_hazarda_parolajxo not in opcioj:
                            opcioj.append(nova_hazarda_parolajxo)
        return {
        "Demando": vortigo_de_demando(nomo, tipo, cela_tipo),
        "Opcioj": opcioj
    }

def normaligi(nomo: str, ekmajusklo: bool = False):
    if nomo.startswith("*"):
        nomo = nomo[1:]
    if ekmajusklo:
        nomo = nomo.capitalize()
    if nomo.startswith("Тохарский") or nomo.startswith("тохарский"):
        nomo = nomo.replace(" а ", " А ").replace(" б ", " Б ")
    return nomo

def purigi(nomo: str, forto: int = 0):
    if forto == 0: 
        return re.sub(r'(\[.+?\]|\n)', r'', nomo).strip().lower()
    else:
        return " ".join(re.sub(r'(\[.+?\]|\(.+?\)|\n)', r'', nomo).split()).lower()

def tipo_el_nomo(nomo: str):
    nomo = purigi(nomo, 1)
    if nomo.endswith('макросемья'):
        return "Makrofamilio"
    elif nomo.endswith('семья'):
        return "Familio"
    elif nomo.endswith('ветвь'):
        return "Branĉo"
    elif nomo.endswith('группа'):
        return "Grupo"
    elif (nomo.endswith('е языки') or nomo.endswith('подгруппа')) and nomo != "ретороманские языки":
        return "Subgrupo"
    elif nomo.endswith('диалект'):
        return "Dialekto"
    else:
        return "Lingvo"

def nomo_k_tipo_el_objekto(obj: dict):
    for t in tipoj:
        if obj[t] == None:
            continue
        tipo = t
        nomo = obj[tipo]
        break
    return (nomo, tipo)

def eligi_demandon(dem):
    print(f"[?] {dem['Demando']}")
    if 'Opcioj' in dem:
        for i in range(len(dem['Opcioj'])):
            print(f"    [{'v' if i == 0 else 'x'}] {dem['Opcioj'][i]}")
    else:
        print(f"    [La ĝusta respondo] {dem['Respondo']}")
        print(f"    [Entajpa esprimo] {dem['Entajpendajxo']}")

def strukturigo(parolajxoj: list, loko: str = None):
    rezulto = {t: None for t in reversed(tipoj)}
    for nomo in parolajxoj:
        tipo = tipo_el_nomo(nomo)
        rezulto[tipo] = nomo
    rezulto["Loko"] = loko
    return rezulto

tipoj = ["Dialekto", "Lingvo", "Subgrupo", "Grupo", "Branĉo", "Familio", "Makrofamilio"]

nunaj_parolajxoj = []
listaro = {t+"j": [] for t in reversed(tipoj)}
listaro["Lokhavaj"] = []
ekster_la_makrofamilio = {t+"j": 0 for t in tipoj if t != "Makrofamilio"}

maksimuma_opciaro = 5

with open('genealogio.tsv', encoding='utf-8') as d:
    for linio in d:
        trovo = re.search(r'\S', linio)
        if trovo is None:
            continue
        nunaj_parolajxoj = nunaj_parolajxoj[:trovo.start()]
        loko = re.findall(r'(?<=\[).+?(?=\])', linio)
        if loko != []:
            loko = loko[0]
        else:
            loko = None
        nomo = purigi(linio)
        tipo = tipo_el_nomo(nomo)
        nunaj_parolajxoj.append(nomo)
        objekto = strukturigo(nunaj_parolajxoj, loko)
        listaro[tipo+"j"].append(deepcopy(objekto))
        if loko != None:
            listaro["Lokhavaj"].append(deepcopy(objekto))
        if nunaj_parolajxoj[0] != "афразийская макросемья": ekster_la_makrofamilio[tipo+"j"] += 1

demandaro = []
for t in tipoj:
    for p in listaro[t+"j"]:
        dem = opciaj_demandoj(p[t])
        if len(dem) == 0 and not t.lower().endswith("familio"):
            print(f"Eraro dum kreado de opciaj demandoj! {t}: {p[t]}")
        demandaro += dem
with open("demandaro.tsv", encoding='utf-8', mode="w", newline='') as tsv_dosiero:
    writer = csv.writer(tsv_dosiero, delimiter='\t', lineterminator='\n')
    writer.writerow(["QUESTION", "CORRECT"] + ["CHOICE"] * maksimuma_opciaro)
    for dem in demandaro:
        writer.writerow([dem["Demando"], 1] + dem["Opcioj"])
#for i in range(5):
    #eligi_demandon(random.choice(demandaro))

demandaro = []
for t in tipoj:
    for p in listaro[t+"j"]:
        dem = entajpaj_demandoj(p)
        if len(dem) == 0 and not t == "Makrofamilio":
            print(f"Eraro dum kreado de entajpaj demandoj! {t}: {p[t]}")
        demandaro = demandaro + dem
with open("demandaro_entajpa.tsv", encoding='utf-8', mode="w", newline='') as tsv_dosiero:
    writer = csv.writer(tsv_dosiero, delimiter='\t', lineterminator='\n')
    writer.writerow(["HINT", "ANSWER", "ISNAME", "TYPEIN"])
    writer.writerow(["Вопрос", "Генеалогическая принадлежность", "", ""])
    for dem in demandaro:
        writer.writerow([dem["Demando"], dem["Respondo"], "N", dem["Entajpendajxo"]])
#for i in range(5):
    #eligi_demandon(random.choice(demandaro))

demandaro = []
for p in listaro["Lokhavaj"]:
    dem = lokaj_demandoj(p)
    if len(dem) == 0:
        print(f"Eraro dum kreado de lokaj demandoj! {t}: {p[t]}")
    demandaro = demandaro + dem
with open("demandaro_loka.tsv", encoding='utf-8', mode="w", newline='') as tsv_dosiero:
    writer = csv.writer(tsv_dosiero, delimiter='\t', lineterminator='\n')
    writer.writerow(["HINT", "ANSWER", "ISNAME", "TYPEIN"])
    writer.writerow(["Вопрос", "Ареал распространения", "", ""])
    for dem in demandaro:
        writer.writerow([dem["Demando"], dem["Respondo"], "N", dem["Entajpendajxo"]])
for i in range(5):
    eligi_demandon(random.choice(demandaro))
print(len(demandaro))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
