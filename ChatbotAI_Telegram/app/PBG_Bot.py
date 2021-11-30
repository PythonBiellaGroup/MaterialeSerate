#!/usr/bin/env python
# coding: utf-8

# # Classe NLP Querying

# ## Caricamento delle librerie

# In[1]:


import numpy as np
import pandas as pd
import re
import os
import random
import pprint
from collections import defaultdict
import pickle
import requests
import json
import datetime
import dateparser

import sklearn_crfsuite
from sklearn.feature_extraction.text import CountVectorizer
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix

from pprint import pprint


# In[2]:


import spacy

nlp = spacy.load("it_core_news_sm")


# ## Alcune funzioni utili

# In[4]:


def remove_nan(df: pd.DataFrame) -> dict:
    """Rimuove i valori nulli da una lista"""

    lookup_dict = df.to_dict("list")

    for k, v in lookup_dict.items():

        while np.nan in lookup_dict[k]:
            lookup_dict[k].remove(np.nan)

    return lookup_dict


# In[1]:


def rimuovi_punteggiatura(text):
    """
    I dati di training contengono parentesi quadre e tonde,
        quindi non vanno eliminate in questa fase
    """

    text = re.sub(r"[?]", " ?", text)
    text = re.sub(r"[\.,;:!]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text


# In[6]:


def spacy_entities_extractor(txt, npl: spacy):

    doc = nlp(txt.capitalize())
    token = doc[0]

    if token.ent_type_ != "":
        return token.ent_type_  # pos_
    else:
        return "O"


# In[7]:


def extend_data(df: pd.DataFrame, spacy: bool = False) -> pd.DataFrame:
    """
    Estende i dati attraverso un algortimo personalizzato
    """

    df["shift-3"] = df.groupby("n_frase")["word"].shift(1).str.slice(-3)
    df["shift+3"] = df.groupby("n_frase")["word"].shift(-1).str.slice(0, 3)
    df["shift-10"] = df.groupby("n_frase")["word"].shift(1).str.slice(-10)
    df["shift+10"] = df.groupby("n_frase")["word"].shift(-1).str.slice(0, 10)

    df["shift-3"].fillna("BOF", inplace=True)
    df["shift+3"].fillna("EOF", inplace=True)
    df["shift-10"].fillna("BOF", inplace=True)
    df["shift+10"].fillna("EOF", inplace=True)

    if spacy:
        df["spacy"] = df["word"].apply(spacy_entities_extractor)

    df["bias"] = 1

    try:
        df.drop(columns=["tag"], inplace=True)
    except:
        pass

    return df


# In[8]:


regex_str = r"\[(?P<name>[a-zA-Z_]+)\]\((?P<value>[a-zA-Z\' ]+)\)+"
slot_match = re.compile(regex_str)


# In[9]:


def conserva_solo_slot_name(text: str) -> str:
    """
    Per facilitare la riduzione dello spazio dimensionale
        vengono eliminati i valori degli slots
        mentre vengono conservati i loro nomi


    Parameters:
    -----------

    text : str

        è la stringa che contiene la frase


    Returns:
    -----------
    text : str

    """

    text = rimuovi_punteggiatura(text)

    pattern = r"(\([A-Za-z0-9 ]+\)|\[|\])"

    text = re.sub(pattern, "", text)

    return text


# **Operazioni:**
# 1. La classe deve verificare se esistono già i file pickle che conservano: modello, vocabolario e crf. Eventualmente parte il training comprensivo di generazione frase;
# 2. Se i dati sono caricati allora può elaborare le frasi
#
#

# In[10]:


class BotAI:
    def __init__(self, db_file: str, model_path: str = "models"):

        self.model_path = model_path
        self.db_file = db_file

        self.classifier_pickle = "classifier.pickle"
        self.label_encoder_pickle = "label_encoder.pickle"
        self.crf_model_pickle = "crf_model.pickle"
        self.vocabulary_pickle = "vocabulary.pickle"

        self.status = "0 - starter"

        self.lookups = None

        self.user_sentences = defaultdict(list)
        self.bot_sentences = defaultdict(list)
        self.dialogs = defaultdict(list)

        self.sentences_file = "sentences_origin.txt"
        self.sentences_file_generated = "sentences_generated.txt"
        self.n_sentences = 1000

        self.X = list()
        self.y = list()

        self.cm = None

        if self.check_model() == False:  # Verifica iniziale

            # self.build_lookup_tables()

            self.crf = sklearn_crfsuite.CRF(
                algorithm="lbfgs",
                c1=0.1,
                c2=0.1,
                max_iterations=100,
                all_possible_states=False,
                all_possible_transitions=False,
            )

            self.cv = CountVectorizer()
            self.le = LabelEncoder()

            self.classifier = SGDClassifier(fit_intercept=False, loss="log")

            self.training()
        else:
            # Carica i modelli

            # TODO: Make it DRY

            load_model = open(
                os.path.join(self.model_path, self.crf_model_pickle), "rb"
            )
            self.crf = pickle.load(load_model)

            load_model = open(
                os.path.join(self.model_path, self.vocabulary_pickle), "rb"
            )
            self.cv = pickle.load(load_model)

            load_model = open(
                os.path.join(self.model_path, self.label_encoder_pickle), "rb"
            )
            self.le = pickle.load(load_model)

            load_model = open(
                os.path.join(self.model_path, self.classifier_pickle), "rb"
            )
            self.classifier = pickle.load(load_model)

            self.sentences_extractor()

            self.is_ready()

            pass

        return None

    def check_model(self):
        """Cerca se ci sono già i modelli per la comprensione del testo"""

        risp = False

        self.build_lookup_tables()

        if self.classifier_pickle in os.listdir(self.model_path):
            if self.label_encoder_pickle in os.listdir(self.model_path):
                if self.crf_model_pickle in os.listdir(self.model_path):
                    if self.vocabulary_pickle in os.listdir(self.model_path):
                        risp = True

        return risp

    def get_status(self) -> str:
        """Restituisce lo stato attuale"""

        return self.status

    def is_ready(self) -> bool:
        """Verifica se l'istanza è pronta"""

        if self.check_model():
            self.status = "ready"
            return True
        else:
            return False

    def build_lookup_tables(self) -> bool:

        df_entities = pd.read_excel("data/dataset.xlsx", sheet_name="entities_slots")

        self.lookups = remove_nan(df_entities)

        self.status = "1 - lookups tables loaded"

        return True

    def sentences_extractor(self) -> bool:
        """Estrae le frasi dell'utente (le salva in un file txt), del bot, della conversazione"""

        # UTENTE

        df_user = pd.read_excel("data/dataset.xlsx", sheet_name="user", header=None)
        df_user.columns = ["user", "sentences"]
        df_user["user"] = df_user["user"].fillna(method="ffill", axis=0)

        df_grouped = df_user.groupby("user")

        for group in df_grouped.groups:

            self.user_sentences[group] = df_grouped.get_group(group)[
                "sentences"
            ].tolist()

        # FILE CON LE FRASI

        #         i = True

        #         for k, v in self.user_sentences.items():

        #             for values in v:

        #                 if i:
        #                     with open(self.sentences_file, "w+") as f:
        #                         f.writelines(f"{values}|{k}\n")
        #                         i = False
        #                 else:
        #                     with open(self.sentences_file, "a+") as f:
        #                         f.writelines(f"{values}|{k}\n")

        # BOT

        df_bot = pd.read_excel("data/dataset.xlsx", sheet_name="bot", header=None)
        df_bot.columns = ["bot", "sentences"]
        df_bot["bot"] = df_bot["bot"].fillna(method="ffill", axis=0)

        df_grouped = df_bot.groupby("bot")

        for group in df_grouped.groups:

            self.bot_sentences[group] = df_grouped.get_group(group)[
                "sentences"
            ].tolist()

        # DIALOGS

        df_dialogs = pd.read_excel("data/dataset.xlsx", sheet_name="dialogs")

        self.dialogs = remove_nan(df_dialogs)

        self.dialogs = {v[0]: v[1] for v in list(self.dialogs.values())}

        self.df_query = pd.read_csv(self.db_file)

        self.status = "2 - estrazione dati completata"

        return True

    def sentences_generator(self) -> bool:

        #         sentences, categories = [], []

        #         with open(self.sentences_file, encoding="utf-8") as f:
        #             dataset = f.read()
        #             dataset = dataset.split("\n")

        #         for data in dataset:
        #             sentence = data.split("|")

        #             if len(sentence) > 1:

        #                 # TODO: Lasciare upper ?

        #                 sentences.append(sentence[0].upper())
        #                 categories.append(sentence[1])

        #         assert len(sentences) == len(categories)

        slots = list(self.lookups.keys())

        for i in range(self.n_sentences):

            category = random.choice(list(self.user_sentences.keys()))

            sentence = random.choice(list(self.user_sentences[category]))

            sentence = sentence.upper()

            regex_str = r"\[(?P<name>[a-zA-Z_]+)\]\((?P<value>[a-zA-Z\' ]+)\)+"
            slot_match = re.compile(regex_str)

            matches = slot_match.findall(sentence)

            dct = {k: v for k, v in matches}

            for k, v in dct.items():

                v2 = random.choice(self.lookups[k.upper()])

                sentence = re.sub(f"\[{k}\]\({v}\)", f"[{k}]({v2})", sentence)

            #     #     index = random.randint(0, len(sentences) - 1)

            #     #     sentence = sentences[index]
            #     #     category = categories[index]

            #     for key in slots:

            #         """
            #         Ogni volta che regex individua lo slot nella frase
            #             sostituisce il valore con uno estratto in modo casuale
            #         """

            #         #         regex_str = fr"\[{key}\]\((?P<value>[a-z ]+)\)+"

            #         #         slot_match = re.compile(regex_str)

            #         slot_sub = re.compile(fr"\[{key}\]\(.+\)")

            #         repl = fr"[{key}]({random.choice(lookups[key])})"

            #         sentence = slot_sub.sub(repl, sentence)

            #         """
            #         Poi riassocia la categoria di partenza
            #         """

            if i == 0:

                with open(self.sentences_file_generated, "w+") as f:
                    f.writelines(f"{sentence}|{category}\n")

            else:

                with open(self.sentences_file_generated, "a+") as f:
                    f.writelines(f"{sentence}|{category}\n")

        self.status = "3 - frasi generate"

        return True

    def prepare_data_crf(self) -> bool:

        with open(self.sentences_file_generated, encoding="utf-8") as f:
            sentences = f.read()
            sentences = sentences.split("\n")

        arr_sentences = list()
        arr_categories = list()

        for n, sentence in enumerate(sentences):

            try:

                sentence, categ = sentence.split("|")

                sentence = rimuovi_punteggiatura(sentence)

                arr_categories.append(categ)

                splits = slot_match.split(sentence)

                #         match = slot_match.search(frase)
                matches = slot_match.findall(sentence)

                dct = {k: v for k, v in matches}

                if matches is not None:

                    for split in splits:
                        if split in list(dct.values()):
                            for value in split.split():

                                index = list(dct.values()).index(split)
                                key = list(dct.keys())[index]

                                arr_sentences.append([n, value, key])
                        elif split in list(dct.keys()):
                            pass
                        else:
                            for value in split.split():
                                arr_sentences.append([n, value, "O"])

                else:
                    """
                    Serve per verificare se in qualche frase non avviene il match
                    """
                    print(n, frase)

            except Exception as err:
                pass

        df = pd.DataFrame(arr_sentences, columns=["n_frase", "word", "tag"])
        df_target = df[["n_frase", "tag"]]

        for k, v in df_target.groupby("n_frase"):

            self.y.append(v["tag"].tolist())

        df = extend_data(df, spacy=False)

        for k, v in df.groupby("n_frase"):

            v.drop(columns="n_frase", inplace=True)

            self.X.append(v.to_dict("records"))

        self.status = "4 - dati pronti per il training del crf"

        return True

    #### INIZIO FUNZIONI PER IL CONDITIONAL RANDOM FIELD ####

    def training_crf(self) -> bool:

        self.crf.fit(self.X, self.y)

        save_model = open(os.path.join(self.model_path, self.crf_model_pickle), "wb")
        pickle.dump(self.crf, save_model)
        save_model.close()

        self.status = "5 - crf model trained"

    def prepare_sentence(self, sentence: str) -> List[pd.DataFrame, list]:
        """
        Prepare la frase per il predict

        Parameters:
        -----------

        sentence : str

            è la frase che sarà elaborata


        Returns:
        -----------
        df : DataFrame

        X_arr[0] : array

            dati in formato utile a CRF per il predict

        """

        sentence = rimuovi_punteggiatura(sentence)

        X_arr = list()

        df = pd.DataFrame(data=[i for i in sentence.split()], columns=["word"])
        df["n_frase"] = 1

        df = extend_data(df)

        for k, v in df.groupby("n_frase"):

            v.drop(columns="n_frase", inplace=True)

            X_arr.append(v.to_dict("records"))

        return df, X_arr[0]

    def extend_sentence(self, sentence: str) -> pd.DataFrame:
        """
        Estrae slots e lo aggiunge al DataFrame come colonna

        Parameters:
        -----------

        sentence : str

            è la stringa che contiene la frase

        model : sklearn_crfsuite.estimator.CRF

            è il modello addestrato di ConditionalRandomField


        Returns:
        -----------
        df : DataFrame

            al DataFrame di partenza viene aggiunta una colonna
            con l'indicazione del tipo di slot individuato

        """

        df, X_arr = self.prepare_sentence(sentence)

        df["slots"] = self.crf.predict_single(X_arr)

        return df

    #### DUCKLING ####

    def extract_datetime(self, text: str, url="http://0.0.0.0:8000/parse"):

        data = {"locale": "it_IT", "text": text}

        resp = None

        datetimes = list()

        try:

            response = requests.post(url, data=data)

            try:

                if response.status_code == 200:

                    for dt in response.json():

                        if dt["dim"] == "time":

                            dtime = dt["value"]["value"]
                            dtime = dateparser.parse(dtime)

                            datetimes.append(dtime)

                resp = dict()

                if len(datetimes) > 1:
                    resp["datetime"] = list([min(datetimes), max(datetimes)])
                else:
                    resp["datetime"] = list(datetimes)

            except:
                pass

        except:
            pass

        return resp

    def slots_extractor(self, sentence: str) -> defaultdict:
        """
        Restituisce un dictionary degli slots individuati

        Parameters:
        -----------

        sentence : str

            è la stringa che contiene la frase

        model : sklearn_crfsuite.estimator.CRF

            è il modello addestrato di ConditionalRandomField


        Returns:
        -----------
        dd : dictionary

        """

        df = self.extend_sentence(sentence)

        dd = defaultdict(list)

        for k, v in df.query("slots != 'O'").groupby("slots"):
            dd[k] = " ".join(v["word"])

        """
        Estrazione date ed orari tramite duckling    
        """

        date_time = self.extract_datetime(sentence)

        if date_time is not None and len(date_time) > 0:
            dd["DATETIMES"] = date_time["datetime"]

        return dd

    #### FINE FUNZIONI PER IL CONDITIONAL RANDOM FIELD ####

    #### INIZIO FUNZIONI PER LA CLASSIFICAZIONE DELL'INTENT ####

    def replace_slot_values(self, sentence_dict: dict) -> dict:
        """
        Integrazione dictionary - parte 1 di 2


        Per operare una riduzione delle variabili
        sostituisce il valore con il relativo slot
        """

        sentence_dict["replaced_sentence"] = sentence_dict["sentence"]

        for k, v in sentence_dict["slots"].items():

            if k != "DATETIMES":

                sentence_dict["replaced_sentence"] = re.sub(
                    v, k, sentence_dict["replaced_sentence"]
                )

        return sentence_dict

    def add_slots(self, sentence: str) -> dict:
        """
        Integrazione dictionary - parte 2 di 2
        """

        sentence_dict = {}

        sentence = rimuovi_punteggiatura(sentence)

        slots_dict = self.slots_extractor(sentence)

        sentence_dict["sentence"] = sentence
        sentence_dict["slots"] = slots_dict

        sentence_dict = self.replace_slot_values(sentence_dict)

        #     date_time = extract_datetime(sentence)

        #     if date_time is not None and len(date_time) > 0:
        #         sentence_dict['datetimes'] = date_time['datetime']
        #     else:
        #         sentence_dict['datetimes'] = False

        return sentence_dict

    def training_intents(self) -> bool:
        """Addestramento algoritmo di classificazione intents"""

        df = pd.read_csv(self.sentences_file_generated, sep="|", header=None)

        df.columns = ["sentences", "intents"]

        df["sentences"] = df["sentences"].apply(conserva_solo_slot_name)

        self.cv.fit(df.sentences)

        with open(
            os.path.join(self.model_path, self.vocabulary_pickle), "wb"
        ) as vocabs:
            pickle.dump(self.cv, vocabs)

        #### GENERAZIONE FRASI FAKE ####

        fake_list = list()

        for i in range(30):
            fake_list.append(
                " ".join(random.choices(list(self.cv.vocabulary_.keys()), k=10))
            )

        df_fake = pd.DataFrame({"sentences": fake_list, "intents": "fake"})

        df = pd.concat([df, df_fake], axis=0, ignore_index=True)

        #### LABEL ENCODER ####

        self.le.fit(df.intents.unique())

        with open(
            os.path.join(self.model_path, self.label_encoder_pickle), "wb"
        ) as label_encoder:
            pickle.dump(self.le, label_encoder)

        labels_categories = self.le.transform(df.intents.values)

        self.classifier.fit(
            X=self.cv.transform(df["sentences"].values).toarray(), y=labels_categories
        )

        with open(os.path.join(self.model_path, self.classifier_pickle), "wb") as cls:
            pickle.dump(self.classifier, cls)

        predicted_categories = [
            self.classifier.predict(
                [np.max(self.cv.transform(sentence.split()).toarray(), axis=0)]
            )[0]
            for sentence in df.sentences.values
        ]

        self.cm = confusion_matrix(labels_categories, predicted_categories)

        self.status = "6 - classifier model trained"

        return True

    #### FINE FUNZIONI PER LA CLASSIFICAZIONE DELL'INTENT ####

    def get_intents_and_slots(self, sentence: str, threasold=0.25) -> dict:
        """
        Estrae gli intents e gli slots dalla frase
        """

        sentence_dict = self.add_slots(sentence)

        sentence = sentence_dict["replaced_sentence"]

        arr = self.cv.transform(
            self.add_slots(sentence)["replaced_sentence"].split()
        ).toarray()

        arr = np.max(arr, axis=0)

        probs = self.classifier.predict_proba([arr])[0]

        df = pd.DataFrame({"classes": self.le.classes_, "probs": probs})
        df.sort_values("probs", ascending=False, inplace=True)
        classes_with_prob = df[df["probs"] > threasold].to_dict("records")
        sentence_dict["intents"] = classes_with_prob

        max_intent = self.le.classes_[np.argmax(probs)]
        sentence_dict["max_intent"] = max_intent

        return sentence_dict

    def bot_reply(self, sentence: str, threasold=0.25) -> dict:
        """
        Genera la risposta
        """

        sentence = sentence.upper()

        data = self.get_intents_and_slots(sentence, threasold)

        if (data["intents"][0]["probs"] > 0.75) and data["intents"][0][
            "classes"
        ] != "fake":

            intent = data["max_intent"]

            reply = self.dialogs[intent]

            reply_str = random.choice(self.bot_sentences[reply])

            query_list = list()

            for k, v in data["slots"].items():

                if k != "DATETIMES":

                    query_list.append(f"{k} == '{v}'")

                    k = list(data["slots"].keys())[0]
                    k = f"[{k}]"

                    v = list(data["slots"].values())[0]

                    reply_str = re.sub(f"[{k}+]", v, reply_str)

            query = " and ".join(query_list)

            n = self.df_query.query(query)["NOME"].drop_duplicates().count()

            return reply_str % (n)

        else:

            intent = "Non ho capito, riformula meglio la tua domanda"

            return intent

    def training(self):

        self.build_lookup_tables()

        self.sentences_extractor()

        self.sentences_generator()

        self.prepare_data_crf()

        self.training_crf()

        self.training_intents()

        return True


# In[18]:


# botAI = BotAI(db_file="db_esempio.csv")


# In[29]:


# botAI.get_status()


# In[28]:


# botAI.training_intents()


# In[27]:


# botAI.cm


# In[26]:


# print(f"Accuracy: {sum(botAI.cm.diagonal()) / botAI.cm.sum() * 100}%")


# In[ ]:


# In[25]:


# botAI.bot_reply("quante fattorie didattiche ci sono a Caserta ?")


# In[ ]:


# In[ ]:
