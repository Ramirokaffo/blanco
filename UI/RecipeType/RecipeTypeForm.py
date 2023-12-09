from tkinter import *
from tkinter import messagebox

from DATA.SettingClass.RecipeType import RecipeType
from UI.BaseForm.BaseMiniForm import BaseMiniForm


class AddRecipeTypeForm(BaseMiniForm):

    def __init__(self, master):
        super().__init__(master)
        self.name_label.configure(text="Nom du type de recette")

    def save(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Erreur", "Le nom est obligatoire")
            return
        RecipeType(name=name, description=self.description_entry.get("0.0", END)).save_to_db()
        messagebox.showinfo("DEL BLANCO", "Enregistré avec succès")

