from datetime import datetime

from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.BaseUser import BaseUser
from DATA.DataBase.DBManager import connect_to_db


class Client(BaseUser):
    my_db = connect_to_db()
    table_name: str = DBTableName.client

    def __init__(self, id: int = None, firstname: str = None, lastname: str = None, phone_number: str = None,
                 email: str = None, gender: str = None, delete_at: datetime = None, create_at: datetime = None):
        super().__init__(id, firstname, lastname, phone_number, create_at, delete_at, email)
        self.gender = gender
        self.delete_at = delete_at
        self.create_at = create_at

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"INSERT INTO {self.table_name} (firstname, lastname, phone_number, email, gender) "
                          "VALUES (%s, %s, %s, %s, %s);", [self.firstname, self.lastname,
                                                           self.phone_number, self.email, self.gender])
                bd_connection.commit()
                return my_cursor.lastrowid

    @classmethod
    def from_map(cls, staff_map: dict):
        return None if staff_map is None else Client(
            id=staff_map.get('id'),
            lastname=staff_map.get('lastname'),
            firstname=staff_map.get('firstname'),
            email=staff_map.get('email'),
            gender=staff_map.get('gender'),
            phone_number=staff_map.get('phone_number'))

    @staticmethod
    def get_by_id(client_id: int):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f"SELECT * FROM {Client.table_name} WHERE id = %s;",
                [client_id])
                return Client.from_map(my_cursor.fetchone())

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
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Client.table_name} WHERE delete_at IS NULL;")
                return [Client.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @staticmethod
    def delete_by_id_permanently(id: int = 1):
        try:
            with connect_to_db() as bd_connection:
                with bd_connection.cursor(dictionary=True) as my_cursor:
                    my_cursor.execute(f"DELETE FROM {Client.table_name} WHERE id = %s;", [id])
                    bd_connection.commit()
                    return True
        except:
            return False
