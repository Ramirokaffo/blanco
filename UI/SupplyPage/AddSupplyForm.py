from datetime import date
from tkinter import messagebox, ttk

from customtkinter import CTkButton, CTkToplevel
from dateutil import parser

from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import *
from Service.DateTimeService import DateTimeService
from Service.InputCheckService import InputCheckService


class AddSupplyForm(Frame):

    def __init__(self, master, supply: Supply = None):
        super().__init__(master)
        self.master = master
        self.input_check_service = InputCheckService(self.master)
        self.foction_inserer_prix_vente_recent_approv = self.master.register(self.on_product_name_change)
        self.paned_fen_approv_produit = PanedWindow(self.master, bg=couleur_frame, orient=HORIZONTAL,
                                                    sashwidth=8)
        self.paned_fen_approv_produit.pack(expand=YES, fill=BOTH)

        self.label_frame_caract_approv = LabelFrame(self.paned_fen_approv_produit, text="Nouvel approvisionnement",
                                                    labelanchor=N,
                                                    bg=couleur_sous_fenetre, fg=couleur_police, bd=bd_widget,
                                                    relief=relief_widget)

        self.paned_fen_approv_produit.add(self.label_frame_caract_approv)

        self.label_frame_approv_save = LabelFrame(self.label_frame_caract_approv, text=""
                                                  , bg=couleur_sous_fenetre, fg=couleur_police, labelanchor=N,
                                                  bd=bd_widget,
                                                  relief=relief_widget)
        self.label_frame_approv_save.pack(side=TOP)

        self.label_frame_approv_outil_bas = LabelFrame(self.label_frame_caract_approv, text=""
                                                       , bg=couleur_sous_fenetre, fg=couleur_police, labelanchor=N,
                                                       bd=bd_widget,
                                                       relief=relief_widget)
        self.label_frame_approv_outil_bas.pack(side=BOTTOM)

        largeur_label_approv = 20
        largeur_champs_approv = 40
        hauteur_label_approv = 3

        """ Label et champs des produits achetés"""

        self.produit_achete_approv = Label(self.label_frame_approv_save, text="Produit acheté*: ",
                                           height=hauteur_label_approv,
                                           width=largeur_label_approv, bg=couleur_label, anchor=W,
                                           justify="left", fg=couleur_police, font=(police, taille_police_texte))
        self.produit_achete_approv.grid(row=1, column=1)
        self.product_name_entry = ttk.Combobox(self.label_frame_approv_save, width=largeur_champs_approv - 2,
                                               font=(police, taille_police_texte), validate="all",
                                               postcommand=self.get_product_list,
                                               validatecommand=(
                                                   self.foction_inserer_prix_vente_recent_approv, "%P"))
        self.product_name_entry.grid(row=1, column=2)

        self.quantite_achete_approv = Label(self.label_frame_approv_save, text="Quantité achetée*: ",
                                            height=hauteur_label_approv,
                                            width=largeur_label_approv, anchor=W,
                                            bg=couleur_label,
                                            justify="left", fg=couleur_police, font=(police, taille_police_texte))
        self.quantite_achete_approv.grid(row=2, column=1, ipadx=5)
        self.product_count_entry = ttk.Combobox(self.label_frame_approv_save, width=largeur_champs_approv - 2,
                                                font=(police, taille_police_texte)
                                                , validate="key",
                                                validatecommand=(self.input_check_service.check_digit, "%S")
                                                )
        self.product_count_entry["values"] = list(range(1, 51))
        self.product_count_entry.grid(row=2, column=2)

        """Cout unitaire du produit"""
        self.pu_produit_approv = Label(self.label_frame_approv_save, text="Cout unitaire d'achat*:",
                                       height=hauteur_label_approv, anchor=W,
                                       width=largeur_label_approv, bg=couleur_label,
                                       justify="left", fg=couleur_police, font=(police, taille_police_texte))
        self.pu_produit_approv.grid(row=3, column=1, ipadx=5)
        self.product_unit_coast_entry = Entry(self.label_frame_approv_save, width=largeur_champs_approv,
                                              fg=couleur_police_champs, validate="key",
                                              validatecommand=(self.input_check_service.check_digit, "%S"),
                                              font=(police, taille_police_texte))
        self.product_unit_coast_entry.grid(row=3, column=2)

        self.pu_vente_approv = Label(self.label_frame_approv_save, text="Prix unitaire de vente*:",
                                     height=hauteur_label_approv, anchor=W,
                                     width=largeur_label_approv, bg=couleur_label,
                                     justify="left", fg=couleur_police, font=(police, taille_police_texte))
        self.pu_vente_approv.grid(row=5, column=1, ipadx=5)
        self.product_unit_price_entry = Entry(self.label_frame_approv_save, width=largeur_champs_approv,
                                              fg=couleur_police_champs, validate="key",
                                              validatecommand=(self.input_check_service.check_digit, "%S"),
                                              font=(police, taille_police_texte))
        self.product_unit_price_entry.grid(row=5, column=2)

        """label et champs de la date d'expiration du produit"""
        self.date_expiration_produit_approv = Label(self.label_frame_approv_save, text="Expiration(JJ-MM-AAAA):",
                                                    height=hauteur_label_approv, anchor=W,
                                                    width=largeur_label_approv, bg=couleur_label,
                                                    justify="left", fg=couleur_police,
                                                    font=(police, taille_police_texte))
        self.date_expiration_produit_approv.grid(row=6, column=1, ipadx=5)
        self.product_exp_entry = Entry(self.label_frame_approv_save, width=largeur_champs_approv,
                                       font=(police, taille_police_texte),
                                       fg=couleur_police_champs, validate="key",
                                       validatecommand=(self.input_check_service.check_date, "%S", "%P"),
                                       )
        self.product_exp_entry.grid(row=6, column=2)

        """Label et champs du founisseur"""
        self.nom_fournisseur = Label(self.label_frame_approv_save, text="Nom du fournisseur:",
                                     height=hauteur_label_approv, anchor=W,
                                     width=largeur_label_approv, bg=couleur_label,
                                     justify="left", fg=couleur_police, font=(police, taille_police_texte))
        self.nom_fournisseur.grid(row=7, column=1, ipadx=5)
        self.nom_fournisseur_champs = ttk.Combobox(self.label_frame_approv_save, width=largeur_champs_approv - 2,
                                                   postcommand=self.suggestion_nom_fournisseur,
                                                   font=(police, taille_police_texte))
        self.nom_fournisseur_champs.grid(row=7, column=2)

        self.bouton_enregistrer_produit = CTkButton(self.label_frame_approv_save, text="Enregistrer l'approvisonnement",
                                                    # bg=couleur_bouton,
                                                    command=lambda: self.save_supply(event=0),
                                                    # fg=couleur_police
                                                    )
        self.bouton_enregistrer_produit.grid(row=9, column=1, columnspan=2, sticky=NSEW, pady=(5, 10), padx=5)
        if supply is not None:
            self.product_exp_entry.insert(0, str(supply.expiration_date) if supply.expiration_date else "")
            self.product_unit_price_entry.insert(0, str(supply.unit_price) if supply.unit_price else "")
            self.product_unit_coast_entry.insert(0, str(supply.unit_coast) if supply.unit_coast else "")
            self.product_name_entry.insert(0, str(supply.product.name) if supply.product else "")
            self.product_count_entry.insert(0, str(supply.product_count) if supply.product_count else "")

    def suggestion_nom_fournisseur(self):
        # self.nom_fournisseur_champs["values"] = self.approv_table_service.select_nom_fournisseur()
        pass

    def get_product_list(self):
        self.product_name_entry["values"] = Product.find_sale_product(self.product_name_entry.get())

    def on_product_name_change(self, product_name):
        product = Product.find_product_by_name(product_name)
        if product is not None:
            supply = Supply.find_product_supply(product_id=product.id)
            if len(supply) != 0:
                self.product_unit_price_entry.delete(0, END)
                self.product_unit_coast_entry.delete(0, END)
                self.product_count_entry.delete(0, END)
                self.product_unit_price_entry.insert(0, f"{supply[0].unit_price:.0f}")
                self.product_unit_coast_entry.insert(0, f"{supply[0].unit_coast:.0f}")
                self.product_count_entry.insert(0, f"{supply[0].cash_amount_entry:.0f}")
                return True
        self.product_unit_price_entry.delete(0, END)
        self.product_unit_coast_entry.delete(0, END)
        self.nom_fournisseur_champs.delete(0, END)
        return True

    # @staticmethod
    # def show():
    #     tl = CTkToplevel()
    #     tl.transient(tl.winfo_toplevel())
    #     AddSupplyForm(tl).pack()

    def save_supply(self, event):
        if Staff.current_staff is None:
            messagebox.showerror("Erreur", "Veuillez choisir l'auteur de l'approvisionnement !")
            return
        product_name = self.product_name_entry.get()
        product_exp_date = DateTimeService.parse_date(self.product_exp_entry.get())
        nom_fournisseur_obtenue = self.nom_fournisseur_champs.get()
        product_count = self.product_count_entry.get()
        product_unit_coast = self.product_unit_coast_entry.get()
        product_unit_price = self.product_unit_price_entry.get()
        if not product_name and not product_exp_date and not nom_fournisseur_obtenue \
                and not product_count and not product_unit_coast and not product_unit_price:
            messagebox.showerror("Erreur", "Vous devez renseigner les données de l'approvisionnment")
            return
        product = Product.find_product_by_name(product_name)
        if product_name != "":
            if product is None:
                question = messagebox.askyesno(title="erreur",
                                               message=f"{product_name} n'existe pas dans la base de données\n"
                                                       "\n"
                                                       "Ajouter maintenant?")
                if question == True:
                    # self.racourci_ajout_prod_bd(product_name)
                    return
        if product_name:
            """Verifier si tous les champs necessaires sont remplis"""
            if product_unit_coast == "":
                messagebox.showerror(title="Erreur", message="Veillez entrer le cout unitaire d'achat du produit")
                return
            if product_unit_price == "":
                messagebox.showerror(title="Erreur", message="Veillez entrer le prix unitaire de vente du produit")
                return
            if product_name != "" and product_count != "":
                if int(product_unit_price) < int(product_unit_coast):
                    messagebox.showerror("Erreur", "Le prix de vente doit etre supérieur au cout d'achat")
                    self.product_unit_coast_entry.focus_set()
                    return
                # try:
                if 3 == 3:
                    if product_exp_date is not None:
                        product_exp_date = parser.parse(product_exp_date).date()
                    if product_exp_date is not None and date.today() >= product_exp_date:
                        messagebox.showerror("Erreur",
                                             "La date d'expiration doit etre superieure à la date d'aujourd'hui !")
                        self.product_exp_entry.focus_set()
                        return
                    Supply(product_count=int(product_count),
                           product_count_rest=int(product_count),
                           unit_coast=float(product_unit_coast),
                           unit_price=float(product_unit_price),
                           product=product,
                           saver_staff=Staff.current_staff,
                           daily=Daily.get_current_daily(),
                           expiration_date=product_exp_date,
                           ).save_to_db()
                    messagebox.showinfo(title='DEL BLANCO', message=f"Vous venez d'ajouter "
                                                                    f"{product_count} unités de {product_name} en stock!")
                    self.product_name_entry.delete(0, END)
                    self.product_exp_entry.delete(0, END)
                    self.nom_fournisseur_champs.delete(0, END)
                    self.product_count_entry.delete(0, END)
                    self.product_unit_coast_entry.delete(0, END)
                    self.product_name_entry.focus_set()
                # except:
                #     messagebox.showerror(title="Erreur",
                #                          message="Erreur inconnue! vérifiez la date d'expiration des produits")
                #     fenetre_approvisionnement.focus_set()

    def quit_page_approv(self):
        """Quitter la page des approvisionnements"""
        # self.super_master_nb.forget(self.master)
        pass
