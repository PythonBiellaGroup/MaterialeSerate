"""
E se aggiungiamo un altro metodo all'interfaccia IShape, come draw_triangle()?
"""


class IShape:
    def draw_square(self):
        raise NotImplementedError

    def draw_rectangle(self):
        raise NotImplementedError

    def draw_circle(self):
        raise NotImplementedError

    def draw_triangle(self):
        raise NotImplementedError


"""
Le classi devono implementare il nuovo metodo o verrà generato un errore.

Vediamo che è impossibile implementare una forma che possa disegnare un
cerchio ma non un rettangolo o un quadrato o un triangolo.
Possiamo solo implementare i metodi generando un errore che mostra
che l'operazione non può essere eseguita.

L'ISP disapprova il design di questa interfaccia IShape.
I clients (qui Rectangle, Circle e Square) non dovrebbero essere costretti
a dipendere da metodi di cui non hanno bisogno o di cui non fanno uso.

Inoltre, l'ISP afferma che le interfacce dovrebbero eseguire un solo lavoro
(come il principio SRP) ogni ulteriore raggruppamento di comportamenti
dovrebbe essere rimosso e assegnato ad un'altra interfaccia.

Qui, la nostra interfaccia IShape esegue azioni che dovrebbero essere gestite
in modo indipendente da altre interfacce.

Per rendere la nostra interfaccia IShape conforme al principio ISP, segreghiamo
le azioni su diverse interfacce.
Le classi (cerchio, rettangolo, quadrato, triangolo, ecc.) possono
semplicemente ereditare dall'interfaccia IShape e implementare il proprio
comportamento.
"""
