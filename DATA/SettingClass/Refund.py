from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Sale import Sale


class Refund:
    my_db = connect_to_db()
    table_name: str = DBTableName.refund

    def __init__(self, id: int = None, value: float = None, sale: Sale = None):
        self.id = id
        self.value = value
        self.sale = sale

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute("INSERT INTO %s (value, sale_id) "
                          "VALUES (%s, %s);", [self.table_name, self.value, self.sale.id])
                bd_connection.commit()
                return my_cursor.lastrowid

    def delete_last_permanently(self, limit: int = 1):
        try:
            with connect_to_db() as bd_connection:
                with bd_connection.cursor(dictionary=True) as my_cursor:
                    my_cursor.execute(f"DELETE FROM {self.table_name} ORDER BY id DESC LIMIT %s;", [limit])
                    bd_connection.commit()
                    return True
        except:
            return False

    @staticmethod
    def delete_permanently(id: int = 1):
        try:
            with connect_to_db() as bd_connection:
                with bd_connection.cursor(dictionary=True) as my_cursor:
                    my_cursor.execute(f"DELETE FROM {Refund.table_name} WHERE id = %s;", [id])
                    bd_connection.commit()
                    return True
        except:
            return False
