import numpy as np


@np.vectorize
def remove_dollar(label: str):
    return float(label.replace("$", "").replace(",", ""))
