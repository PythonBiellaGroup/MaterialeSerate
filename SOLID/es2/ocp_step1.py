"""
Open-Closed Principle
"""


class Animal:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        pass


def animal_sound(animals: list) -> None:
    for animal in animals:
        if animal.name == 'lion':
            print('roar')

        elif animal.name == 'mouse':
            print('squeak')


animals = [
    Animal('lion'),
    Animal('mouse')
]
animal_sound(animals)

"""
La funzione animal_sound() non è conforme al principio OCP perché
non è chiusa contro l'aggiunta di nuovi tipi di animali.
Se aggiungiamo un nuovo animale, Snake ad esempio, dobbiamo modificarla.
"""
