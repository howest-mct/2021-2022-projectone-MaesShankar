from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_history():
        sql = "SELECT * from Historiek ORDER BY HistoriekID DESC LIMIT 50"
        return Database.get_rows(sql)
    @staticmethod
    def read_alc_history():
        sql = "SELECT * FROM AlcoholHistoriek ORDER BY AlcHistoriekID DESC LIMIT 50"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_alc_history_user(id):
        sql="SELECT * FROM AlcoholHistoriek WHERE UserID=%s ORDER BY AlcHistoriekID DESC LIMIT 50;"
        params=[id]
        return Database.get_rows(sql,params)

    @staticmethod
    def read_users():
        sql="SELECT * FROM Users ORDER BY UserID ASC"
        return Database.get_rows(sql)
    @staticmethod
    def read_userID(id):
        sql="SELECT UserID FROM Users Where RFID like %s"
        params=[id]
        return Database.get_rows(sql,params)
    @staticmethod
    def read_toegang(id):
        sql="SELECT Toegang FROM Users Where RFID like %s"
        params=[id]
        return Database.get_rows(sql,params)
    @staticmethod
    def update_toegang(toegang,id):
        sql="UPDATE Users SET Toegang=%s WHERE RFID=%s ;"
        params=[toegang,id]
        Database.execute_sql(sql,params)
    

    
    @staticmethod
    def create_log(DeviceID,ActieID,Datum,Waarde,Commentaar):
        sql = "INSERT INTO Historiek(DeviceID,ActieID,Datum,Waarde,Commentaar) Values(%s,%s,%s,%s,%s);"
        params = [DeviceID,ActieID,Datum,Waarde,Commentaar]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def create_alc_log(UserID,ADatum,AWaarde):
        sql = "INSERT INTO AlcoholHistoriek(UserID,ADatum,AWaarde) Values(%s,%s,%s);"
        params = [UserID,ADatum,AWaarde]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def getAwaardes():
        sql = 'SELECT AWaarde FROM AlcoholHistoriek  ORDER BY AlcHistoriekID desc LIMIT 8'
        return Database.get_rows(sql)
    @staticmethod
    def gettemps():
        sql = 'SELECT Waarde FROM Historiek WHERE DeviceID=2 order by Datum desc LIMIT 8;'
        return Database.get_rows(sql)
    @staticmethod
    def getdata():
        sql = 'SELECT Datum FROM Historiek WHERE DeviceID=2 order by Datum desc LIMIT 8;'
        return Database.get_rows(sql)
    @staticmethod
    def getlatestalc():
        sql = 'SELECT AWaarde FROM AlcoholHistoriek  ORDER BY AlcHistoriekID desc LIMIT 1;'
        return Database.get_rows(sql)