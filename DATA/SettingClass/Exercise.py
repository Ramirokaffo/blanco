from datetime import datetime

from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName


class Exercise:
    my_db = connect_to_db()
    table_name: str = DBTableName.exercise
    current_exercise = None

    def __init__(self, id: int = None, start_date: datetime = None, end_date: datetime = None):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def get_by_id(id, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Exercise.table_name} WHERE id = %s;", [id])
                result = my_cursor.fetchone()
                return Exercise.from_map(result) if not return_map else result

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Exercise.table_name};")
                return [Exercise.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else Exercise(id=data_map.get("id"), start_date=data_map.get("start_date"),
                                                  end_date=data_map.get("end_date"))

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Exercise.table_name} ORDER BY id DESC LIMIT 1;")
                result = my_cursor.fetchone()
                return Exercise.from_map(result) if not return_map else result

    def save_to_db(self):
        return Exercise.create(start_date=self.start_date, end_date=self.end_date)

    @staticmethod
    def create(start_date: datetime, end_date: datetime = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"INSERT INTO {Exercise.table_name} (start_date, end_date) VALUES (%s, %s);",
                                  [start_date, end_date])
                bd_connection.commit()
                return my_cursor.lastrowid

    @staticmethod
    def get_current_exercise(return_map: bool = False):
        if Exercise.current_exercise is None:
            expected_last_exercise = Exercise.get_last(return_map=return_map)
            if expected_last_exercise is None:
                exercise_id = Exercise.create(start_date=datetime.today())
                return Exercise.get_by_id(id=exercise_id)
            return expected_last_exercise
        return Exercise.current_exercise


