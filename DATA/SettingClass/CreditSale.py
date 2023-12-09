from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Sale import Sale
from datetime import date


class CreditSale:
    table_name: str = DBTableName.credit_sale

    def __init__(self, id: int = None, refund_date: date = None,  sale: Sale = None):
        self.id = id
        self.refund_date = refund_date
        self.sale = sale

    def save_to_db(self):
        bd_connection = connect_to_db()
        with bd_connection.cursor() as my_cursor:
            my_cursor.execute(
                f"INSERT INTO {CreditSale.table_name} (refund_date, sale_id) VALUES (%s, %s);",
                [self.refund_date, self.sale.id])
            bd_connection.commit()
            return my_cursor.lastrowid

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else CreditSale(id=data_map.get("id"),
                                                   refund_date=data_map.get("refund_date"),
                                                   sale=Sale(id=data_map.get("sale_id")))

    @staticmethod
    def get_by_id(id: int = None, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT * FROM {CreditSale.table_name} WHERE id = %s;",
                    [id])
                result = my_cursor.fetchone()
                return CreditSale.from_map(result) if not return_map else result

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT * FROM {CreditSale.table_name} ORDER BY id DESC LIMIT 1;")
                result = my_cursor.fetchone()
                return CreditSale.from_map(result) if not return_map else result

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
                    my_cursor.execute(f"DELETE FROM {CreditSale.table_name} WHERE id = %s;", [id])
                    bd_connection.commit()
                    return True
        except:
            return False
