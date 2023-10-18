import re

book_count = 7
max_words_in_spell = 4
spells = [ [] for _ in range(max_words_in_spell)]

with open("Spells.txt") as f:
    spells_all = f.readlines()
    for s in spells_all:
        number_of_spaces = len(s.split()) - 1
        spells[number_of_spaces].append(s.replace("\n", "").lower())

text = ""
for book in range(1, book_count + 1):
    print(f"Processing book {book}/{book_count}...")
    with open(f"raw/JKR_HP{book}_raw.txt", encoding="utf-8") as f:
        text = f.read()
        if (book <= 3):
            text = re.sub(r"\n\t?(?!\s)", "", text)
        text = re.sub(r"[^A-Za-z0-9\s]", "", text)
        text = text.upper()
        for number_of_spaces in range(max_words_in_spell-1, -1, -1):
            for spell in spells[number_of_spaces]:
                text = re.sub(r"\b" + re.escape(spell.upper()) + r"\b", spell.replace(" ", ""), text)
        text = re.sub(r"[A-Z0-9]+", "*", text)
    with open(f"results/JKR_HP{book}.txt", "w") as f:
        f.write(text)