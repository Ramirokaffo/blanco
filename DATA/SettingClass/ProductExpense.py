from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.ExpenseType import ExpenseType
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supply import Supply


class ProductExpense:
    def __init__(self, id: int = None, product_count: int = None, details: str = None, supply: Supply = None,
                 product_expense_reason: ExpenseType = None, saver_staff: Staff = None, daily: Daily = None):
        self.id = id
        self.product_count = product_count
        self.details = details
        self.supply = supply
        self.daily = daily
        self.saver_staff = saver_staff
        self.product_expense_reason = product_expense_reason
        self.table_name: str = DBTableName.product_expense

