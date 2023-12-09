from tkinter import *
from tkinter import messagebox

from DATA.SettingClass.Gamme import Gamme
from UI.BaseForm.BaseMiniForm import BaseMiniForm


class AddGammeForm(BaseMiniForm):

    def __init__(self, master):
        super().__init__(master)
        self.name_label.configure(text="Nom de la gamme")

    def save(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Erreur", "Le nom est obligatoire")
            return
        Gamme(name=name, description=self.description_entry.get("0.0", END)).save_to_db()
        messagebox.showinfo("DEL BLANCO", "Enregistré avec succès")





