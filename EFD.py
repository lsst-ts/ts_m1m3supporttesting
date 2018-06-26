from Utilities import *
import MySQLdb

class EFD:
    def __init__(self):
        Log("EFD: Initialize")
        self.db = MySQLdb.connect(host = "localhost",
                             user="efduser",
                             passwd="lssttest",
                             db="EFD")
        self.cur = self.db.cursor()

    def Close(self):
        Log("EFD: Shutdown")
        self.db.close()
        
    def QueryOne(self, query):
        Log("EFD: QueryOne %s" % query)
        self.cur.execute(query)
        return self.cur.fetchone()
        
    def QueryAll(self, query):
        Log("EFD: QueryAll %s" % query)
        self.cur.execute(query)
        return self.cur.fetchall()