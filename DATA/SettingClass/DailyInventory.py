
from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Staff import Staff
from datetime import datetime


class DailyInventory:
    table_name: str = DBTableName.daily_inventory
    left_join_sql = f"LEFT JOIN (SELECT SUM({DBTableName.sale}.total) AS sale_recipe_amount, " \
                         f"{DBTableName.sale}.daily_id FROM {DBTableName.sale} WHERE " \
                         f"{DBTableName.sale}.delete_at IS NULL GROUP BY {DBTableName.sale}.daily_id) as " \
                         f"{DBTableName.sale} ON {table_name}.daily_id = " \
                         f"{DBTableName.sale}.daily_id " \
                         f"LEFT JOIN (SELECT SUM({DBTableName.daily_recipe}.amount) AS daily_recipe_amount, " \
                         f"{DBTableName.daily_recipe}.daily_id FROM {DBTableName.daily_recipe} WHERE " \
                         f"{DBTableName.daily_recipe}.delete_at IS NULL GROUP BY {DBTableName.daily_recipe}.daily_id) as " \
                         f"{DBTableName.daily_recipe} ON {table_name}.daily_id = " \
                         f"{DBTableName.daily_recipe}.daily_id " \
                         f"LEFT JOIN (SELECT SUM({DBTableName.daily_expense}.amount) AS daily_expense_amount, " \
                         f"{DBTableName.daily_expense}.daily_id FROM {DBTableName.daily_expense} WHERE " \
                         f"{DBTableName.daily_expense}.delete_at IS NULL GROUP BY {DBTableName.daily_expense}.daily_id) as " \
                         f"{DBTableName.daily_expense} ON {table_name}.daily_id = " \
                         f"{DBTableName.daily_expense}.daily_id "

    def __init__(self, id: int = None, cash_amount: float = None, cash_float: float = None,
                 daily_expense_amount: float = None, daily_recipe_amount: float = None,
                 sale_recipe_amount: float = None,
                 saver_staff: Staff = None, create_at: datetime = None,
                 delete_at: datetime = None, daily: Daily = None):
        self.id = id
        self.cash_amount = cash_amount
        self.cash_float = cash_float
        self.daily_expense_amount = daily_expense_amount
        self.daily_recipe_amount = daily_recipe_amount
        self.sale_recipe_amount = sale_recipe_amount
        self.daily = daily
        self.saver_staff = saver_staff
        self.create_at = create_at
        self.delete_at = delete_at

    def save_to_db(self):
        bd_connection = connect_to_db()
        with bd_connection.cursor(dictionary=True) as my_cursor:
            my_cursor.execute(
                f"INSERT INTO {DailyInventory.table_name} (cash_amount, cash_float, "
                f"staff_id, daily_id) VALUES (%s, %s, %s, %s);",
                [self.cash_amount, self.cash_amount if self.cash_float is None
                else self.cash_float, self.saver_staff.id, self.daily.id])
            bd_connection.commit()
            return my_cursor.lastrowid

    @classmethod
    def from_map(cls, data_map: dict):
        return None if not data_map else DailyInventory(id=data_map.get("id"),
                                                        cash_amount=data_map.get("cash_amount"),
                                                        cash_float=data_map.get("cash_float"),
                                                        sale_recipe_amount=data_map.get("sale_recipe_amount"),
                                                        daily_expense_amount=data_map.get("daily_expense_amount"),
                                                        daily_recipe_amount=data_map.get("daily_recipe_amount"),
                                                        create_at=data_map.get("create_at"),
                                                        delete_at=data_map.get("delete_at"),
                                                        saver_staff=Staff(id=data_map.get("staff_id")),
                                                        daily=Daily(id=data_map.get("daily_id")))

    @staticmethod
    def get_by_id(id: int = None, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT * FROM {DailyInventory.table_name} {DailyInventory.left_join_sql} WHERE id = %s;", [id])
                result = my_cursor.fetchone()
                return DailyInventory.from_map(result) if not return_map else result

    @staticmethod
    def get_last(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT * FROM {DailyInventory.table_name} {DailyInventory.left_join_sql} ORDER BY id DESC LIMIT 1;")
                result = my_cursor.fetchone()
                return DailyInventory.from_map(result) if not return_map else result

    @staticmethod
    def get_all(return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {DailyInventory.table_name} " + DailyInventory.left_join_sql + \
                                  f"WHERE {DailyInventory.table_name}.delete_at IS NULL;")

                return [DailyInventory.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    def load_staff(self):
        if self.saver_staff is not None:
            self.saver_staff = self.saver_staff.get_by_id(just_active=False)
        return self.saver_staff
