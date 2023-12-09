from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName


class GrammageType:
    my_db = connect_to_db()
    table_name: str = DBTableName.grammage_type

    def __init__(self, id: int = None, name: str = None, description: str = None):
        self.id = id
        self.name = name
        self.description = description

    @staticmethod
    def get_by_id(category_id: int, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {GrammageType.table_name} WHERE id = %s AND delete_at IS NULL;",
                                  [category_id])
                result = my_cursor.fetchone()
                return GrammageType.from_map(result) if not return_map else result

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {GrammageType.table_name} WHERE delete_at IS NULL;")
                return [GrammageType.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, category_map: dict):
        return None if not category_map else GrammageType(id=category_map.get("id"), name=category_map.get("name"),
                                                   description=category_map.get("description"))

    @staticmethod
    def get_by_name(category_name: str, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {GrammageType.table_name} WHERE name = %s AND delete_at IS NULL;",
                                  [category_name])
                result = my_cursor.fetchone()
                return GrammageType.from_map(result) if not return_map else result

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {GrammageType.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {GrammageType.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return GrammageType.from_map(result) if not return_map else result

    @staticmethod
    def create(name: str, description: str = None) -> int:
        return GrammageType(name=name, description=description).save_to_db()

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"INSERT INTO {GrammageType.table_name} (name, description) VALUES (%s, %s);",
                                  [self.name, self.description])
                bd_connection.commit()
            return my_cursor.lastrowid

