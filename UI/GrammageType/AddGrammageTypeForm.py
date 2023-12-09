from tkinter import *
from tkinter import messagebox

from DATA.SettingClass.GrammageType import GrammageType
from UI.BaseForm.BaseMiniForm import BaseMiniForm


class AddGrammageTypeForm(BaseMiniForm):

    def __init__(self, master):
        super().__init__(master)
        self.name_label.configure(text="Type de grammage")

    def save(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Erreur", "Le nom est obligatoire")
            return
        GrammageType(name=name, description=self.description_entry.get("0.0", END)).save_to_db()
        messagebox.showinfo("DEL BLANCO", "Enregistré avec succès")


