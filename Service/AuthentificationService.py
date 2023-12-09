from tkinter import messagebox
from tkinter import *

from DATA.SettingClass.Staff import Staff
from STATIC.ConstantFile import couleur_sous_fenetre
from Service.AnyService import AnyService


class AuthentificationPage:

    def __init__(self, master, staff: Staff):
        self.master = master
        self.user_name = staff.get_all_name()
        self.staff = staff
        # self.nom_vendeur_ch = nom_vendeur_ch
        self.status = False
        # self.nom_vendeur_ch.config(state=DISABLED)
        self.fenetre_auth = Toplevel(self.master)
        self.fenetre_auth.title("Authentification")
        # self.fenetre_auth.iconbitmap(logo)
        self.fenetre_auth.resizable(width=False, height=False)
        self.fenetre_auth.wm_transient(self.master)
        self.fenetre_auth.geometry("630x200+400+150")
        self.fenetre_auth.configure(background=couleur_sous_fenetre)
        self.frame = Frame(self.fenetre_auth, bg=couleur_sous_fenetre)
        self.frame.pack(expand=YES)
        self.label_nom_utilisateur = Label(self.frame, font=("arial", 15, "bold"), bg=couleur_sous_fenetre,
                                           text=f"Veuillez entrer le mot de passe de l'utilisateur {self.user_name}")
        self.label_nom_utilisateur.grid(row=1, column=1, columnspan=2, sticky=EW)

        self.label_password_utilisateur = Label(self.frame, font=("arial", 12), text="Mot de passe:", bg=couleur_sous_fenetre)
        self.label_password_utilisateur.grid(row=2, column=1, sticky=EW, pady=20)

        self.champs_password = Entry(self.frame, show="*")
        self.champs_password.grid(row=2, column=2, sticky=EW, pady=20)
        self.champs_password.focus_set()

        self.bouton_ok = Button(self.frame, text="OK", width=20, command=lambda: self.verify_user(0),
                                bg=couleur_sous_fenetre)
        self.bouton_ok.grid(row=3, column=1, sticky=EW)

        self.bouton_cancel = Button(self.frame, text="Annuler", width=20, command=self.wait_windows,
                                    bg=couleur_sous_fenetre)
        self.bouton_cancel.grid(row=3, column=2, sticky=EW)

        self.fenetre_auth.bind("<Return>", self.verify_user)
        # self.fenetre_auth.master.winfo_toplevel().bind("<Return>", self.verify_user)
        # print(self.fenetre_auth.master.winfo_toplevel())
        # self.fenetre_auth.wait_window(self.fenetre_auth)
        AnyService.top_level_was_show = True
        # self.fenetre_auth.bind("<Destroy>", self.on_destroy)
        self.fenetre_auth.focus_set()

    # def on_destroy(self, event):
    #     AnyService.top_level_was_show = False

    def wait_windows(self):
        # if not self.status:
        #     self.nom_vendeur_ch.config()
        self.fenetre_auth.destroy()

    def verify_user(self, event):
        result = Staff().login(username=self.staff.username, password=self.champs_password.get())
        if result is None:
            messagebox.showerror("DEL BLANCO", "Mot de passe incorrect !!")
            self.champs_password.delete(0, END)
            self.champs_password.focus_set()
            self.status = False
            return False
        else:
            self.status = True
            self.fenetre_auth.destroy()
            return True

