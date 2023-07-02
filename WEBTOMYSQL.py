import pymysql
import pymysql.cursors


class DCP_BDD:
    def __init__(self):
        pass

    def connec(self):
        connection = pymysql.connect(user="user1",
                                     password="pass1",
                                     host="host1",
                                     database="dcp",
                                     ssl_disabled=False)
        return connection
