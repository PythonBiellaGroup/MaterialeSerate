# ESEMPIO CRUD
# CREATE
# READ (SELECT)
# UPDATE
# DELETE

from main import db, Corso

## CREATE
corso_pandas = Corso("Pandas", "Maria Teresa", 30)
db.session.add(corso_pandas)
db.session.commit()

# READ all the courses
tutti_corsi = Corso.query.all()
print(tutti_corsi)

# SELECT (READ) corso Pandas tramite id
corso_selezionato = Corso.query.get(3)
print(corso_selezionato)

# FILTRO
corso_selezionato_nome = Corso.query.filter_by(nome="Pandas")
print(corso_selezionato_nome)  # ritorna la query
print(corso_selezionato_nome.all())  # ritorna tutti i risultati trovati
print(corso_selezionato_nome.first())  # ritorna solamente il primo risultato trovato

# UPDATE
corso_flask = Corso.query.get(1)
corso_flask.allievi = 100
db.session.add(corso_flask)
db.session.commit()

print(Corso.query.get(1))

# DELETE
corso_rimuovere = Corso.query.filter_by(nome="Pandas").all()
db.session.delete(corso_rimuovere[-1])
db.session.commit()

print(Corso.query.all())
