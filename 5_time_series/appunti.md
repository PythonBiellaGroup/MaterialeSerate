### Lista di punti da trattare

Generale
- Lista covariate 
- Quanti dati ci sono per ogni covariata

Intervallo di campionamento
- Per ogni covariata, voglio sapere l'intervallo/gli intervalli di tempo in cui sono disponibili i dati
- Per ogni covariata, voglio sapere la frequenza di campionamento Minima, Media e Massima.
- Per le covariate con intervalli discordanti, voglio sapere la distribuzione degli intervalli di campionamento.
- Per le covariate con intervalli discordanti, può essere utile sapere gli esatti periodo in cui l’intervallo di campionamento è cambiato.
- Processing delle covariate con intervalli di campionamento non costanti tramite resampling

Valori di ogni covariata
- Quali covariate hanno almeno un valore NaN.
- Quali covariate hanno tutti o una parte dei valori pari a un valore costante
- Per ogni covariata, min, max, devstd, avg, median, distribuzione dei valori (hist), curva
- Possibilità di filtrare una o più o tutte le covariate sulla base di valori assunti da un’altra covariata. E.g. filtrare ts in base alla label di un’altra ts (dato acceso/spento)
- Processing dei valori NaN di una covariata

Outliers
- Per ogni covariata, voglio sapere il timestamp in cui si registra un outlier (l’outlier lo seleziono graficamente o con delle soglie numeriche manuali (fisse o variabili) o IQR)
- Per ogni covariata, voglio eliminare gli outliers con una determinata tecnica

Correlazione
- Per ogni covariata, autocorrelazione
- Per 2 o più covariate, correlazione


