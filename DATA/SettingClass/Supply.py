from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supplier import Supplier
from datetime import datetime, date


class Supply:
    table_name: str = DBTableName.supply

    def __init__(self, id: int = None, product_count: int = None, product_count_rest: int = None,
                 unit_coast: float = None, unit_price: float = None, supplier: Supplier = None,
                 saver_staff: Staff = None, product: Product = None, create_at: datetime = None,
                 delete_at: datetime = None, expiration_date: date = None, daily: Daily = None):
        self.id = id
        self.product_count = product_count
        self.product_count_rest = product_count_rest
        self.unit_coast = unit_coast
        self.unit_price = unit_price
        self.supplier = supplier
        self.product = product
        self.saver_staff = saver_staff
        self.table_name = DBTableName.supply
        self.create_at = create_at
        self.delete_at = delete_at
        self.daily = daily
        self.expiration_date = expiration_date

    def save_to_db(self):
        bd_connection = connect_to_db()
        with bd_connection.cursor(dictionary=True) as my_cursor:
            my_cursor.execute(
                f"INSERT INTO {self.table_name} (product_count, product_count_rest, unit_coast, unit_price, "
                f"supplier_id, staff_id, product_id, daily_id, expiration_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                [self.product_count, self.product_count if not self.product_count_rest else self.product_count_rest,
                 0 if not self.unit_coast else self.unit_coast, 0 if not self.unit_price else self.unit_price,
                 None if self.supplier is None else self.supplier.id, self.saver_staff.id, self.product.id,
                 self.daily.id if self.daily is not None else Daily.get_current_daily().id, self.expiration_date])
            bd_connection.commit()
            return my_cursor.lastrowid

    def reduce_product_rest(self, to_reduce: int):
        bd_connection = connect_to_db()
        with bd_connection.cursor(dictionary=True) as my_cursor:
            my_cursor.execute(
            f"UPDATE {self.table_name} SET product_count_rest = %s WHERE (id = %s);",
            [self.product_count_rest - to_reduce, self.id])
            return bd_connection

    def reduce_many_product_rest(self, list_rest_id: []):
        bd_connection = connect_to_db()
        with bd_connection.cursor(dictionary=True) as my_cursor:
            my_cursor.executemany(
                f"UPDATE {self.table_name} SET product_count_rest = %s WHERE (id = %s);", list_rest_id)
            return bd_connection


    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else Supply(id=data_map["id"], product_count=data_map["product_count"],
                                                product_count_rest=data_map["product_count_rest"],
                                                unit_coast=data_map["unit_coast"],
                                                unit_price=data_map["unit_price"],
                                                create_at=data_map["create_at"],
                                                delete_at=data_map["delete_at"],
                                                expiration_date=data_map["expiration_date"],
                                                supplier=Supplier(id=data_map["supplier_id"]),
                                                saver_staff=Staff(id=data_map["staff_id"]),
                                                daily=Daily(id=data_map["daily_id"]),
                                                product=Product(id=data_map["product_id"]))

    def find_right_product_supply(self, product_id: int):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE product_count_rest != '0' AND product_id = %s AND delete_at "
                f"IS NULL ORDER BY create_at ASC LIMIT 1;",
                [product_id])
                return Supply.from_map(my_cursor.fetchone())

    @staticmethod
    def find_product_supply(product_id: int, count: int = 50, page: int = 0, return_map: bool = False,
                            order_column: str = "create_at", order: str = "DESC"):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f"SELECT * FROM {Supply.table_name} WHERE product_id = %s AND delete_at "
                f"IS NULL ORDER BY {order_column} {order} "
                f"LIMIT %s OFFSET %s;", [product_id, count, count * page])
                return [Supply.from_map(supply) if not return_map else supply for supply in my_cursor.fetchall()]

    def get_by_id(self, supply_id: int = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE id = %s;",
                [self.id if supply_id is None else supply_id])
                return Supply.from_map(my_cursor.fetchone())

    def find_product_supply_with_stock(self, product_id: int):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE product_count_rest != '0' AND product_id = %s AND delete_at "
                f"IS NULL ORDER BY create_at ASC;",
                [product_id])
                return [Supply.from_map(supply) for supply in my_cursor.fetchall()]

    @staticmethod
    def get_supply_with_date_critic(count: int = 50, page: int = 0, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f"SELECT * FROM {Supply.table_name} LEFT JOIN (SELECT {Product.table_name}.id, {Product.table_name}.name, "
                f"{Product.table_name}.exp_alert_period AS exp_limit FROM {Product.table_name}) as product ON "
                f"{Supply.table_name}.product_id = {Product.table_name}.id WHERE ((current_date() + interval "
                                  f"{Product.table_name}.exp_limit month)  > "
                f"{Supply.table_name}.expiration_date) AND {Supply.table_name}.product_count_rest != '0' AND delete_at "
                f"IS NULL ORDER BY {Supply.table_name}.create_at ASC "
                f"LIMIT %s OFFSET %s;", [count, count * page])
                return [Supply.from_map(supply) if not return_map else supply for supply in my_cursor.fetchall()]

    def load_product(self):
        self.product = Product().get_by_id(product_id=self.product.id)
        return self.product

    def delete_last_permanently(self, limit: int = 1):
        try:
            with connect_to_db() as bd_connection:
                with bd_connection.cursor(dictionary=True) as my_cursor:
                    my_cursor.execute(f"DELETE FROM {self.table_name} ORDER BY id DESC LIMIT %s;", [limit])
                    bd_connection.commit()
                    return True
        except:
            return False

