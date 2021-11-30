#!.venv/bin/python
# coding: utf-8

# import Class_NLP_Query

from PBG_Bot import BotAI

botAI = BotAI(db_file="data/db_esempio.csv")

if botAI.check_model():
    while True:

        try:

            nuova_frase = input("Chiedi qualcosa:")

            print(botAI.bot_reply(nuova_frase))

        except KeyboardInterrupt:
            break
