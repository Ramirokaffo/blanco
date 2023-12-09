from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre
from UI.DailyInventory.DailyInventoryForm import DailyInventoryForm
from UI.DailyInventory.DailyInventoryTable import DailyInventoryTable


class DailyInventoryPage(Frame):

    def __init__(self, master, background=couleur_sous_fenetre):
        super().__init__(master)
        self.configure(background=background)
        self.daily_inventory_form = DailyInventoryForm(self)
        self.daily_inventory_form.pack(side=LEFT, anchor=N)

        self.daily_inventory_table = DailyInventoryTable(self)
        self.daily_inventory_table.pack(side=RIGHT)
        self.daily_inventory_table.load_table_data()


