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
        sql="SELECT * FROM Users ORDER BY UserID DESC"
        return Database.get_rows(sql)