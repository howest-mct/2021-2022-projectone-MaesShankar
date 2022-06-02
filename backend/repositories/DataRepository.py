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
        sql = "SELECT * from Historiek ORDER BY datum ASC"
        return Database.get_rows(sql)
    @staticmethod
    def read_users():
        sql="SELECT * FROM Users ORDER BY UserID ASC"
        return Database.get_rows(sql)
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