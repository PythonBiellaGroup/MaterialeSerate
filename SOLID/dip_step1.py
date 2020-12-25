"""
Dependency Inversion Principle
"""


class EventStreamer():
    def __init__(self, parsed_data: str):
        self.parsed_data = parsed_data
        self.client = Syslog()

    def stream(self):
        self.client.send(self.parsed_data)


class Syslog():
    @staticmethod
    def send(data: str):
        print(f"Syslog send: {data}")
        pass


streamer1 = EventStreamer("for Syslog data!")
streamer1.stream()

"""
Questo design non è molto buono, perché abbiamo una classe di alto livello
(EventStreamer) che dipende da una di basso livello (Syslog è un dettaglio
di implementazione).
Se qualcosa cambia nel modo in cui vogliamo inviare i dati a Syslog,
EventStreamer dovrà essere modificato.

Se vogliamo cambiare la destinazione dei dati per una diversa o aggiungerne
di nuovi in ​​fase di esecuzione, siamo anche nei guai perché ci troveremo a
modificare costantemente il metodo stream() per adattarlo a queste esigenze.
"""
