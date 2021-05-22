class Animal:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        pass


class AnimalDB:
    def get_animal(self, id) -> Animal:
        pass

    def save(self, animal: Animal):
        pass


"""
Quando progettiamo le nostre classi, dovremmo mettere insieme le funzionalità
correlate, quindi ogni volta che tendono a cambiare cambiano per lo stesso
motivo. E dovremmo separare le funzionalità se cambieranno per motivi diversi.

Lo svantaggio di questa soluzione è che i client di questo codice devono
gestire due classi.
Una soluzione comune a questo probelma è applicare la il Facade pattern.
"""
