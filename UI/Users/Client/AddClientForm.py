
from tkinter import messagebox

from DATA.SettingClass.Client import Client
from Service.InputCheckService import InputCheckService
from UI.BaseForm.BaseUserForm import BaseUserForm
from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre


class AddClientForm(BaseUserForm):
    client: Client = None
    is_client_input_fill: bool = False

    def __init__(self, master, client: Client, is_sale_mode: bool = True):
        super().__init__(master)
        self.is_sale_mode = is_sale_mode
        # self.my_top_level_window = Toplevel(self.master)
        # self["master"] = self.my_top_level_window
        self.configure(background=couleur_sous_fenetre)
        self.master.configure(background=couleur_sous_fenetre)
        self.master.geometry("390x280+400+200")
        self.master.transient(self.master.master.winfo_toplevel())
        if client.firstname is not None:
            self.firstname_entry.insert(0, client.firstname)
        if client.lastname is not None:
            self.lastname_entry.insert(0, client.lastname)
        self.phone_number_label = Label(self.form_frame, text="Téléphone", bg=couleur_sous_fenetre)
        self.phone_number_label.grid(row=6, column=2, sticky=W, pady=20, padx=5)
        self.input_check_service = InputCheckService(self)
        self.phone_number_entry = Entry(self.form_frame)
        self.phone_number_entry.grid(row=6, column=3, sticky=EW, padx=5)
        if client.lastname is not None:
            self.phone_number_entry.insert(0, client.phone_number)
        self.pack(padx=20, pady=20)
        self.master.wait_window(self)

    def save(self):
        firstname = self.firstname_entry.get()
        if not firstname:
            messagebox.showerror("Erreur", "Le nom est obligatoire")
            return
        if self.is_sale_mode:
            AddClientForm.is_client_input_fill = True
            AddClientForm.client = Client(firstname=firstname, lastname=self.lastname_entry.get(),
                                          phone_number=self.phone_number_entry.get())
            self.master.destroy()
            return
        else:
            client_id = Client(firstname=firstname, lastname=self.lastname_entry.get(), phone_number=self.phone_number_entry.get()).save_to_db()
            messagebox.showinfo("DEL BLANCO", "Client ajouté avec succès")

    def abort(self):
        AddClientForm.is_client_input_fill = False
        self.master.destroy()
