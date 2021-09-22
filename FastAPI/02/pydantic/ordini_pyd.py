import datetime
from typing import List, Optional

from pydantic import BaseModel

ordine_json = {
    'elemento_id': '123',
    'data_creazione': '2002-11-24 12:22',
    'pagine_visitate': [1, 2, '3'],
    'prezzo': 17.22
}


class Ordine(BaseModel):
    elemento_id: int
    data_creazione: Optional[datetime.datetime]
    pagine_visitate: List[int] = []
    prezzo: float


def main() -> None:
    # o = Ordine(elemento_id=ordine_json.get('elemento_id'), ...)
    o = Ordine(**ordine_json)
    print(o)


if __name__ == "__main__":
    main()