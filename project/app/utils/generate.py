import uuid
from datetime import datetime

import pandas as pd


def namefile():
    curr_time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    return curr_time+"-"+str(uuid.uuid4())

def read_xlsx(content):
    try:
        df = pd.read_excel(content, engine="openpyxl")
    except FileNotFoundError as e:
        print("FileNotFoundError({0}): {1}".format(e.errno, e.strerror))
    except pd.errors.EmptyDataError as e:
        print(e)
    return df