# Devlog

# 7a settimana

Gestione Profilo

Navigation bar

Post

Commenti

Corso
- Aggiunta stato (completo, in corso, organizzato, da organizzare)
- Aggiunta link github/documentazione
- Aggiunta gestione tag in Edit Corso (relazione N:N)


# 6a settimana

Autenticazione
- login
- logout
- registrazione
- password dimenticata
- conferma registrazione

Autorizzazioni alle operazioni

# 5a settimana

10/11/2020
- base.html - Header Completa Boostrap invece che Navigation bar (Risolto il problema xlink:href per sprite.svg; c'era un 404)
- Aggiunta pagina "Prossime serate"

11/11/2020
- Lista completa serate utilizzando lo stesso template delle "prossime serate"
- Aggiunta bottoni per edit e cancellazione (ancora TO DO)

12/11/2020
- Separazione html tra lista serate e prossime serate
- Revisione file configurazione e application factory (propedeutico per test)

13/12/2020
- Creazione del package di test

14/12/2020
- Creazione del blue print "main"
- Aggiunta ore-minuti nella "data" della serata

15/12/2020
- Preparazione slides
- Aggiunte live serata

# 4a settimana

03/11/2020
- Aggiunto menu corsi (lista/nuovo)
- Aggiunta pagina lista corsi

04/11/2020
- Aggiunto in menu corsi: gestione tags
- Lista, cancellazione dei tags
- (Modello) SERATA: aggiunto link incontro (Zoom o altro)/ aggiunto link registrazione (Youtube o altro)

06/11/2020
- Aggiunta pagina dettaglio corso (da lista)

07/11/2020
- Aggiunta funzione creazione/edit Tag
- Correzioni di imprecisioni varie non bloccanti
- Refactoring creazione corso, con pieno utilizzo WTform
- (Modello) CORSO: eliminato numero_lezioni; sistemazione view, form e data.py
- Cancellazione Corso da pagina di dettaglio
- Pagina Dettaglio Corso: tags e serate visualizzate solo se presenti
- Pagina Dettaglio Corso: aggiunta gestione del link alla registrazione Youtube, ove presente

08/11/2020
- Aggiunto "required" nelle form html ove necessario
- Pagina Dettaglio Corso: aggiunta in lista visualizzazione serata con registrazione non presente
- Pagina Dettaglio Corso: possibilità di aggiungere Serata al corso
- Creato Blueprint "tags" con relativi spostamenti di pagine e metodi
- Refactoring; naming (routes invece di views); creato models in blueprint tag

09/11/2020
- Refactoring dei modelli
- Creato Blueprint per Serate
- Sistemata cartella static dai Blueprint

# Applicazioni semplici Flask da cui imparare

Riferimento per il libro:
https://github.com/miguelgrinberg/flasky

https://github.com/OmkarPathak/A-Simple-Note-Taking-Web-App

# TO DO Modello

Ruolo
- Aggiungere "moderatore" ?

# TO DO App
- CSS utenti e blog
- Immagine statica corso


# Corso Flask
## Progetto di esempio

In questo progetto proveremo ad integrare tutte le nozioni viste durante il corso di Flask in modo da realizzare un portale per il Python Biella Group.

In questo portale si potrà:
1. Visualizzare l'elenco dei corsi attivi e passati
2. Inserire un nuovo corso
3. Definire delle giornate di corso
4. Fare login con un particolare utente (amministratore o normale)
5. A seconda dei permessi si potranno modificare o creare nuovi corsi oppure visualizzare l'elenco dei corsi
6. Creare articoli di blog con commenti


**Step progettuali**
Elenco di cose da trattare durante il corso:
1. Suddivisione in cartelle del progetto
2. Creare ambiente con venv
3. Definire app.py e __init__ del progetto + configurazione bootstrap locale
4. Definire i modelli dei dati e lanciare costruzione del database
5. Costruire i templates base usando bootstrap con pagine di errore
6. Costruire la vista dei corsi con form di compilazione + Visualizzazione dei risultati
7. Agganciare i corsi al DB
8. Costruire funzionalità di visualizzazione di tutti i corsi esistenti all'interno del database
9. Costruire funzionalità delle serate
10. Maschera di Login con funzionalità di Login e permessi di visualizzazione
(fino qui)
11. Pagina di Blog
12. Finalizzazione e test sulla pagina
13. Gestione della sicurezza
14. Deploy
15. Heroku


**Comandi utili**

Flask Migrate commands
```
##### Export Path #####
#MacOS/Linux
export FLASK_APP=app.py

#Windows
set FLASK_APP=app.py

##### Migration commands #####
flask db init #set up the migrations directory
flask db migrate -m "some message" #set up the migration file (is always usefull inserting a comment to remember what you have done)
flask db upgrade #update the database with the migration

```


**Bonus track** se abbiamo tempo di farlo
- Import dei dati passando da script SQL con SQLAlchemy (in modo da scriptare i dati di inizializzazione in modo più facile)
- Login con Google
- Docker con docker-compose
- Pipeline di deploy CI/CD con GitLab
- Pipeline di deploy CI/CD con GitHub
- Test browser con Selenium
- Test browser con Behave

Link e materiale utile
- Tema Bootstrap Italia: https://italia.github.io/bootstrap-italia/
- Behave: https://behave.readthedocs.io/en/latest/
  