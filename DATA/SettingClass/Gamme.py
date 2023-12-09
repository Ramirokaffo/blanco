from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName


class Gamme:
    my_db = connect_to_db()
    table_name = DBTableName.gamme

    def __init__(self, id: int = None, name: str = None, description: str = None):
        self.id = id
        self.name = name
        self.description = description

    @staticmethod
    def get_by_id(category_id: int, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Gamme.table_name} WHERE id = %s AND delete_at IS NULL;",
                                  [category_id])
                result = my_cursor.fetchone()
                return Gamme.from_map(result) if not return_map else result

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Gamme.table_name} WHERE delete_at IS NULL;")
                return [Gamme.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, category_map):
        return None if not category_map else Gamme(id=category_map["id"], name=category_map["name"],
                                                      description=category_map["description"])

    @staticmethod
    def get_by_name(category_name: str, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Gamme.table_name} WHERE name = %s AND delete_at IS NULL;",
                                  [category_name])
                result = my_cursor.fetchone()
                return Gamme.from_map(result) if not return_map else result

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Gamme.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {Gamme.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return Gamme.from_map(result) if not return_map else result

    @staticmethod
    def create(name: str, description: str = None) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"INSERT INTO {Gamme.table_name} (name, description) VALUES (%s, %s);",
                                  [name, description])
                bd_connection.commit()
            return my_cursor.lastrowid

    def save_to_db(self):
        return Gamme.create(name=self.name, description=self.description)

