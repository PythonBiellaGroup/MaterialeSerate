import datetime
from dataclasses import dataclass
from typing import List, Optional

ordine_json = {
    'elemento_id': '123',
    'data_creazione': '2002-11-24 12:22',
    'pagine_visitate': [1, 2, '3'],
    'prezzo': 17.22
}

# https://docs.python.org/3/library/dataclasses.html#module-dataclasses
# This module provides a decorator and functions for automatically adding generated special methods 
# such as __init__() and __repr__() to user-defined classes.
@dataclass
class Ordine:
    elemento_id: int
    data_creazione: Optional[datetime.datetime]
    pagine_visitate: List[int]
    prezzo: float

    def __post_init__(self):
        # Inserire tutti i controlli qui
        pass


def main() -> None:
    # o = Ordine(elemento_id=ordine_json.get('elemento_id'), ...)
    o = Ordine(**ordine_json)
    print(o)


if __name__ == "__main__":
    main()