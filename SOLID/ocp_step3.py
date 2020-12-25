class Animal:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        pass

    def make_sound(self):
        raise NotImplementedError


class Lion(Animal):
    def make_sound(self):
        return 'roar'


class Mouse(Animal):
    def make_sound(self):
        return 'squeak'


class Snake(Animal):
    def make_sound(self):
        return 'hiss'


def animal_sound(animals: list):
    for animal in animals:
        print(animal.make_sound())


animals = [
    Lion('lion'),
    Mouse('mouse'),
    Snake('snake')
]
animal_sound(animals)

"""
Animal ora ha un metodo virtuale make_sound().
Ogni animale estende la classe Aanimal e implementa il metodo virtuale.
Ogni animale aggiunge la propria implementazione su come emette un suono.
La funzione animal_sound() itera attraverso la lista di animali e
semplicemente chiama il suo metodo make_sound().

Ora, se aggiungiamo un nuovo animale, animal_sound() non deve cambiare.
Tutto ciò di cui abbiamo bisogno sarà aggiungere il nuovo animale
all'array degli animali.

animal_sound() ora è conforme al principio OCP.
"""
