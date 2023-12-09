from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Staff import Staff
from datetime import datetime


class Inventory:
    table_name: str = DBTableName.inventory

    def __init__(self, id: int = None, valid_product_count: int = None, invalid_product_count: int = None,
                 saver_staff: Staff = None, product: Product = None, create_at: datetime = None,
                 delete_at: datetime = None, exercise: Exercise = None):
        self.id = id
        self.valid_product_count = valid_product_count
        self.invalid_product_count = invalid_product_count
        self.product = product
        self.exercise = exercise
        self.saver_staff = saver_staff
        self.create_at = create_at
        self.delete_at = delete_at

    def save_to_db(self):
        bd_connection = connect_to_db()
        with bd_connection.cursor(dictionary=True) as my_cursor:
            my_cursor.execute(
                f"INSERT INTO {Inventory.table_name} (valid_product_count, invalid_product_count, "
                f"staff_id, product_id, exercise_id) VALUES (%s, %s, %s, %s, %s);",
                [self.valid_product_count, self.valid_product_count if self.invalid_product_count is None
                else self.invalid_product_count, self.saver_staff.id, self.product.id, self.exercise.id])
            bd_connection.commit()
            return my_cursor.lastrowid

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else Inventory(id=data_map.get("id"),
                                                   valid_product_count=data_map.get("valid_product_count"),
                                                   invalid_product_count=data_map.get("invalid_product_count"),
                                                   create_at=data_map.get("create_at"),
                                                   delete_at=data_map.get("delete_at"),
                                                   saver_staff=Staff(id=data_map.get("staff_id")),
                                                   exercise=Exercise(id=data_map.get("exercise_id")),
                                                   product=Product(id=data_map.get("product_id")))

    @staticmethod
    def get_by_id(id: int = None, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT * FROM {Inventory.table_name} WHERE id = %s;",
                    [id])
                result = my_cursor.fetchone()
                return Inventory.from_map(result) if not return_map else result

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT * FROM {Inventory.table_name} ORDER BY id DESC LIMIT 1;")
                result = my_cursor.fetchone()
                return Inventory.from_map(result) if not return_map else result
