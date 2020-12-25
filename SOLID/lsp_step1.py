"""
Liskov Substitution Principle
"""


class Animal:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        pass

    def make_sound(self):
        pass

    @staticmethod
    def animal_leg_count(animals: list):
        for animal in animals:
            if isinstance(animal, Lion):
                print(animal.lion_leg_count())
            elif isinstance(animal, Mouse):
                print(animal.mouse_leg_count())
            elif isinstance(animal, Snake):
                print(animal.snake_leg_count())


class Lion(Animal):
    def make_sound(self):
        return 'roar'

    def lion_leg_count(self):
        return 4


class Mouse(Animal):
    def make_sound(self):
        return 'squeak'

    def mouse_leg_count(self):
        return 4


class Snake(Animal):
    def make_sound(self):
        return 'hiss'

    def snake_leg_count(self):
        return 0


animals = [
    Lion('lion'),
    Mouse('mouse'),
    Snake('snake')
]
Animal.animal_leg_count(animals)


"""
Per fare in modo che questa funzione segua il principio LSP, seguiremo questo
postulato LSP di Steve Fenton:

Se la superclasse (Animal) ha un metodo che accetta un parametro di tipo
superclasse (Animale), ogni sua sua sottoclasse (Snake) dovrebbe accettare
come argomento un tipo superclasse (tipo animale) o tipo sottoclasse.
Se la superclasse restituisce un tipo superclasse (Animale), la sua
sottoclasse dovrebbe restituire un tipo di superclasse (tipo animale)
o tipo di sottoclasse (Snake).

Proviamo a reimplementare la funzione animal_leg_count.
"""
