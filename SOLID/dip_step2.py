from abc import *
 
class EventStreamer():
    def __init__(self, parsed_data: str, client):
        self.parsed_data = parsed_data
        assert client in DataTargetClient.__subclasses__(), "Client is not DataTargetClient"
        self.client = client
        
    def stream(self):
        self.client.send(self.parsed_data)
 
class DataTargetClient(metaclass=ABCMeta):
    """Interface: DataTargetClient class"""
    @abstractmethod
    def send(data: str):
        pass            
        
class Syslog(DataTargetClient):
    @staticmethod
    def send(data: str):
        print(f"Syslog send: {data}")
        pass
    
class OtherClient(DataTargetClient):
    @staticmethod
    def send(data: str):
        print(f"OtherClient send: {data}")
        pass
 
 
streamer1 = EventStreamer("for Syslog data!", Syslog)
streamer1.stream()
streamer2 = EventStreamer("for OtherClient data!", OtherClient)
streamer2.stream()

"""
La soluzione a questi problemi è far interagire EventStreamer con un'interfaccia, 
piuttosto che con una classe concreta.
L'implementazione di questa interfaccia sarà effettuata nelle classi di basso livello,
che contengono i dettagli di implementazione.

L'interfaccia che rappresenta un target di dati generico a cui verranno inviati i dati.
Si noti come le dipendenze siano state invertite: 
EventStreamer non dipende da un'implementazione concreta di un particolare target di dati,
non deve cambiare in linea con i cambiamenti su questo.
Al contrario ciascuna implementazione concreta dovrà implementare correttamente l'interfaccia 
e adattarsi ai cambiamenti se necessario.

NOTA:
Tutto sommato, non era obbligatorio definire la classe base astratta,
ma è comunque consigliabile per ottenere un design più pulito.
"""