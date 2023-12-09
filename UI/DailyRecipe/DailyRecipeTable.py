
from tkinter import *
from tkinter import ttk

from DATA.SettingClass.DailyRecipe import DailyRecipe
from STATIC.ConstantFile import couleur_sous_fenetre, couleur_label, couleur_inverse_tree
from Service.DateTimeService import DateTimeService


class DailyRecipeTable(Frame):
    table_list = []

    def __init__(self, master):
        super().__init__(master)
        self.is_shown = False
        DailyRecipeTable.table_list.append(self)
        self.main_frame = Frame(self, bg=couleur_sous_fenetre)
        self.main_frame.pack(side=RIGHT, fill=Y)

        self.separator = ttk.Separator(self, orient=VERTICAL)
        self.separator.pack(fill=Y, side=RIGHT, padx=0)

        self.scroll_bar_y = Scrollbar(self.main_frame, orient=VERTICAL)
        self.scroll_bar_y.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x = Scrollbar(self.main_frame, orient=HORIZONTAL)
        self.scroll_bar_x.pack(side=BOTTOM, fill=X)

        self.table = ttk.Treeview(self.main_frame, columns=("1", "2", "3", "4", "5"),
                                  yscrollcommand=self.scroll_bar_y.set,
                                  xscrollcommand=self.scroll_bar_x.set,
                                  show="headings", style="mystyle.Treeview", height=26)

        self.table.heading("1", text="Type", anchor=W)
        self.table.heading("2", text="Montant", anchor=W)
        self.table.heading("3", text="Auteur", anchor=E)
        self.table.heading("4", text="Date", anchor=CENTER)
        self.table.heading("5", text="Description", anchor=W)

        self.table.column("1", width=180, anchor=W)
        self.table.column("2", width=90, anchor=W)
        self.table.column("3", width=120, anchor=E)
        self.table.column("4", width=120, anchor=CENTER)
        self.table.column("5", width=400, anchor=W)

        self.table.pack(expand=YES)

        self.scroll_bar_x.configure(command=self.table.xview)
        self.scroll_bar_y.configure(command=self.table.yview)

        self.table.bind("<ButtonRelease-3>", self.show_popup)

        self.bind("<Expose>", self.on_expose)
        self.bind("<Unmap>", self.on_hide)

    def on_expose(self, event):
        self.is_shown = True

    def on_hide(self, event):
        self.is_shown = False

    @staticmethod
    def reload_all_table():
        if len(DailyRecipeTable.table_list) > 0:
            table: DailyRecipeTable
            for table in DailyRecipeTable.table_list:
                if table.winfo_exists():
                    table.load_table_data()

    def get_selected_item_id(self):
        dep_select = self.table.selection()
        if dep_select[0]:
            ligne_dep_select = self.table.item(dep_select[0])
            value_dep_select = ligne_dep_select["values"]
            return value_dep_select[-1]

    def show_popup(self, event):
        if self.get_selected_item_id():
            menu_popup_action_depense = Menu(self.table, tearoff=0,
                                             title="Action sur les dépenses enregistrees")
            menu_popup_action_depense.add_command(label=f"Dupliquer la recette",
                                                  command=self.dupplicate_depense)
            x, y = self.master.winfo_pointerxy()
            menu_popup_action_depense.tk_popup(x, y)

    def dupplicate_depense(self):
        dep_select = self.table.selection()
        if dep_select[0]:
            ligne_dep_select = self.table.item(dep_select[0])
            # value_dep_select = ligne_dep_select["values"]
            # self.type_vente_champs.delete(0, END)
            # self.type_vente_champs.insert(0, value_dep_select[0])
            # self.montant_depense_champs.delete(0, END)
            # self.montant_depense_champs.insert(0, value_dep_select[1])
            # self.description_depense_champs.delete("0.0", END)
            # self.description_depense_champs.insert("0.0", value_dep_select[2])
            # self.save_depense()

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)

    def load_table_data(self):
        self.clear_table()
        daily_recipe: DailyRecipe
        for i, daily_recipe in enumerate(DailyRecipe().get_all()):
            daily_recipe.load_staff()
            daily_recipe.load_raison()
            self.table.insert("", index=END, id=str(i), values=[daily_recipe.recipe_type.name, daily_recipe.amount,
                                                                daily_recipe.staff.get_all_name(),
                                                                DateTimeService.format_date_time(daily_recipe.create_at),
                                                                daily_recipe.description
                                                                ], tags=("even" if i % 2 == 0 else "odd",))
        self.table.tag_configure("even", background=couleur_label)
        self.table.tag_configure("odd", background=couleur_inverse_tree)

    def displays(self):
        self.pack(expand=YES)
        return self.master




