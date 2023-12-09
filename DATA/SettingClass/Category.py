from datetime import datetime

from DATA.DataBase.DBTableName import DBTableName
from DATA.DataBase.DBManager import connect_to_db


class Category:
    table_name = DBTableName.category

    def __init__(self, id: int = None, name: str = None, description: str = None, delete_at: datetime = None,
                 create_at: datetime = None):
        self.id = id
        self.name = name
        self.description = description
        self.delete_at = delete_at
        self.create_at = create_at

    @staticmethod
    def get_by_id(category_id, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Category.table_name} WHERE id = %s AND delete_at IS NULL;",
                                  [category_id])
                result = my_cursor.fetchone()
                return Category.from_map(result) if not return_map else result

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Category.table_name} WHERE delete_at IS NULL;")
                return [Category.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, category_map: dict):
        return None if not category_map else Category(id=category_map.get("id"), name=category_map.get("name"),
                                                      description=category_map.get("description"))

    @staticmethod
    def get_by_name(category_name, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Category.table_name} WHERE name = %s AND delete_at IS NULL;",
                                  [category_name])
                result = my_cursor.fetchone()
                return Category.from_map(result) if not return_map else result

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Category.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {Category.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return Category.from_map(result) if not return_map else result

    @staticmethod
    def create(name: str, description: str = None) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"INSERT INTO {Category.table_name} (name, description) VALUES (%s, %s);",
                              [name, description])
                bd_connection.commit()
                return my_cursor.lastrowid

    def save_to_db(self) -> int:
        return Category.create(name=self.name, description=self.description)



