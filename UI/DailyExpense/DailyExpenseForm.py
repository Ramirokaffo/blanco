from tkinter import ttk, messagebox

from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.DailyExpense import DailyExpense
from DATA.SettingClass.ExpenseType import ExpenseType
from DATA.SettingClass.Staff import Staff
from STATIC.ConstantFile import *
from Service.InputCheckService import InputCheckService
from UI.DailyExpense.DailyExpenseTable import DailyExpenseTable


class DailyExpenseForm(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.input_check_service = InputCheckService(master)

        self.main_frame = Frame(master, bg=couleur_sous_fenetre)
        self.main_frame.pack(side=LEFT, fill=Y, padx=5)

        self.expense_type_label = Label(self.main_frame, anchor=W, text="Type de dépense",
                                        justify=LEFT, bg=couleur_sous_fenetre)
        self.expense_type_label.grid(row=1, column=1, padx=5, pady=15, sticky=W)

        self.type_vente_champs = ttk.Combobox(self.main_frame, postcommand=self.on_select_expense_type)
        self.type_vente_champs.grid(row=1, column=2, pady=15, padx=5, sticky=EW)

        self.expense_amount_label = Label(self.main_frame, anchor=W, text="Montant de la dépense",
                                          justify=LEFT, bg=couleur_sous_fenetre)
        self.expense_amount_label.grid(row=2, column=1, pady=15, padx=5, sticky=W)

        self.expense_amount_entry = Entry(self.main_frame, validate="key",
                                          validatecommand=(self.input_check_service.check_digit, "%S"))
        self.expense_amount_entry.grid(row=2, column=2, pady=15, padx=5, sticky=EW)

        self.label_description_depense = Label(self.main_frame, anchor=W, text="Description de la dépense",
                                               justify=LEFT, bg=couleur_sous_fenetre)
        self.label_description_depense.grid(row=3, column=1, pady=15, padx=5, sticky=W)

        self.description_entry = Text(self.main_frame, height=3, width=30)
        self.description_entry.grid(row=3, column=2, padx=5, pady=15, sticky=EW)

        ttk.Separator(self.main_frame, orient=HORIZONTAL).grid(row=4, padx=5, columnspan=2, column=1, sticky=EW, pady=10)
        self.save_button = Button(self.main_frame, text="Enregistrer", command=self.on_save, bg=couleur_bouton)
        self.save_button.grid(row=5, column=1, sticky=EW, padx=5, columnspan=2, pady=10)

    def on_select_expense_type(self):
        self.type_vente_champs.config(values=[raison.name for raison in ExpenseType().get_all()])

    def on_save(self):
        if Staff.current_staff is None:
            messagebox.showerror("DEL BLANCO", "Veuillez choisir l'auteur de la dépense !")
            return
        raison_name = self.type_vente_champs.get()
        expense_amount = self.expense_amount_entry.get()
        expense_description = self.description_entry.get("0.0", END)
        if not raison_name:
            messagebox.showerror("Erreur", message="Veuillez saisir ou sélectionner le type de dépense !")
        elif not expense_amount:
            messagebox.showerror("Erreur", message="Le montant de la dépense est obligatoire !")
        else:
            try:
                expected_reason: ExpenseType = ExpenseType().get_by_name(name_value=raison_name)
                DailyExpense(amount=float(expense_amount), description=expense_description,
                             daily=Daily.get_current_daily(), staff=Staff.current_staff,
                             raison=expected_reason).save_to_db()
                messagebox.showinfo("DEL BLANCO", "Enregistrement éffectué avec succès !!")
                self.description_entry.delete("0.0", END)
                self.expense_amount_entry.delete(0, END)
                self.type_vente_champs.delete(0, END)
                DailyExpenseTable.reload_all_table()
            except:
                messagebox.showerror("Erreur", "Une erreur s'est produite lors de l'enregistrement de la dépense !")

