from numpy import *
import mysql.connector


class db_handler():
    def __init__(self, _authorID, _userID):
        self.host = "localhost"
        self.user = "DakKilvari"
        self.password = "Pilvax_Officer_Dak4160"
        self.database = "swgoh"
        self.authorID = _authorID
        self.userID = _userID

    def fetchMe(self, raw_allycode, mycursor):

        if raw_allycode == "me":
            sql = "SELECT Allycode FROM pilvax WHERE DiscordID = %s"
            adr = (self.authorID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()
            for x in myresult:
                allycode = x
            print(allycode)
        else:
            try:
                allycode = int(raw_allycode)
            except:
                try:
                    s = self.userID
                    sql = "SELECT Allycode FROM pilvax WHERE DiscordID = %s"
                    adr = (self.userID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        allycode = x
                    print(allycode)
                except:
                    allycode = 000000000
        return allycode


    def myDb(self):

        mydb = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        return mydb