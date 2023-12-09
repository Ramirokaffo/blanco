from datetime import datetime

from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.BaseUser import BaseUser
from DATA.DataBase.DBManager import connect_to_db


class Supplier(BaseUser):
    my_db = connect_to_db()
    table_name: str = DBTableName.supplier

    def __init__(self, id: int = None, firstname: str = None, lastname: str = None, phone_number: str = None,
                 email: str = None, gender: str = None, delete_at: datetime = None, create_at: datetime = None):
        super().__init__(id, firstname, lastname, phone_number, create_at, delete_at, email)
        self.gender = gender
        self.delete_at = delete_at
        self.create_at = create_at
        self.table_name = DBTableName.supplier

    def save_to_db(self):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute("INSERT INTO %s (firstname, lastname, phone_number, email, gender) "
                          "VALUES (%s, %s, %s, %s, %s);", [self.table_name, self.firstname, self.lastname,
                                                           self.phone_number, self.email, self.gender])
                return my_cursor.lastrowid

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f'''SELECT * FROM {Supplier.table_name} WHERE delete_at IS NULL;''')
                return [Supplier.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, staff_map: dict):
        return None if staff_map is None else Supplier(
            id=staff_map.get("id"),
            lastname=staff_map.get("lastname"),
            firstname=staff_map.get("firstname"),
            email=staff_map.get("email"),
            gender=staff_map.get("gender"),
            create_at=staff_map.get("create_at"),
            delete_at=staff_map.get("delete_at"),
            phone_number=staff_map.get("phone_number"))

