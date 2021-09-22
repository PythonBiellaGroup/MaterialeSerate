# Gestisce ordini in un pasto, calcola costo totale e costo massimo
from collections import namedtuple

# https://docs.python.org/3/library/collections.html#collections.namedtuple
Ordine = namedtuple("Ordine", "voce, prezzo")

costo_massimo = None


def calcola_costo(ordini):
    global costo_massimo
    total = 0

    for o in ordini:
        total += o.prezzo
        # Editor non mi aiuta nel capire che "prezzi" non esiste
        # total += o.prezzi

    # Di che tipo è costo_massimo?
    if not costo_massimo or total > costo_massimo:
        costo_massimo = total

    return total


def main():
    print("Inseriamo i pasti consumati nel giorno")

    cena = [Ordine('Pizza', 20), Ordine('Birra', 9), Ordine('Birra', 9)]
    colazione = [Ordine('Pancakes', 11), Ordine('Bacon', 4),
                 Ordine('Caffè', 3), Ordine('Caffè', 3), Ordine('Brioche', 2)]

    totale_cena = calcola_costo(cena)
    print(f"Costo cena EUR {totale_cena:,.02f}")

    totale_colazione = calcola_costo(colazione)
    print(f"Costo colazione EUR {totale_colazione:,.02f}")

    print(f"Oggi il costo più elevato è stato EUR {costo_massimo:.02f}")


if __name__ == '__main__':
    main()
