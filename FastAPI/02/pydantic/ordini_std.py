import datetime
from typing import List

# Si noti il terzo elemento tra le pagine visitate
ordine_json = {
    'elemento_id': '123',
    'data_creazione': '2002-11-24 12:22',
    'pagine_visitate': [1, 2, '3'],
    'prezzo': 17.22
}

# Versione semplificata... ma...
class Ordine:

    def __init__(self, elemento_id: int, data_creazione: datetime.datetime,
                 pagine_visitate: List[int], prezzo: float):
        self.elemento_id = elemento_id
        self.data_creazione = data_creazione
        self.pagine_visitate = pagine_visitate
        self.prezzo = prezzo

    def __str__(self):
        return str(self.__dict__)

# .. qualcosa non va nei tipi rispetto alle nostre attese


def main() -> None:
    # o = Ordine(elemento_id=ordine_json.get('elemento_id'), ...)
    o = Ordine(**ordine_json)
    print(o)


if __name__ == "__main__":
    main()
