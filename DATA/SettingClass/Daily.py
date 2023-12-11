
from datetime import datetime

from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Exercise import Exercise


class Daily:
    my_db = connect_to_db()
    table_name: str = DBTableName.daily
    current_daily = None

    def __init__(self, id: int = None, start_date: datetime = None, end_date: datetime = None, exercise: Exercise = None):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.exercise = exercise

    @staticmethod
    def get_by_id(id, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Daily.table_name} WHERE id = %s;", [id])
                result = my_cursor.fetchone()
                return Daily.from_map(result) if not return_map else result

    @staticmethod
    def get_under_id(id, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Daily.table_name} WHERE id < %s LIMIT 1;", [id])
                result = my_cursor.fetchone()
                return Daily.from_map(result) if not return_map else result

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Daily.table_name};")
                return [Daily.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else Daily(id=data_map.get("id"), start_date=data_map.get("start_date"),
                                                  end_date=data_map.get("end_date"),
                                               exercise=Exercise(id=data_map.get("exercise_id")))

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Daily.table_name} ORDER BY id DESC LIMIT 1;")
                result = my_cursor.fetchone()
                return Daily.from_map(result) if not return_map else result

    def save_to_db(self):
        return Daily.create(start_date=self.start_date, end_date=self.end_date, exercise=self.exercise)

    @staticmethod
    def create(start_date: datetime = datetime.now(), exercise: Exercise = Exercise.get_current_exercise(), end_date: datetime = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"INSERT INTO {Daily.table_name} (start_date, end_date, exercise_id) VALUES (%s, %s, %s);",
                                  [start_date, end_date, exercise.id])
                bd_connection.commit()
                return my_cursor.lastrowid

    def close_daily(self):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"UPDATE {Daily.table_name} SET end_date = %s WHERE id = %s;",
                                  [datetime.now(), self.id])
                bd_connection.commit()
                return my_cursor.lastrowid

    @staticmethod
    def get_current_daily(return_map: bool = False):
        if Daily.current_daily is None:
            expected_last_daily = Daily.get_last(return_map=return_map)
            if expected_last_daily is None:
                daily_id = Daily.create(start_date=datetime.today())
                Daily.current_daily = Daily.get_by_id(id=daily_id)
                return Daily.current_daily
            else:
                if expected_last_daily.end_date is not None:
                    daily_id = Daily.create(start_date=datetime.today())
                    Daily.current_daily = Daily.get_by_id(id=daily_id)
                    return Daily.current_daily
                else:
                    Daily.current_daily = expected_last_daily
                    return expected_last_daily
        return Daily.current_daily


