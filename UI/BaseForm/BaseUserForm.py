from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre


class BaseUserForm(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.form_frame = Frame(self, bg=couleur_sous_fenetre,)
        self.form_frame.pack()
        self.firstname_label = Label(self.form_frame, text="Nom *", bg=couleur_sous_fenetre, width=20, anchor=W)
        self.firstname_label.grid(row=2, column=2, sticky=W, pady=20, padx=5)

        self.firstname_entry = Entry(self.form_frame, width=30)
        self.firstname_entry.grid(row=2, column=3, sticky=EW, padx=5)

        self.lastname_label = Label(self.form_frame, text="Prénom", bg=couleur_sous_fenetre)
        self.lastname_label.grid(row=3, column=2, sticky=W, pady=20, padx=5)

        self.lastname_entry = Entry(self.form_frame)
        self.lastname_entry.grid(row=3, column=3, sticky=EW, padx=5)

        self.save_button = Button(self.form_frame, text="Enregistrer", command=self.save, bg=couleur_sous_fenetre)
        self.save_button.grid(row=20, column=2, sticky=EW, pady=10, padx=5)
        self.abort_button = Button(self.form_frame, text="Annuler", command=self.abort, bg=couleur_sous_fenetre)
        self.abort_button.grid(row=20, column=3, sticky=EW, pady=10, padx=5)
        self.winfo_toplevel().bind("<Return>", lambda x: self.save())

    def save(self):
        pass

    def abort(self):
        self.destroy()


