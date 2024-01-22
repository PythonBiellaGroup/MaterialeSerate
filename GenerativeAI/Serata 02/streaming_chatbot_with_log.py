"""
- Data Masters -
Creazione e gestione di un chatbot interattivo basato su modelli di linguaggio avanzati.

Utilizzando librerie come LangChain e Gradio, viene configurato un modello di chat (ChatOpenAI) con specifiche
personalizzate; viene definito un template di prompt per guidare le risposte del chatbot; è implementata una memoria
per la conversazione in modo da poter mantenere il contesto ed è sfruttata una catena di esecuzione (LangChain) per
gestire l'input e le risposte; durante l'interazione con l'utente vengono loggati alcuni elementi della conversazione.
Infine, il codice utilizza Gradio per creare un'interfaccia utente che permette una gradevole interazione in tempo
reale con il chatbot.
"""

# Iniziamo importando le librerie necessarie i moduli specifici di LangChain per la
# gestione dei modelli di chat e delle memorie e l'interfaccia utente Gradio

from operator import itemgetter
import os
from langchain_openai import ChatOpenAI  # pip install langchain-openai
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder  # pip instal langchain
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.schema import SystemMessage, HumanMessage
import gradio as gr  # pip install gradio

# Inizializzazione del modello di chat, un modello basato su LangChain che utilizza la classe
# "ChatOpenAI", specificando alcune opzioni come la chiave API di OpenAI, la temperatura e il
# numero massimo di token per generazione.
llm = ChatOpenAI(openai_api_key=os.getenv("openai_key"), temperature=.2, max_tokens=1024, request_timeout=30)

# Definizione di un template di prompt: viene definito un template di prompt che include una
# descrizione di come il chatbot dovrebbe comportarsi ("Act like an expert data scientist...")
# scritto in inglese per una migliore comprensione da parte del modello e da un segnaposto per
# le conversazioni passate ("history").
# Questo template verrà utilizzato per creare prompt di chat durante le conversazioni.
system_template = ("Act like an expert data scientist by using casual, engaging language to convey the beauty of data"
                   " science in every conversation. Write short answers. Always include in your answers a lesson on the "
                   "data-driven mindset.")

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# Creazione di una memoria per la conversazione: viene creata una memoria denominata "history" utilizzando
# la classe "ConversationBufferMemory". Questa memoria conserverà i messaggi scambiati con il chatbot in
# modo da renderli disponibili a ogni singola nuova generazione di testo, mantenendo così il contesto
# durante tutta la conversazione
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Creazione di una catena di esecuzione: viene definita una catena che include tre step.
# Il primo step è una "RunnablePassthrough" che carica le conversazioni passate dalla memoria
# utilizzando il metodo "memory.load_memory_variables".
# Il secondo step è il template di prompt creato in precedenza.
# Il terzo step è il modello di chat LangChain.
chain = (
        RunnablePassthrough.assign(history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"))
        | chat_prompt
        | llm
)


def stream_response(input, history):
    """
    Gestione delle risposte del chatbot utilizzando la catena di esecuzione
    definita precedentemente per ottenere le risposte generate dal chatbot
    durante la generazione dell'output.
    :param input: messaggio di input
    :param history: conversazioni passate
    """
    if input is not None:
        # aggiungo la risposta dell'utente in memoria
        memory.chat_memory.add_user_message(input)

        # processo la risposta dell'LLM
        partial_message = ""
        for response in chain.stream({"input": input, "history": history}):
            partial_message += response.content
            yield partial_message  # trasforma il valore corrente di partial_message in un generatore e lo rende
            # disponibile all'esterno della funzione stream_response permettendo lo streaming
            # degli output generati, senza aspettare il termine della generazione

        # memorizzo anche la risposta dell'LLM in modo da renderla disponibile e poter così creare
        # un "contesto" della discussione / sessione attuale
        memory.chat_memory.add_ai_message(partial_message)

        # generazione di un riassunto della conversazione ed estrazione dei principali tag riscontrati
        res = llm.invoke([
            SystemMessage(
                content="Extract the main keywords in the text into a comma-separated list, then summarize the text in"
                        " a very short form. Please prefix the keywords with 'Keywords:' and the short summary with "
                        "'Summary:'"),
            HumanMessage(content=input + " " + partial_message)
        ])

        # log
        print('\n--- conversazione ---\n')
        print(res.content)
        print('\n------ memoria ------\n')
        hist = memory.load_memory_variables({})
        for elem in hist["history"]:
            print(type(elem), elem.content)
        print('\n---------------------\n\n\n')


# Creazione dell'interfaccia utente Gradio utilizzando "gr.ChatInterface",
# che utilizza la funzione "stream_response" per gestire le interazioni
# con il chatbot in modalità streaming in tempo reale
gr.ChatInterface(stream_response).queue().launch(debug=True)
