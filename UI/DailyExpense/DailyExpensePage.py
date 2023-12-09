from tkinter import ttk, messagebox

from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.DailyExpense import DailyExpense
from DATA.SettingClass.ExpenseType import ExpenseType
from DATA.SettingClass.Staff import Staff
from STATIC.ConstantFile import *
from UI.DailyExpense.DailyExpenseForm import DailyExpenseForm
from UI.DailyExpense.DailyExpenseTable import DailyExpenseTable


class DailyExpensePage(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.main_frame = Frame(master, bg=couleur_sous_fenetre)
        self.main_frame.pack()
        self.control_displays = 0

        self.expense_table = DailyExpenseForm(self.main_frame)
        self.expense_table.pack(side=LEFT)

        self.expense_table = DailyExpenseTable(self.main_frame)
        self.expense_table.pack(side=RIGHT)
        self.expense_table.load_table_data()

