"""
La classe degli animali sarà la punto ingresso/facciata (Facade) per la
gestione del database degli animali e gestione delle proprietà degli animali.
"""


class Animal:
    def __init__(self, name: str):
        self.name = name
        self.db = AnimalDB()

    def get_name(self):
        return self.name

    def get(self, id):
        return self.db.get_animal(id)

    def save(self):
        self.db.save(animal=self)


class AnimalDB:
    def get_animal(self, id) -> Animal:
        pass

    def save(self, animal: Animal):
        pass


"""
I metodi più importanti stanno nella classe Animal, usata come
"facciata" per le funzioni minori.
"""
