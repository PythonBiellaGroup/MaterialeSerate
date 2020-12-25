"""
Per ogni nuovo Animal, viene aggiunta una nuova logica alla funzione.
Questo è un semplice esempio ma il problema è frequente.
"""


class Animal:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        pass


def animal_sound(animals: list):
    for animal in animals:
        if animal.name == 'lion':
            print('roar')
        elif animal.name == 'mouse':
            print('squeak')
        elif animal.name == 'snake':
            print('hiss')


animals = [
    Animal('lion'),
    Animal('mouse'),
    Animal('snake')
]
animal_sound(animals)


"""
Come rendere animal_sound() conforme a OCP?
"""
