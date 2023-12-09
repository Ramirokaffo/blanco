
from tkinter import *
from tkinter import ttk

from DATA.SettingClass.DailyExpense import DailyExpense
from DATA.SettingClass.DailyInventory import DailyInventory
from STATIC.ConstantFile import couleur_sous_fenetre, couleur_label, couleur_inverse_tree
from Service.DateTimeService import DateTimeService


class DailyInventoryTable(Frame):
    table_list: list = []

    def __init__(self, master):
        super().__init__(master)
        self.main_frame = Frame(self, bg=couleur_sous_fenetre)
        self.main_frame.pack(side=RIGHT, fill=Y)
        DailyInventoryTable.table_list.append(self)
        self.separator = ttk.Separator(self, orient=VERTICAL)
        self.separator.pack(fill=Y, side=RIGHT, padx=0)

        self.scroll_bar_y = Scrollbar(self.main_frame, orient=VERTICAL)
        self.scroll_bar_y.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x = Scrollbar(self.main_frame, orient=HORIZONTAL)
        self.scroll_bar_x.pack(side=BOTTOM, fill=X)

        self.table = ttk.Treeview(self.main_frame, columns=list(str(i) for i in range(1, 8)),
                                  yscrollcommand=self.scroll_bar_y.set,
                                  xscrollcommand=self.scroll_bar_x.set,
                                  show="headings", style="mystyle.Treeview", height=26)

        self.table.heading("1", text="Montant cash", anchor=W)
        self.table.heading("2", text="Fond de caisse", anchor=W)
        self.table.heading("3", text="Recette journalière", anchor=W)
        self.table.heading("4", text="Dépenses journalières", anchor=W)
        self.table.heading("5", text="Autres recettes", anchor=W)
        self.table.heading("6", text="Date", anchor=CENTER)
        self.table.heading("7", text="Auteur", anchor=E)

        self.table.column("1", width=100, anchor=W)
        self.table.column("2", width=100, anchor=W)
        self.table.column("3", width=100, anchor=W)
        self.table.column("4", width=120, anchor=W)
        self.table.column("5", width=100, anchor=W)
        self.table.column("6", width=150, anchor=CENTER)
        self.table.column("7", width=150, anchor=E)

        self.table.pack(expand=YES)

        self.scroll_bar_x.configure(command=self.table.xview)
        self.scroll_bar_y.configure(command=self.table.yview)

        self.table.bind("<ButtonRelease-3>", self.show_popup_depense)

    def get_selected_depense_id(self):
        dep_select = self.table.selection()
        if dep_select[0]:
            ligne_dep_select = self.table.item(dep_select[0])
            value_dep_select = ligne_dep_select["values"]
            return value_dep_select[-1]

    def show_popup_depense(self, event):
        if self.get_selected_depense_id():
            menu_popup_action_depense = Menu(self.table, tearoff=0,
                                             title="Action sur les dépenses enregistrees")
            # menu_popup_action_depense.add_command(label=f"Dupliquer la depense",
            #                                       command=self.dupplicate_depense)
            x, y = self.master.winfo_pointerxy()
            menu_popup_action_depense.tk_popup(x, y)

    @staticmethod
    def reload_all_table():
        if len(DailyInventoryTable.table_list) > 0:
            table: DailyInventoryTable
            for table in DailyInventoryTable.table_list:
                if table.winfo_exists():
                    table.load_table_data()

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)

    def load_table_data(self):
        self.clear_table()
        daily_inventory: DailyInventory
        for i, daily_inventory in enumerate(DailyInventory.get_all()):
            daily_inventory.load_staff()
            self.table.insert("", index=END, id=str(i), values=[daily_inventory.cash_amount,
                                                                daily_inventory.cash_float,
                                                                daily_inventory.daily_recipe_amount,
                                                                daily_inventory.daily_expense_amount,
                                                                daily_inventory.other_recipe_amount,
                                                                daily_inventory.create_at,
                                                                daily_inventory.saver_staff.get_all_name() if \
                                                                daily_inventory.saver_staff is not None else "Aucun",
                                                                ], tags=("even" if i % 2 == 0 else "odd",))
        self.table.tag_configure("even", background=couleur_label)
        self.table.tag_configure("odd", background=couleur_inverse_tree)



