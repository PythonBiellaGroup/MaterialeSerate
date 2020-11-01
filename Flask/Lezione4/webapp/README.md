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
  