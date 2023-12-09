
from datetime import datetime, date

from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.RecipeType import RecipeType
from DATA.SettingClass.Staff import Staff


class DailyRecipe:
    table_name = DBTableName.daily_recipe

    def __init__(self, id: int = None, amount: float = None, description: str = None, staff: Staff = None,
                 recipe_type: RecipeType = None, delete_at: datetime = None, create_at: datetime = None,
                 daily: Daily = None):
        self.id = id
        self.amount = amount
        self.recipe_type = recipe_type
        self.staff = staff
        self.daily = daily
        self.delete_at = delete_at
        self.create_at = create_at
        self.description = description
        self.my_map = {}

    @staticmethod
    def get_by_id(daily_expense_id: int, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {DailyRecipe.table_name} WHERE id = %s AND delete_at IS NULL;",
                                  [daily_expense_id])
                result = my_cursor.fetchone()
                return DailyRecipe.from_map(result) if not return_map else result

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {DailyRecipe.table_name} WHERE delete_at IS NULL;")
                return [DailyRecipe.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else DailyRecipe(id=data_map.get("id"), amount=data_map.get("amount"),
                                                     description=data_map.get("description"),
                                                     staff=Staff(id=data_map.get("staff_id")),
                                                     daily=Daily(id=data_map.get("daily_id")),
                                                     create_at=data_map.get("create_at"),
                                                     delete_at=data_map.get("delete_at"),
                                                     recipe_type=RecipeType(id=data_map.get("recipe_type_id")))

    @staticmethod
    def get_by_column_name(column_name: str, value, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {DailyRecipe.table_name} WHERE {column_name} = %s AND delete_at IS NULL;",
                                  [value])
                return [DailyRecipe.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {DailyRecipe.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {DailyRecipe.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return DailyRecipe.from_map(result) if not return_map else result

    @staticmethod
    def get_daily_recipe_amount_by_date(ca_date: date = date.today()) -> float:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT SUM(amount) AS total FROM {DailyRecipe.table_name} WHERE date(create_at) = %s AND "
                                  f'''delete_at IS NULL;''', [ca_date])
                return my_cursor.fetchone()["total"]

    @staticmethod
    def get_daily_recipe_amount_by_daily(daily_id: int = Daily.get_current_daily().id) -> float:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT SUM(amount) AS total FROM {DailyRecipe.table_name} WHERE daily_id = %s AND "
                                  f'''delete_at IS NULL;''', [daily_id])
                return my_cursor.fetchone()["total"]

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"INSERT INTO {DailyRecipe.table_name} (amount, description, staff_id, recipe_type_id, daily_id) "
                                  f"VALUES (%s, %s, %s, %s, %s);",
                                  [self.amount, self.description, self.staff.id, self.recipe_type.id, self.daily.id])
                bd_connection.commit()
                return my_cursor.lastrowid

    def load_raison(self, return_map: bool = False) -> RecipeType | dict:
        if not return_map:
            self.recipe_type = RecipeType().get_by_id(line_id=self.recipe_type.id)
            return self.recipe_type
        self.my_map[DBTableName.recipe_type] = RecipeType().get_by_id(line_id=self.recipe_type.id, return_map=return_map)
        return self.my_map[DBTableName.recipe_type]

    def load_staff(self, return_map: bool = False) -> Staff | dict:
        if not return_map:
            self.staff = Staff().get_by_id(line_id=self.staff.id)
            return self.staff
        self.my_map[DBTableName.staff] = Staff().get_by_id(line_id=self.recipe_type.id, return_map=return_map)
        return self.my_map[DBTableName.staff]



