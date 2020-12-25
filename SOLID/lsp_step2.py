
"""
The animal_leg_count function cares less the type of Animal passed, it just
calls the leg_count method.  All it knows is that the parameter must be of an
Animal type, either the Animal class or its sub-class.

The Animal class now have to implement/define a leg_count method.  And its
sub-classes have to implement the leg_count method:
"""


class Animal:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        pass

    def make_sound(self) -> str:
        pass

    def leg_count(self) -> int:
        pass

    @staticmethod
    def animal_leg_count(animals: list) -> None:
        for animal in animals:
            print(animal.leg_count())


class Lion(Animal):
    def make_sound(self) -> str:
        return 'roar'

    def leg_count(self) -> int:
        return 4


class Mouse(Animal):
    def make_sound(self) -> str:
        return 'squeak'

    def leg_count(self) -> int:
        return 4


class Snake(Animal):
    def make_sound(self) -> str:
        return 'hiss'

    def leg_count(self) -> int:
        return 0


animals = [
    Lion('lion'),
    Mouse('mouse'),
    Snake('snake')
]
Animal.animal_leg_count(animals)

"""
Quando un leone viene passato alla funzione animal_leg_count,
restituisce il numero di gambe che ha un leone.

Vedi, animal_leg_count non ha bisogno di conoscere il tipo di animale per
restituire il suo conteggio delle gambe; chiama semplicemente il metodo
leg_count() del tipo Animal perché "per contratto" una sottoclasse
della classe Animal deve implementare la funzione leg_count.
"""
