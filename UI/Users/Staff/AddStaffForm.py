from tkinter import messagebox

from DATA.Enumeration.UserRoleEnum import UserRoleEnum
from DATA.SettingClass.Staff import Staff
from Service.InputCheckService import InputCheckService
from UI.BaseForm.BaseUserForm import BaseUserForm
from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre


class AddStaffForm(BaseUserForm):

    def __init__(self, master):
        super().__init__(master=master)
        self.username_label = Label(self.form_frame, text="Login *", bg=couleur_sous_fenetre)
        self.username_label.grid(row=6, column=2, sticky=W, pady=20, padx=5)
        self.input_check_service = InputCheckService(self)
        self.username_entry = Entry(self.form_frame)
        self.username_entry.grid(row=6, column=3, sticky=EW, padx=5)

        self.password_label = Label(self.form_frame, text="Mot de passe *", bg=couleur_sous_fenetre)
        self.password_label.grid(row=7, column=2, sticky=W, pady=20, padx=5)

        self.password_entry = Entry(self.form_frame, show="*", validate="key",
                                    validatecommand=(self.input_check_service.check_password, "%S", "%P"))
        self.password_entry.grid(row=7, column=3, sticky=EW, padx=5)

        self.password_confirm_label = Label(self.form_frame, text="Confirmer le mot de passe *",
                                            bg=couleur_sous_fenetre)
        self.password_confirm_label.grid(row=8, column=2, sticky=W, pady=20, padx=5)

        self.password_confirm_entry = Entry(self.form_frame, show="*", validate="key",
                                            validatecommand=(self.input_check_service.check_password, "%S", "%P"))
        self.password_confirm_entry.grid(row=8, column=3, sticky=EW, padx=5)

    def save(self):
        firstname = self.firstname_entry.get()
        login = self.username_entry.get()
        password = self.password_entry.get()
        password_confirm = self.password_confirm_entry.get()
        if not firstname:
            messagebox.showerror("Erreur", "Le nom est obligatoire")
            return
        if not login:
            messagebox.showerror("Erreur", "Le login est obligatoire")
            return
        if not password:
            messagebox.showerror("Erreur", "Le mot de passe est obligatoire")
            return
        if not password_confirm:
            messagebox.showerror("Erreur", "Veuillez confirmer le mot de passe")
            return
        if len(password) != 5:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir 6 chiffres")
            return
        if password != password_confirm:
            messagebox.showerror("Erreur", "Les deux mots de passe ne correspondent pas")
            return
        staff = Staff(firstname=firstname, lastname=self.lastname_entry.get(), password=password,
                         username=login)
        if Staff.current_staff is not None:
            if Staff.current_staff.role == UserRoleEnum.ADMIN:
                staff.is_active = True
        staff.save_to_db()
        messagebox.showinfo("DEL BLANCO", "Utilisateur ajouté avec succès")
