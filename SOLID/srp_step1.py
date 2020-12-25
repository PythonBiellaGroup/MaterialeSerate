"""
Single Responsibility Principle
"""


class Animal:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        pass

    def save_on_db(self, db_uri: str):
        pass


"""
La classe Animal viola l'SRP.

SRP afferma che le classi dovrebbero avere una responsabilità, qui, possiamo
vedere due responsabilità:
- gestione del database degli animali
- gestione proprietà degli animali

Il costruttore e get_name gestiscono le proprietà Animal mentre il
save gestisce l'archiviazione degli animali su un database.

In che modo questo design causerà problemi in futuro?

Se l'applicazione cambia nella gestione del database, le classi che fanno
uso delle proprietà Animal dovranno essere toccate.

Questo sistema puzza di rigidità, è come un effetto domino: toccare una
carta influenza tutte le altre carte in linea.

Per renderlo conforme a SRP, creiamo un'altra classe che gestirà la sola
responsabilità di memorizzare un animale in un database.
"""
