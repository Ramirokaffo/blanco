
from tkinter import *
from tkinter import ttk, messagebox

from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.DailyExpense import DailyExpense
from DATA.SettingClass.DailyInventory import DailyInventory
from DATA.SettingClass.DailyRecipe import DailyRecipe
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Sale import Sale
from DATA.SettingClass.Staff import Staff
from STATIC.ConstantFile import couleur_sous_fenetre, couleur_police_champs
from Service.AnyService import AnyService
from Service.InputCheckService import InputCheckService
from UI.DailyInventory.DailyInventoryTable import DailyInventoryTable


class DailyInventoryForm(Frame):
    form_list: list = []

    def __init__(self, master, relief=FLAT, padx=0, pady=0, avance_value: str = "", refund_value: str = ""):
        super().__init__(master)
        DailyInventoryForm.form_list.append(self)

        self.configure(background=couleur_sous_fenetre)
        self.input_check_service = InputCheckService(self.master)
        main_frame = Frame(self, background=couleur_sous_fenetre, relief=relief, borderwidth=1)
        main_frame.pack(expand=YES, padx=padx, pady=pady, ipady=5, ipadx=5)
        last_inventory = DailyInventory.get_last()
        daily_recipe = Sale.get_ca_by_daily()
        other_recipe = DailyRecipe.get_daily_recipe_amount_by_daily()
        daily_expense = DailyExpense.get_daily_expense_amount_by_daily()

        self.last_cash_float_var = StringVar(value=str(last_inventory.cash_float if last_inventory and last_inventory is not None else 0))
        self.daily_recipe_var = StringVar(value=str(daily_recipe if daily_recipe is not None else 0))
        self.daily_expense_var = StringVar(value=str(daily_expense if daily_expense is not None else 0))
        self.other_recipe_var = StringVar(value=str(other_recipe if other_recipe is not None else 0))
        self.difference_var = StringVar()
        on_cash_amount_change = self.register(self.on_cash_amount_change)

        Label(main_frame, text="Recette journalière", bg=couleur_sous_fenetre, width=30, anchor=W).grid(row=1, column=2, sticky=EW, pady=20, padx=5)
        Label(main_frame, textvariable=self.daily_recipe_var, bg=couleur_sous_fenetre, width=30, anchor=E, fg="green").grid(row=1, column=3, sticky=EW, pady=20, padx=5)

        Label(main_frame, text="Dépense journalière", background=couleur_sous_fenetre, width=30, anchor=W).grid(row=2, column=2, sticky=EW, pady=20, padx=5)
        Label(main_frame, textvariable=self.daily_expense_var, bg=couleur_sous_fenetre, fg="red", width=30, anchor=E).grid(row=2, column=3, sticky=EW, pady=20, padx=5)

        Label(main_frame, text="Autres Recettes", background=couleur_sous_fenetre, width=30, anchor=W).grid(row=3, column=2, sticky=EW, pady=20, padx=5)
        Label(main_frame, textvariable=self.other_recipe_var, bg=couleur_sous_fenetre, fg="green", width=30, anchor=E).grid(row=3, column=3, sticky=EW, pady=20, padx=5)

        Label(main_frame, text="Ancien fond de caisse", background=couleur_sous_fenetre, width=30, anchor=W).grid(row=4, column=2, sticky=EW, pady=20, padx=5)
        Label(main_frame, textvariable=self.last_cash_float_var, background=couleur_sous_fenetre, width=30, anchor=E, fg="green").grid(row=4, column=3, sticky=EW, pady=20, padx=5)

        Label(main_frame, text="Montant comptant", background=couleur_sous_fenetre, width=30, anchor=W).grid(row=5, column=2, sticky=EW, pady=20, padx=5)
        self.cash_amount_entry = Entry(main_frame, width=30, validate="key", fg="red", validatecommand=(on_cash_amount_change, "%S"))
        self.cash_amount_entry.insert(0, avance_value)
        self.cash_amount_entry.grid(row=5, column=3, sticky=EW, padx=5)
        ttk.Separator(main_frame, orient=HORIZONTAL).grid(row=6, column=2, columnspan=2, sticky=EW, padx=5)

        Label(main_frame, text="Difference", anchor=W, background=couleur_sous_fenetre).grid(row=7, column=2, pady=20, sticky=EW, padx=5)
        Label(main_frame, textvariable=self.difference_var, anchor=W, background=couleur_sous_fenetre).grid(row=7, column=3, pady=20, sticky=E, padx=5)
        self.new_cash_float_entry = Entry(main_frame, fg=couleur_police_champs, validate="key",
                                          validatecommand=(self.input_check_service.check_date, "%S", "%P"))
        for value in refund_value:
            self.new_cash_float_entry.insert(END, value)
        ttk.Separator(main_frame, orient=HORIZONTAL).grid(row=8, column=2, columnspan=2, sticky=EW, padx=5)

        Label(main_frame, text="Nouveau fond de caisse", anchor=W, background=couleur_sous_fenetre).grid(row=9, column=2, pady=20, sticky=EW, padx=5)
        self.new_cash_float_entry.grid(row=9, column=3, sticky=EW, padx=5)
        ttk.Separator(main_frame, orient=HORIZONTAL).grid(row=10, column=2, columnspan=2, sticky=EW, padx=5)

        Button(main_frame, text="Enregistrer", command=self.save, background=couleur_sous_fenetre).grid(row=11, column=2, sticky=EW, padx=5, columnspan=2, pady=20)
        # Button(main_frame, text="Annuler", command=self.abort).grid(row=10, column=3, sticky=EW, padx=5)
        self.winfo_toplevel().bind("<Return>", lambda x: self.save())
        self.bind("<FocusIn>", self.on_focus_in)
        self.focus_set()
        self.pack()
        self.update_difference()

    @staticmethod
    def reload_all_form():
        if len(DailyInventoryForm.form_list) > 0:
            table: DailyInventoryForm
            for table in DailyInventoryForm.form_list:
                if table.winfo_exists():
                    table.reload_form()

    def reload_form(self):
        dcf = DailyInventory.get_last()
        daily_recipe = Sale.get_ca_by_daily()
        other_recipe = DailyRecipe.get_daily_recipe_amount_by_daily()
        daily_expense = DailyExpense.get_daily_expense_amount_by_daily()
        self.last_cash_float_var.set(str(dcf.cash_float if dcf and dcf is not None else 0))
        self.daily_recipe_var.set(str(daily_recipe if daily_recipe is not None else 0))
        self.daily_expense_var.set(str(daily_expense if daily_expense is not None else 0))
        self.other_recipe_var.set(str(other_recipe if other_recipe is not None else 0))
        self.update_difference()

    def on_cash_amount_change(self, quoi):
        try:
            int(quoi)
            self.after(5, self.update_difference)
            return True
        except:
            if quoi == ".":
                self.after(5, self.update_difference)
                return True
            else:
                self.master.bell()
                return False

    def update_difference(self):
        daily_recipe = self.daily_recipe_var.get()
        daily_expense = self.daily_expense_var.get()
        other_recipe = self.other_recipe_var.get()
        cash_amount = self.cash_amount_entry.get()
        last_cash_float = self.last_cash_float_var.get()
        difference = float(daily_recipe if daily_recipe else 0) + float(other_recipe if other_recipe else 0) + \
        float(last_cash_float if last_cash_float else 0) - float(daily_expense if daily_expense else 0) - \
                     float(cash_amount if cash_amount else 0)
        self.difference_var.set(str(difference))

    def on_focus_in(self, event):
        AnyService.top_level_was_show = True

    def save(self):
        if Staff.current_staff is None:
            messagebox.showerror("Erreur", "Veuillez choisir un utilisateur")
            return
        comptant_amount = self.cash_amount_entry.get()
        new_cash_float = self.new_cash_float_entry.get()
        daily_recipe = self.daily_recipe_var.get()
        daily_expense = self.daily_expense_var.get()
        other_recipe = self.other_recipe_var.get()
        if not comptant_amount:
            messagebox.showerror("Erreur", "Veuillez entrer le montant comptant")
            self.cash_amount_entry.focus_set()
            return
        if not new_cash_float:
            messagebox.showerror("Erreur", "Veuillez entrer le montant du fond de caisse")
            self.new_cash_float_entry.focus_set()
            return
        new_daily_inventory_id = DailyInventory(cash_amount=float(comptant_amount), cash_float=float(new_cash_float),
                                             saver_staff=Staff.current_staff, daily=Daily.get_current_daily(),
                                                daily_recipe_amount=float(daily_recipe),
                                                daily_expense_amount=float(daily_expense),
                                                other_recipe_amount=float(other_recipe),
                                                ).save_to_db()
        Daily.get_current_daily().close_daily()
        Daily.create()
        Daily.current_daily = None
        messagebox.showinfo("DEL BLANCO", "Enregistré avec succès")
        self.new_cash_float_entry.delete(0, END)
        self.cash_amount_entry.delete(0, END)
        DailyInventoryTable.reload_all_table()
        DailyInventoryForm.reload_all_form()



