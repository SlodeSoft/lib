import pyodbc
from lib import OARKEnho

class CDS_BDD:
    def __init__(self):
        pass

    def connec(self=None):
        # SQL CONNECTION
        __server__ = OARKEnho.__deux__.password
        __database__ = OARKEnho.__trois__.password
        __username__ = OARKEnho.__cinq__.username
        __password__ = OARKEnho.__cinq__.password
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + __server__ + ';DATABASE=' + __database__ + ';UID=' + __username__ + ';PWD=' + __password__)
        cursor = cnxn.cursor()
        return cursor

