import re

def get_class(file:str, class2id:dict):
    """
    Estrae la classe dal path del file
    """

    txt = file.split("/")[-1]
    txt = txt.split("_")[1]
    
    classe = class2id[txt]
    
    return classe


def read_text_data(txt_file:str) -> str:
    """
    Legge il contenuto testuale del file e restituisce il risultato
    """

    with open(txt_file, 'r', encoding='utf-8') as f:
        txt = f.readlines()
        txt = " ".join(" ".join(txt).split("\n"))
        txt = re.findall(r"<body>(.*)</body>", txt)[0]
        
    return txt

