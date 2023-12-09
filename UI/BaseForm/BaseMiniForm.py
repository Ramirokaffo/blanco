from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre


class BaseMiniForm(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.form_frame = Frame(self, bg=couleur_sous_fenetre,)
        self.form_frame.pack()
        self.name_label = Label(self.form_frame, text="Nom", bg=couleur_sous_fenetre)
        self.name_label.grid(row=2, column=2, sticky=EW, pady=20)

        self.name_entry = Entry(self.form_frame)
        self.name_entry.grid(row=2, column=3, sticky=EW)

        self.description_label = Label(self.form_frame, text="Description", bg=couleur_sous_fenetre)
        self.description_label.grid(row=3, column=2, sticky=EW)

        self.description_entry = Text(self.form_frame, height=10, width=50)
        self.description_entry.grid(row=3, column=3, sticky=EW)

        self.save_button = Button(self.form_frame, text="Enregistrer", command=self.save, bg=couleur_sous_fenetre)
        self.save_button.grid(row=4, column=2, sticky=EW, columnspan=2, pady=10)
        self.winfo_toplevel().bind("<Return>", lambda x: self.save())

    def save(self):
        pass