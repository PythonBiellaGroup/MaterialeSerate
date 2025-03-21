# Gestisce ordini in un pasto, calcola costo totale e costo massimo
from collections import namedtuple
from typing import Optional, Iterable

# https://docs.python.org/3/library/collections.html#collections.namedtuple
Ordine = namedtuple("Ordine", "voce, prezzo")

costo_massimo: Optional[int] = None


def calcola_costo(ordini: Iterable[Ordine]) -> int:
    global costo_massimo
    total = 0

    for o in ordini:
        total += o.prezzo

    if not costo_massimo or total > costo_massimo:
        costo_massimo = total

    return total


def main() -> None:
    print("Inseriamo i pasti consumati nel giorno")

    cena = [Ordine('Pizza', 20), Ordine('Birra', 9), Ordine('Birra', 9)]
    colazione = [Ordine('Pancakes', 11), Ordine('Bacon', 4), Ordine('Caffè', 3), Ordine('Caffè', 3), Ordine('Brioche', 2)]

    totale_cena = calcola_costo(cena)
    print(f"Costo cena EUR {totale_cena:,.02f}")

    totale_colazione = calcola_costo(colazione)
    print(f"Costo colazione EUR {totale_colazione:,.02f}")

    print(f"Oggi il costo più elevato è stato EUR {costo_massimo:.02f}")


if __name__ == '__main__':
    main()