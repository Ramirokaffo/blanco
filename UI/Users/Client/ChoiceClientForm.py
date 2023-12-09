from tkinter import messagebox

from DATA.SettingClass.Client import Client
from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre
from UI.Users.Client.ClientTable import ClientTable
from customtkinter import CTkScrollableFrame, CTkButton, CTkFrame


class ChoiceClientForm(Toplevel):
    client: Client = None
    is_client_input_fill: bool = False

    def __init__(self, master, client: Client):
        super().__init__(master)
        self.configure(background=couleur_sous_fenetre)

        main_frame = Frame(self, background=couleur_sous_fenetre)
        main_frame.pack(expand=YES, pady=20, padx=20)
        # self.master.geometry("390x280+400+200")
        self.transient(self.master.master.winfo_toplevel())
        self.client_table = ClientTable(main_frame)
        self.client_table.grid(row=1, column=1, columnspan=2, pady=(0, 20))
        Button(main_frame, text="Enregistrer", command=self.save).grid(row=2, column=1, sticky=EW)
        Button(main_frame, text="Annuler", command=self.abort).grid(row=2, column=2, sticky=EW)
        self.master.wait_window(self)

    def save(self):
        ChoiceClientForm.is_client_input_fill = True
        expected_clients: list[Client] = self.client_table.get_selected()
        if len(expected_clients) == 0:
            messagebox.showerror("Erreur", "Veuillez selectionner un client")
            return
        if len(expected_clients) > 1:
            messagebox.showerror("Erreur", "Veuillez selectionner un seul client")
            return
        ChoiceClientForm.client = expected_clients[0]
        self.destroy()
        return

    def abort(self):
        ChoiceClientForm.is_client_input_fill = False
        self.destroy()


