from datetime import datetime

from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName


class ExpenseType:
    table_name: str = DBTableName.expense_type

    def __init__(self, id: int = None, name: str = None, description: str = None, delete_at: datetime = None,
                 create_at: datetime = None):
        self.id = id
        self.name = name
        self.description = description
        self.delete_at = delete_at
        self.create_at = create_at

    def get_by_id(self, line_id, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s AND delete_at IS NULL;",
                                  [line_id])
                result = my_cursor.fetchone()
                return ExpenseType.from_map(result) if not return_map else result

    def get_all(self, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE delete_at IS NULL;")
                return [ExpenseType.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else ExpenseType(id=data_map.get("id"), name=data_map.get("name"),
                                                     description=data_map.get("description"))

    def get_by_name(self, name_value, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = %s AND delete_at IS NULL;",
                                  [name_value])
                result = my_cursor.fetchone()
                return ExpenseType.from_map(result) if not return_map else result

    def get_last(self, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {self.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return ExpenseType.from_map(result) if not return_map else result

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"INSERT INTO {self.table_name} (name, description) VALUES (%s, %s);",
                              [self.name, self.description])
                bd_connection.commit()
                return my_cursor.lastrowid
