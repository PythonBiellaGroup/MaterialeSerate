# Python Biella Group - Bot

## Introduzione

Semplice Bot costruito per una serata al Python Biella Group

## Installazione del modello della lingua italiana

Dopo l'installazione di spacy bisogna bisogna scaricare il modello italiano:

```
python -m spacy download it_core_news_lg
```

## Installazione e avvio di duckling

```
docker pull rasa/duckling

docker run --rm -p 8000:8000 rasa/duckling
```

## Set del Token Telegram

```
export PBG_BOT='TOKEN'
```

## Avvio del Bot

Il bot è stato concepito per essere compatibile con qualsiasi framework.
