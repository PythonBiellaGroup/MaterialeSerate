import base64
from io import BytesIO

import pandas as pd


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="openpyxl")
    df.to_excel(writer, index=False, sheet_name="Sheet1")
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df, excel_check=False):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    if excel_check:
        output_file = to_excel(df)
        text = "Download excel data"
    else:
        output_file = df.to_csv(index=False)

        text = "Download csv data"
    b64 = base64.b64encode(
        output_file.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="dataframe.csv">{text}</a>'
    return href