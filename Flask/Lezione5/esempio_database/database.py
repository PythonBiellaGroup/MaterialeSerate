from main import db, Corso

try:
    # Creazione delle tabelle
    db.create_all()

    # costruiamo dei nuovi oggetti
    corso_flask = Corso("Flask", "Andrea", 10)
    corso_pygame = Corso("Pygame", "Mario", 20)

    # Visualizziamo gli id
    print("Id corso flask: ", corso_flask.id)
    print("Id corso pygame", corso_pygame.id)

    # Aggiungiamo alla sessione dei database i nostri oggetti
    db.session.add_all([corso_flask, corso_pygame])

    db.session.commit()

    # Visualizziamo gli id
    print("Id corso flask: ", corso_flask.id)
    print("Id corso pygame", corso_pygame.id)
    
except Exception as message:
    print(f"Impossibile inserire un nuovo record... :{message}")

