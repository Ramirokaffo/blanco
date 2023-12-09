
from tkinter import ttk, messagebox

from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.DailyRecipe import DailyRecipe
from DATA.SettingClass.RecipeType import RecipeType
from DATA.SettingClass.Staff import Staff
from STATIC.ConstantFile import *
from Service.InputCheckService import InputCheckService
from UI.DailyRecipe.DailyRecipeTable import DailyRecipeTable


class DailyRecipeForm(Frame):

    def __init__(self, master, background=couleur_sous_fenetre):
        super().__init__(master)
        self.input_check_service = InputCheckService(self.master)
        self.master = master
        self.control_displays = 0
        self.configure(background=background)

        self.main_frame = Frame(self, bg=couleur_sous_fenetre)
        self.main_frame.pack(side=LEFT, fill=Y, padx=5)
        self.control_displays = 0

        self.recipe_type_label = Label(self.main_frame, anchor=W, text="Type de recette",
                                       justify=LEFT, bg=couleur_sous_fenetre)
        self.recipe_type_label.grid(row=1, column=1, padx=5, pady=15, sticky=W)

        self.recipe_type_entry = ttk.Combobox(self.main_frame, postcommand=self.on_select_expense_type)
        self.recipe_type_entry.grid(row=1, column=2, pady=15, padx=5, sticky=EW)

        self.recipe_amount_label = Label(self.main_frame, anchor=W, text="Montant de la recette",
                                         justify=LEFT, bg=couleur_sous_fenetre)
        self.recipe_amount_label.grid(row=2, column=1, pady=15, padx=5, sticky=W)

        self.recipe_amount_entry = Entry(self.main_frame, validate="key",
                                         validatecommand=(self.input_check_service.check_digit, "%S")
                                         )
        self.recipe_amount_entry.grid(row=2, column=2, pady=15, padx=5, sticky=EW)

        self.recipe_description_label = Label(self.main_frame, anchor=W, text="Description de la recette",
                                              justify=LEFT, bg=couleur_sous_fenetre)
        self.recipe_description_label.grid(row=3, column=1, pady=15, padx=5, sticky=W)

        self.recipe_description_entry = Text(self.main_frame, height=3, width=30)
        self.recipe_description_entry.grid(row=3, column=2, padx=5, pady=15, sticky=EW)

        ttk.Separator(self.main_frame, orient=HORIZONTAL).grid(row=4, padx=5, columnspan=2, column=1, sticky=EW, pady=10)
        self.save_button = Button(self.main_frame, text="Enregistrer",
                                  command=self.on_save, bg=couleur_bouton)
        self.save_button.grid(row=5, column=1, sticky=EW, padx=5, columnspan=2, pady=10)

    def on_select_expense_type(self):
        self.recipe_type_entry.config(values=[recipe_type.name for recipe_type in RecipeType().get_all()])

    def on_save(self):
        pass
        if Staff.current_staff is None:
            messagebox.showerror("DEL BLANCO", "Veuillez choisir un utilisateur !")
            return
        recipe_type = self.recipe_type_entry.get()
        recipe_amount = self.recipe_amount_entry.get()
        recipe_description = self.recipe_description_entry.get("0.0", END)
        if not recipe_type:
            messagebox.showerror("Erreur", message="Veuillez saisir ou sélectionner le type de recette !")
        elif not recipe_amount:
            messagebox.showerror("Erreur", message="Le montant de la recette est obligatoire !")
        else:
            # try:
            expected_recipe_type: RecipeType = RecipeType().get_by_name(name_value=recipe_type)
            DailyRecipe(amount=float(recipe_amount), description=recipe_description,
                         daily=Daily.get_current_daily(), staff=Staff.current_staff,
                         recipe_type=expected_recipe_type).save_to_db()
            messagebox.showinfo("DEL BLANCO", "Enregistrement éffectué avec succès !!")
            self.recipe_description_entry.delete("0.0", END)
            self.recipe_amount_entry.delete(0, END)
            self.recipe_type_entry.delete(0, END)
            DailyRecipeTable.reload_all_table()
            # except:
            #     messagebox.showerror("Erreur", "Une erreur s'est produite lors de l'enregistrement de la recette !")

