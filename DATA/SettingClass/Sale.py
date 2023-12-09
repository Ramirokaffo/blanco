from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Client import Client
from datetime import datetime, date

from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Staff import Staff


class Sale:
    table_name: str = DBTableName.sale

    def __init__(self, id: int = None, is_paid: bool = None, is_credit: bool = None, client: Client = None,
                 create_at: datetime = None, delete_at: datetime = None, total: float = None, staff: Staff = None
                 , daily: Daily = None):
        self.id = id
        self.is_paid = is_paid
        self.create_at = create_at
        self.delete_at = delete_at
        self.is_credit = is_credit
        self.total = total
        self.client = client
        self.daily = daily
        self.staff = staff

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"INSERT INTO {Sale.table_name} (is_paid, is_credit, client_id, staff_id, daily_id, total) "
                                  "VALUES (%s, %s, %s, %s, %s, %s);", [self.is_paid, self.is_credit, self.client.id,
                                                                       self.staff.id, self.daily.id, self.total])
                bd_connection.commit()
                return my_cursor.lastrowid

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else Sale(id=data_map.get("id"), is_paid=data_map.get("is_paid"),
                                              create_at=data_map.get("create_at"),
                                              delete_at=data_map.get("delete_at"),
                                              client=Client(id=data_map.get("client_id")),
                                              staff=Staff(id=data_map.get("staff_id")),
                                              daily=Daily(id=data_map.get("daily_id")),
                                              total=data_map.get("total"))

    @staticmethod
    def get_sale_list(page: int = 0, count: int = 20):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Sale.table_name} WHERE delete_at IS NULL ORDER BY id DESC LIMIT %s OFFSET %s;",
                                  [count, page * count])
                return [Sale.from_map(result) for result in my_cursor.fetchall()]

    @staticmethod
    def get_ca_by_date(ca_date: date = date.today(), is_credit: bool = False, max_hours: int = None) -> float:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT SUM(total) AS ca FROM {Sale.table_name} WHERE date(create_at) = %s AND "
                                  f'''is_credit = %s {f"AND HOUR(create_at) < '{max_hours}'" if max_hours is not None 
                                  else ''} AND delete_at IS NULL;''', [ca_date, is_credit])
                return my_cursor.fetchone()["ca"]

    @staticmethod
    def get_ca_by_daily(daily_id: int = Daily.get_current_daily().id, is_credit: bool = False, max_hours: int = None) -> float:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT SUM(total) AS ca FROM {Sale.table_name} WHERE daily_id = %s AND "
                                  f'''is_credit = %s {f"AND HOUR(create_at) < '{max_hours}'" if max_hours is not None 
                                  else ''} AND delete_at IS NULL;''', [daily_id, is_credit])
                return my_cursor.fetchone()["ca"]

    @staticmethod
    def get_first_sale_date_time(sale_date: date = date.today(), is_credit: bool = False) -> datetime:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT create_at FROM {Sale.table_name} WHERE date(create_at) = %s AND "
                                  f"is_credit = %s AND delete_at IS NULL ORDER BY create_at ASC LIMIT 1;",
                                  [sale_date, is_credit])
                return my_cursor.fetchone()["create_at"]

    @staticmethod
    def get_sale_count_by_date(ca_date: date = date.today(), is_credit: bool = False, deleted: bool = False) -> float:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT COUNT(*) as sale_count FROM {Sale.table_name} WHERE date(create_at) = %s AND "
                                  f"is_credit = %s AND delete_at IS {'NOT' if deleted else ''} NULL;", [ca_date, is_credit])
                return my_cursor.fetchone()["sale_count"]

    @staticmethod
    def get_sale_product_count_by_date(ca_date: date = date.today(), is_credit: bool = False) -> float:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT SUM(sale_product.product_count) as sale_product_count FROM {Sale.table_name} "
                                  f"LEFT JOIN sale_product AS sale_product ON sale.id = sale_product.sale_id "
                                  f"WHERE date(create_at) = %s AND "
                                  f"is_credit = %s AND delete_at IS NULL;", [ca_date, is_credit])
                return my_cursor.fetchone()["sale_product_count"]

    @staticmethod
    def get_sale_search(sale_id: str, staff_name: str, client_name: str, page: int = 0, count: int = 20):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT {Sale.table_name}.id, {Sale.table_name}.is_paid, {Sale.table_name}.total, "
                                  f"{Sale.table_name}.client_id, {Sale.table_name}.staff_id, {Sale.table_name}.delete_at, "
                                  f"{Sale.table_name}.create_at, {Sale.table_name}.is_credit "
                                  f"FROM {Sale.table_name} "
                                  f"LEFT JOIN staff ON staff_id = {DBTableName.staff}.id "
                                  f"LEFT JOIN client ON client_id = {DBTableName.client}.id "
                                  f"WHERE {Sale.table_name}.id LIKE '{sale_id}%' OR staff.firstname LIKE '%{staff_name}%' "
                                  f"OR client.firstname LIKE '%{client_name}%' AND {Sale.table_name}.delete_at IS NULL "
                                  f"ORDER BY {Sale.table_name}.id DESC LIMIT %s OFFSET %s;",
                                  [count, page * count])
                results = my_cursor.fetchall()
                return [Sale.from_map(result) for result in results]

    def load_staff(self):
        if self.staff is not None:
            self.staff = self.staff.get_by_id(just_active=False)
        return self.staff

    def load_client(self):
        self.client = self.client.get_by_id(client_id=self.client.id) if self.client is not None else None
        return self.client

    def get_last(self):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {self.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return Sale.from_map(result)

    def get_last_id(self):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT id FROM {self.table_name} ORDER BY id DESC LIMIT 1;")
                result = my_cursor.fetchone()
                return result['id']

    def delete_permanently(self, sale_id: int = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} WHERE (`id` = %s);",
                                  [self.id if sale_id is None else sale_id])
                bd_connection.commit()
                return True

    def delete_last_permanently(self, limit: int = 1):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} ORDER BY id DESC LIMIT %s;", [limit])
                bd_connection.commit()
                return True



