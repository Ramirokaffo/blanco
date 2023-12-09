from tkinter import ttk, messagebox

from datetime import date

from dateutil import parser

from DATA.SettingClass.Category import Category
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Gamme import Gamme
from DATA.SettingClass.GrammageType import GrammageType
from DATA.SettingClass.Product import Product
from DATA.SettingClass.ProductImage import ProductImage
from DATA.SettingClass.Rayon import Rayon
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supplier import Supplier
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import *
from Service.DateTimeService import DateTimeService
from Service.ImageService import ImageService
from Service.InputCheckService import InputCheckService
from UI.Product.AddProductSetting import PageParametreAjoutProduit
from UI.Images.ImageManager import ImageManager
from customtkinter import *


class AddProductForm(LabelFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master: Misc = master
        hauteur_label_gprod = 2
        self.image_produit = StringVar(value=image_defaut_produit)
        self.variable_control_enregis_modifprod = IntVar()
        self.var_flex_id_prod_a_modi = StringVar()
        self.liste_caract_prod_a_mod = StringVar()
        self.input_check_service = InputCheckService(self.master)
        self.configure(text="Caracteristiques du produit", labelanchor=N)

        self.label_frame_left_entry = LabelFrame(self,
                                                 labelanchor=N,
                                                 bg=couleur_sous_fenetre, fg=couleur_police, bd=bd_widget,
                                                 relief=relief_widget)
        self.label_frame_left_entry.pack(expand=YES, fill=X, ipadx=10, side=LEFT)
        # separator = ttk.Separator(self, orient=VERTICAL).pack(fill=Y)
        self.label_frame_right_entry = LabelFrame(self,
                                                  labelanchor=N,
                                                  bg=couleur_sous_fenetre, fg=couleur_police, bd=bd_widget,
                                                  relief=relief_widget)
        self.label_frame_right_entry.pack(side=RIGHT, anchor=N, fill=Y, ipadx=10)

        a = 1
        fusion_colon = 1
        """label et champs de l'identifiant du produit"""
        self.id_produit = Label(self.label_frame_left_entry, text="Code du produit*",
                                height=hauteur_label_gprod,
                                bg=couleur_label,
                                justify="left", fg=couleur_police, font=(police, taille_police_texte - a), anchor=W)
        self.id_produit.grid(row=1, column=1, sticky=EW, columnspan=fusion_colon)
        self.id_produit_champs = Entry(self.label_frame_left_entry,
                                       fg=couleur_police_champs,
                                       font=(police, taille_police_texte - a))
        self.id_produit_champs.grid(row=1, column=2, columnspan=fusion_colon, sticky=EW)
        """label et champs du nom du produit"""
        self.nom_produit = Label(self.label_frame_left_entry, text="Nom du produit*", height=hauteur_label_gprod,
                                 bg=couleur_label, anchor=W,
                                 justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.nom_produit.grid(row=2, column=1, sticky=EW, columnspan=fusion_colon)
        self.nom_produit_champs = Entry(self.label_frame_left_entry,
                                        fg=couleur_police_champs,
                                        font=(police, taille_police_texte - a))
        self.nom_produit_champs.grid(row=2, column=2, sticky=EW, columnspan=fusion_colon)

        """label et champs de la categorie du produit"""
        self.categorie_produit = Label(self.label_frame_left_entry, text="Categorie du produit",
                                       height=hauteur_label_gprod,
                                       bg=couleur_label, anchor=W,
                                       justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.categorie_produit.grid(row=3, column=1, sticky=EW, columnspan=fusion_colon)
        self.categorie_produit_champs = ttk.Combobox(self.label_frame_left_entry,
                                                     # postcommand=self.sugerer_categorie_produit,
                                                     font=(police, taille_police_texte - a),
                                                     values=[category.name for category in Category.get_all()]
                                                     )
        self.categorie_produit_champs.grid(row=3, column=2, sticky=EW, columnspan=fusion_colon)
        """label et champs de la marque du produit"""
        self.marque_produit = Label(self.label_frame_left_entry, text="Marque du produit", height=hauteur_label_gprod,
                                    bg=couleur_label, anchor=W,
                                    justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.marque_produit.grid(row=4, column=1, sticky=EW, columnspan=fusion_colon)
        self.marque_produit_champs = ttk.Combobox(self.label_frame_left_entry,
                                                  # postcommand=self.sugerer_marque_produit,
                                                  font=(police, taille_police_texte - a),
                                                  # values=self.liste_marque
                                                  )
        self.marque_produit_champs.grid(row=4, column=2, sticky=EW, columnspan=fusion_colon)
        """label et champs du cout d'achat du produit"""
        self.cout_achat_produit = Label(self.label_frame_left_entry, text="Cout d'achat du produit*",
                                        height=hauteur_label_gprod,
                                        bg=couleur_label, anchor=W,
                                        justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.cout_achat_produit.grid(row=5, column=1, sticky=EW, columnspan=fusion_colon)
        self.cout_achat_produit_champs = Entry(self.label_frame_left_entry,
                                               fg=couleur_police_champs, validate="key",
                                               validatecommand=(self.input_check_service.check_digit, "%S"),
                                               font=(police, taille_police_texte - a), name="cap")
        self.cout_achat_produit_champs.grid(row=5, column=2, sticky=EW, columnspan=fusion_colon)

        """label et champs du prix de vente du produit"""
        self.prix_vente_produit = Label(self.label_frame_left_entry, text="Prix de vente du produit*",
                                        height=hauteur_label_gprod,
                                        bg=couleur_label, anchor=W,
                                        justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.prix_vente_produit.grid(row=6, column=1, sticky=EW, columnspan=fusion_colon)
        self.prix_vente_produit_champs = Entry(self.label_frame_left_entry,
                                               fg=couleur_police_champs, validate="key",
                                               validatecommand=(self.input_check_service.check_digit, "%S"),
                                               font=(police, taille_police_texte - a), name="pvp")
        self.prix_vente_produit_champs.grid(row=6, column=2, sticky=EW, columnspan=fusion_colon)

        """label et champs de la quantité de debut de stock du produit"""
        self.quantite_debut_stock_produit = Label(self.label_frame_left_entry, text="Quantité du produit*",
                                                  height=hauteur_label_gprod,
                                                  bg=couleur_label, anchor=W,
                                                  justify="left", fg=couleur_police,
                                                  font=(police, taille_police_texte - a))
        self.quantite_debut_stock_produit.grid(row=7, column=1, sticky=EW, columnspan=fusion_colon)
        self.quantite_debut_stock_produit_champs = Entry(self.label_frame_left_entry,
                                                         fg=couleur_police_champs, validate="key",
                                                         validatecommand=(self.input_check_service.check_digit, "%S"),
                                                         font=(police, taille_police_texte - a), name="qp")
        self.quantite_debut_stock_produit_champs.grid(row=7, column=2, sticky=EW, columnspan=fusion_colon)

        self.date_expiration_produit = Label(self.label_frame_left_entry, text="Expiration(JJ-MM-AAAA):",
                                             height=hauteur_label_gprod, anchor=W,
                                             bg=couleur_label,
                                             justify="left", fg=couleur_police, font=(police, taille_police_texte - a))

        self.date_expiration_produit.grid(row=8, column=1, sticky=EW, columnspan=fusion_colon)
        self.product_exp_entry = Entry(self.label_frame_left_entry,
                                       fg=couleur_police_champs,
                                       validatecommand=(self.input_check_service.check_date, "%S", "P"),
                                       font=(police, taille_police_texte - a))
        self.product_exp_entry.grid(row=8, column=2, sticky=EW, columnspan=fusion_colon)
        self.product_supplier_name = Label(self.label_frame_left_entry, text="Nom du fournisseur:",
                                           height=hauteur_label_gprod,
                                           bg=couleur_label, anchor=W,
                                           justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.product_supplier_name.grid(row=9, column=1, sticky=EW, columnspan=fusion_colon)
        self.product_supplier_name_entry = ttk.Combobox(self.label_frame_left_entry,
                                                        # postcommand=self.sugerer_nom_fournisseur,
                                                        font=(police, taille_police_texte - a),
                                                        values=[supplier.get_all_name() for supplier in
                                                                Supplier.get_all()]
                                                        )
        self.product_supplier_name_entry.grid(row=9, column=2, sticky=EW, columnspan=fusion_colon)

        self.rayon_produit = Label(self.label_frame_left_entry, text="Rayon du produit:", height=hauteur_label_gprod,
                                   bg=couleur_label, anchor=W,
                                   justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.rayon_produit.grid(row=10, column=1, sticky=EW, columnspan=fusion_colon)
        self.rayon_produit_champs = ttk.Combobox(self.label_frame_left_entry,
                                                 font=(police, taille_police_texte - a),
                                                 values=[rayon.name for rayon in Rayon.get_all()]
                                                 )
        self.rayon_produit_champs.grid(row=10, column=2, sticky=EW, columnspan=fusion_colon)

        """label et champs du grammage du produit"""
        self.grammage_produit = Label(self.label_frame_left_entry, text="Grammage du produit",
                                      height=hauteur_label_gprod,
                                      bg=couleur_label, anchor=W,
                                      justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.grammage_produit.grid(row=11, column=1, sticky=EW, columnspan=fusion_colon)
        self.grammage_produit_champs = Entry(self.label_frame_left_entry,
                                             fg=couleur_police_champs, validate="key",
                                             validatecommand=(self.input_check_service.check_digit, "%S"),
                                             font=(police, taille_police_texte - a))
        self.grammage_produit_champs.grid(row=11, column=2, sticky=EW, columnspan=fusion_colon)
        """label et champs de l'unité du grammage du produit"""
        self.unite_grammage_produit = Label(self.label_frame_left_entry, text="Unité du grammage",
                                            height=hauteur_label_gprod,
                                            bg=couleur_label, anchor=W,
                                            justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.unite_grammage_produit.grid(row=12, column=1, sticky=EW, columnspan=fusion_colon)
        self.product_grammage_type_entry = ttk.Combobox(self.label_frame_left_entry,
                                                        font=(police, taille_police_texte - a))
        self.product_grammage_type_entry["values"] = [grammage_type.name for grammage_type in GrammageType.get_all()]
        self.product_grammage_type_entry.grid(row=12, column=2, sticky=EW, columnspan=fusion_colon)

        self.product_gamme = Label(self.label_frame_left_entry, text="Gamme du produit",
                                   height=hauteur_label_gprod,
                                   bg=couleur_label, anchor=W,
                                   justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.product_gamme.grid(row=13, column=1, sticky=EW, columnspan=fusion_colon)
        self.product_gamme_entry = ttk.Combobox(self.label_frame_left_entry,
                                                font=(police, taille_police_texte - a))
        self.product_gamme_entry["values"] = [gamme.name for gamme in Gamme.get_all()]
        self.product_gamme_entry.grid(row=13, column=2, sticky=EW, columnspan=fusion_colon)

        """label et champs du seuil des commandes du produit"""
        self.seuil_commande_produit = Label(self.label_frame_left_entry, text="Seuil des commandes",
                                            height=hauteur_label_gprod,
                                            bg=couleur_label, anchor=W,
                                            justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.seuil_commande_produit.grid(row=14, column=1, sticky=EW, columnspan=fusion_colon, pady=0)
        self.seuil_commande_produit_champs = ttk.Combobox(self.label_frame_left_entry,
                                                          font=(police, taille_police_texte - a)
                                                          , validate="key",
                                                          validatecommand=(self.input_check_service.check_digit, "%S"),
                                                          )
        self.seuil_commande_produit_champs["values"] = list(range(5, 51, 5))
        self.seuil_commande_produit_champs.grid(row=14, column=2, sticky=EW, columnspan=fusion_colon, pady=0)

        """label et champs de la periode des commandes produit"""
        self.periode_commande_produit = Label(self.label_frame_left_entry, text="Periode d'alerte(mois)",
                                              height=hauteur_label_gprod,
                                              bg=couleur_label, anchor=W,
                                              justify="left", fg=couleur_police, font=(police, taille_police_texte - a))
        self.periode_commande_produit.grid(row=15, column=1, sticky=EW, columnspan=fusion_colon, pady=0)
        self.periode_commande_produit_champs = ttk.Combobox(self.label_frame_left_entry,
                                                            font=(police, taille_police_texte - a)
                                                            , validate="key",
                                                            validatecommand=(
                                                                self.input_check_service.check_digit, "%S"),
                                                            )
        self.periode_commande_produit_champs["values"] = list(range(1, 7))
        self.periode_commande_produit_champs.grid(row=15, column=2, sticky=EW, columnspan=fusion_colon, pady=0)

        self.label_frame_descript_prod_pop = LabelFrame(self.winfo_toplevel(), labelanchor=N,
                                                        bg=couleur_sous_fenetre, fg=couleur_police, bd=bd_widget + 5,
                                                        relief=RIDGE)

        self.frame_icone_pro = Frame(self.label_frame_left_entry, bg=couleur_sous_fenetre)
        self.frame_icone_pro.grid(row=16, column=1, sticky=EW)

        self.frame_icone_pro_est = Frame(self.label_frame_left_entry, bg=couleur_sous_fenetre)

        self.frame_action_pro = Frame(self.label_frame_left_entry, bg=couleur_sous_fenetre)
        self.frame_action_pro.grid(row=17, column=1, sticky=EW, columnspan=2)

        self.labelf_description_prouit = LabelFrame(self.label_frame_right_entry, text="Description du produit",
                                                    bg=couleur_sous_fenetre, fg=couleur_police, labelanchor=N,
                                                    font=(police, taille_police_texte), bd=bd_widget,
                                                    relief=relief_widget)
        self.labelf_description_prouit.pack(side=TOP)
        self.images_widget = ImageManager(self.label_frame_right_entry, images=[], is_view_mode=False)
        self.images_widget.pack(expand=YES)

        # self.msg_description_prod = Message(self.labelf_description_prouit,
        #                                     text="Ajouter une description au produit pour faciliter "
        #                                          "les recherches", width=150)
        # self.msg_description_prod.grid(row=1, column=1, sticky=W)

        self.description_prouit_champs = Text(self.labelf_description_prouit, font=(police, taille_police_texte),
                                              width=100,
                                              height=20,
                                              relief=SUNKEN, bd=5)
        self.description_prouit_champs.grid(row=2, column=1, sticky=W)

        self.labelf_prix_modifiable_champs = LabelFrame(self.frame_icone_pro, text="Prix modifiable",
                                                        bg=couleur_sous_fenetre,
                                                        labelanchor=NW, fg=couleur_police,
                                                        bd=bd_widget,
                                                        relief=relief_widget)
        self.labelf_prix_modifiable_champs.grid(row=1, column=1, sticky=EW, columnspan=2, pady=0, )

        self.is_price_reducible_variable = BooleanVar(value=True)
        self.radio_bout_pu_mod_non_champs = Radiobutton(self.labelf_prix_modifiable_champs,
                                                        variable=self.is_price_reducible_variable,
                                                        value=False
                                                        , bg=couleur_sous_fenetre, fg=couleur_police_champs, text="Non",
                                                        width=2
                                                        , selectcolor=couleur_inverse_tree
                                                        , activebackground="blue", anchor=N, height=2)
        self.radio_bout_pu_mod_non_champs.grid(row=1, column=1, sticky=EW)

        self.radio_bout_pu_mod_oui_champs = Radiobutton(self.labelf_prix_modifiable_champs,
                                                        variable=self.is_price_reducible_variable,
                                                        value=True
                                                        , bg=couleur_sous_fenetre, fg=couleur_police_champs, text="Oui",
                                                        anchor=N,
                                                        width=2, height=2
                                                        , selectcolor=couleur_inverse_tree,
                                                        activebackground="blue")
        self.radio_bout_pu_mod_oui_champs.grid(row=1, column=2)

        self.separator = ttk.Separator(self.frame_icone_pro_est, orient=VERTICAL)
        self.separator.grid(row=1, column=0, sticky=NS, padx=1)

        # self.labelf_image_prouit = LabelFrame(self.paned_fen_gestion_produit_sud_est, text="Image produit",
        #                                       bg=couleur_label, fg=couleur_police, labelanchor=N, width=20,
        #                                       font=(police, taille_police_texte), bd=bd_widget, relief=relief_widget)
        # self.paned_fen_gestion_produit_sud_est.add(self.labelf_image_prouit)
        # self.liste_champs_add_prod_stock = [self.nom_founisseur_produit_champs,
        #                                     self.date_expiration_produit_champs,
        #                                     # self.date_expiration_produit_champs,
        #                                     self.rayon_produit_champs,
        #                                     self.id_produit_champs,
        #                                     self.nom_produit_champs,
        #                                     self.grammage_produit_champs,
        #                                     self.unite_grammage_produit_champs,
        #                                     self.categorie_produit_champs,
        #                                     self.marque_produit_champs,
        #                                     self.quantite_debut_stock_produit_champs,
        #                                     self.description_prouit_champs,
        #                                     self.cout_achat_produit_champs,
        #                                     self.prix_vente_produit_champs,
        #                                     self.seuil_commande_produit_champs,
        #                                     self.periode_commande_produit_champs]
        #
        # self.liste_champs_add_prod_stock_a_supp = self.liste_champs_add_prod_stock.copy()

        self.parametre_produit_widget = PageParametreAjoutProduit(self.master,
                                                                  # self.select_default_pu_modifiable,
                                                                  # fonction_interdit_lettre,
                                                                  # self.liste_champs_add_prod_stock_a_supp,
                                                                  # self.nom_founisseur_produit_champs,
                                                                  # self.date_expiration_produit_champs,
                                                                  # self.rayon_produit_champs,
                                                                  # self.id_produit_champs,
                                                                  # self.nom_produit_champs,
                                                                  # self.grammage_produit_champs,
                                                                  # self.unite_grammage_produit_champs,
                                                                  # self.categorie_produit_champs,
                                                                  # self.marque_produit_champs,
                                                                  # self.quantite_debut_stock_produit_champs,
                                                                  # self.description_prouit_champs,
                                                                  # self.cout_achat_produit_champs,
                                                                  # self.prix_vente_produit_champs,
                                                                  # self.seuil_commande_produit_champs,
                                                                  # self.periode_commande_produit_champs,
                                                                  #    self.id_produit
                                                                  )
        # self.img_param_prod = redimension_icone(image_parametre, 20, 20)
        # self.bouton_param_prod = Button(self.frame_icone_pro, text="<<Parametre>>",
        #                                 command=self.parametre_produit_widget.param_prod_open
        #                                 # , height=25
        #                                 , bd=bd_widget,
        #                                 # image=self.img_param_prod
        #                                 )
        # self.bouton_param_prod.grid(row=1, column=5, columnspan=1, sticky=EW)

        # self.bouton_quit_page_prod = Button(self.frame_action_pro, text="<<Quitter>>"
        #                                     # , command=self.quit_page_ajout_prod
        #                                     , bg=couleur_sous_fenetre, width=15)
        # self.bouton_quit_page_prod.grid(row=1, column=1, sticky=EW)

        # self.img_descr_prod = redimension_icone(image_description_prod_stock, 20, 20)
        # self.bouton_descrip_prod = Button(self.frame_icone_pro,
        #                                   # image=self.img_descr_prod,
        #                                   command=self.descr_prod_open,
        #                                   text="Description du produit"
        #                                   # , height=25
        #                                   , bd=bd_widget)
        # self.bouton_descrip_prod.grid(row=1, column=6, columnspan=1, sticky=EW)

        # self.bouton_quit_desc_prod = Button(self.labelf_description_prouit, text="<<Terminer>>",
        #                                     command=lambda: self.descr_prod_quit(0)
        #                                     , height=2, bd=bd_widget, bg=couleur_nuance, fg=fg_nuance)
        # self.bouton_quit_desc_prod.grid(row=3, column=1, sticky=W)

        # img_effece_all_champs = redimension_icone(image_nettoyage_noir, 35, 35)
        bouton_effece_all_champs = Button(self.frame_action_pro, bg=couleur_bouton,
                                          text="Nettoyer", fg=couleur_police,
                                          command=self.clean_all_champs_prod, width=25)
        bouton_effece_all_champs.grid(row=1, column=2, sticky=EW)

        # imag_validp = redimension_icone(image_ajout_bd, 35, 35)
        self.bouton_enregistrer_produit_bd = Button(self.frame_action_pro, text="Enregistrer", bg=couleur_bouton,
                                                    command=lambda: self.save_product(0),
                                                    fg=couleur_police
                                                    , width=25)
        self.bouton_enregistrer_produit_bd.grid(row=1, column=3, sticky=EW)
        # self.imag_retablir = redimension_icone(image_flashback, 35, 35)

        self.bouton_retablir_info_prod = Button(self.frame_icone_pro_est, text="Retablir", bg=couleur_bouton,
                                                # command=self.retablir_modification_prod,
                                                fg=couleur_police
                                                , width=17)
        self.bouton_annul_modif_info_prod = Button(self.frame_icone_pro_est, text="Annuler",
                                                   bg=couleur_bouton, width=17,
                                                   command=self.annuler_modification, fg=couleur_police)
        self.bouton_retablir_info_prod.grid(row=1, column=7)
        self.bouton_annul_modif_info_prod.grid(row=1, column=8)
        self.winfo_toplevel().bind("<Return>", self.save_product)
        self.nom_produit_champs.bind("<FocusOut>", self.verif_product_name)
        self.id_produit_champs.bind("<FocusOut>", self.verif_product_code)

    def verif_product_name(self, event):
        expected_product = Product.find_product_by_name(name=self.nom_produit_champs.get())
        if expected_product:
            self.nom_produit.configure(fg="red", text="Ce nom est déjà utilisé")
        else:
            self.nom_produit.configure(fg="black", text="Nom du produit")

    def verif_product_code(self, event):
        expected_product = Product.get_by_code(product_code=self.id_produit_champs.get())
        if expected_product:
            self.id_produit.configure(fg="red", text="Ce code est déjà utilisé")
        else:
            self.id_produit.configure(fg="black", text="Code du produit")

    @staticmethod
    def generate_product_code(product_code: str, expected_product_category: str, rayon_prod_obtenu: str):
        """Fonction de generation automatique des codes des produits en fonction de la categorie du produit"""
        category_count = Product.get_product_count_by_category_name(expected_product_category)
        if product_code:
            return product_code
        if not expected_product_category:
            messagebox.showerror("Erreur", "Le mode d'IDENTIFICATION AUTOMATQUE requiert la categorie du produit")
            return False
        if len(rayon_prod_obtenu) >= 3:
            rayon_prod_obtenu = rayon_prod_obtenu[0:3]
        if not rayon_prod_obtenu:
            rayon_prod_obtenu = "NR"
        if len(expected_product_category) == 2:
            expected_product_category = expected_product_category + "-"
        elif len(expected_product_category) == 1:
            expected_product_category = expected_product_category + "--"
        else:
            expected_product_category = expected_product_category[0:3]
        if not category_count:
            category_count = "1"
        else:
            category_count = f"{category_count + 1}"
        try:
            product_code = expected_product_category + str(category_count).zfill(4) + rayon_prod_obtenu
            return product_code
        except:
            messagebox.showerror("Erreur",
                                 "Erreur lors de la génération du code du produit; essayez la methode manuelle")
            return False

    def supp_cham_prod_dtock(self):
        self.product_supplier_name_entry.delete(0, END)
        self.product_exp_entry.delete(0, END)
        self.product_exp_entry.insert(0, str(date.today())[:3])
        self.rayon_produit_champs.delete(0, END)
        self.id_produit_champs.delete(0, END)
        self.nom_produit_champs.delete(0, END)
        self.grammage_produit_champs.delete(0, END)
        self.product_grammage_type_entry.delete(0, END)
        self.categorie_produit_champs.delete(0, END)
        self.marque_produit_champs.delete(0, END)
        self.quantite_debut_stock_produit_champs.delete(0, END)
        self.description_prouit_champs.delete("0.0", END)
        self.cout_achat_produit_champs.delete(0, END)
        self.prix_vente_produit_champs.delete(0, END)
        self.seuil_commande_produit_champs.delete(0, END)
        self.periode_commande_produit_champs.delete(0, END)
        # self.label_img_produit.config(image=self.affiche_img)
        # self.label_img_produit.image = self.affiche_img
        self.image_produit.set(image_defaut_produit)

    def clean_all_champs_prod(self):
        """Supprimer les champs d'enregistrement des produits necessaires"""
        self.id_produit_champs.delete(0, END)
        self.nom_produit_champs.delete(0, END)
        self.grammage_produit_champs.delete(0, END)
        self.product_grammage_type_entry.delete(0, END)
        self.categorie_produit_champs.delete(0, END)
        self.quantite_debut_stock_produit_champs.delete(0, END)
        self.marque_produit_champs.delete(0, END)
        self.description_prouit_champs.delete("0.0", END)
        self.cout_achat_produit_champs.delete(0, END)
        self.prix_vente_produit_champs.delete(0, END)
        self.rayon_produit_champs.delete(0, END)
        self.product_gamme_entry.delete(0, END)
        self.product_supplier_name_entry.delete(0, END)
        self.product_exp_entry.delete(0, END)
        self.seuil_commande_produit_champs.delete(0, END)
        self.periode_commande_produit_champs.delete(0, END)

    def save_product(self, event):
        product_name = self.nom_produit_champs.get()
        product_grammage = self.grammage_produit_champs.get()
        product_grammage_type_name = self.product_grammage_type_entry.get()
        product_category_name = self.categorie_produit_champs.get()
        product_brand = self.marque_produit_champs.get()
        product_count = self.quantite_debut_stock_produit_champs.get()
        product_description = self.description_prouit_champs.get("0.0", "end")
        cout_achat_produit_obtenu = self.cout_achat_produit_champs.get()
        prix_vente_produit_obtenu = self.prix_vente_produit_champs.get()
        product_rayon_name = self.rayon_produit_champs.get()
        product_gamme_name = self.product_gamme_entry.get()
        supplier_name = self.product_supplier_name_entry.get()
        product_exp_date = DateTimeService.parse_date(self.product_exp_entry.get())
        stock_limit = self.seuil_commande_produit_champs.get()
        exp_alert_period = self.periode_commande_produit_champs.get()
        if Staff.current_staff is None:
            messagebox.showerror("DEL BLANCO", "Veuillez choisir un utilisateur")
            return
        if not product_name:
            messagebox.showerror("DEL BLANCO", "Le nom du produit est obligatoire")
            return
        if self.id_produit["fg"] == "red":
            messagebox.showerror("DEL BLANCO", "Ce code de produit est déjà utilisé")
            return
        if self.nom_produit["fg"] == "red":
            messagebox.showerror("DEL BLANCO", "Ce nom de produit est déjà utilisé")
            return
        if not prix_vente_produit_obtenu:
            messagebox.showerror("DEL BLANCO", "Le prix de vente du produit est obligatoire")
            return
        if not cout_achat_produit_obtenu:
            messagebox.showerror("DEL BLANCO", "Le cout d'achat du produit est obligatoire")
            return
        if not product_count:
            messagebox.showerror("DEL BLANCO", "Veuillez entrer une quantité de début de stock")
            return
        if product_exp_date is not None:
            product_exp_date = parser.parse(product_exp_date).date()
        if product_exp_date is not None and date.today() >= product_exp_date:
            messagebox.showerror("Erreur",
                                 "La date d'expiration doit etre superieure à la date d'aujourd'hui !")
            self.product_exp_entry.focus_set()
            return
        unit_price = float(prix_vente_produit_obtenu)
        unit_coast = float(cout_achat_produit_obtenu)
        if unit_price < unit_coast:
            messagebox.showerror("Erreur", "Le prix de vente du produit doit etre superieur à son cout d'achat")
            return
        product_code = self.generate_product_code(
            expected_product_category=product_category_name,
            product_code=self.id_produit_champs.get(),
            rayon_prod_obtenu=product_rayon_name)
        if not product_code:
            return
        product_category = Category.get_by_name(product_category_name)
        if product_category_name and product_category is None:
            category_id = Category.create(name=product_category_name)
            if category_id:
                product_category = Category.get_by_id(category_id=category_id)
        product_rayon = Rayon.get_by_name(product_rayon_name)
        if product_rayon_name and product_rayon is None:
            rayon_id = Rayon.create(name=product_rayon_name)
            if rayon_id:
                product_rayon = Rayon.get_by_id(rayon_id=rayon_id)
        product_gamme = Gamme.get_by_name(product_gamme_name)
        if product_gamme_name and product_gamme is None:
            gamme_id = Gamme.create(name=product_gamme_name)
            if gamme_id:
                product_gamme = Gamme.get_by_id(gamme_id)
        product_grammage_type = GrammageType.get_by_name(product_grammage_type_name)
        if product_grammage_type_name and product_grammage_type is None:
            if GrammageType.create(name=product_grammage_type_name):
                product_grammage_type = GrammageType.get_last()

        product_id = Product(code=product_code,
                             name=product_name,
                             grammage=float(product_grammage) if product_grammage else None,
                             brand=product_brand,
                             description=product_description,
                             stock_limit=int(stock_limit) if stock_limit else 5,
                             category=product_category,
                             rayon=product_rayon,
                             exp_alert_period=int(exp_alert_period) if exp_alert_period else 6,
                             grammage_type=product_grammage_type,
                             gamme=product_gamme,
                             is_price_reducible=self.is_price_reducible_variable.get()
                             ).save_to_db()
        product_count = int(product_count)
        saved_product = Product.get_by_id(product_id=product_id)
        first_supply = Supply(product_count=product_count,
                              product_count_rest=product_count,
                              unit_price=unit_price,
                              unit_coast=unit_coast,
                              product=saved_product,
                              expiration_date=product_exp_date,
                              saver_staff=Staff.current_staff,
                              daily=Exercise.get_current_exercise()
                              ).save_to_db()
        for product_image in self.images_widget.images:
            product_image.path = product_image.real_path.split("/")[-1]
            product_image.product = saved_product
        ProductImage.save_many_to_db(self.images_widget.images)
        for product_image in self.images_widget.images:
            ImageService.save_from_local("product", product_image.real_path)
        self.clean_all_champs_prod()
        messagebox.showinfo("DEL BLANCO", "Produit enregistré avec succès")

    #
    #     statut_mode_id = select_setting("id_auto_prod")
    #     if statut_mode_id == "oui":
    #         id_produit_obtenu = self.generateur_id_prod()
    #         if id_produit_obtenu == 0:
    #             return
    #     if prix_vente_produit_obtenu.endswith(".0"):
    #         prix_vente_produit_obtenu = prix_vente_produit_obtenu.replace(".0", "")
    #     if cout_achat_produit_obtenu.endswith(".0"):
    #         cout_achat_produit_obtenu = cout_achat_produit_obtenu.replace(".0", "")
    #     if not seuil_commande_produit_obtenue:
    #         seuil_commande_produit_obtenue = 0
    #     if not periode_commande_produit_obtenue:
    #         periode_commande_produit_obtenue = 0
    #
    #     if date_expiration_produit_obtenue == str(date.today())[0:3] or not date_expiration_produit_obtenue:
    #         date_expiration_produit_obtenue = "0000-00-00"
    #     if id_produit_obtenu == "" and nom_produit_obtenue == "" \
    #             and cout_achat_produit_obtenu == "" and prix_vente_produit_obtenu == "" and grammage_produit_obtenu == "" \
    #             and unite_grammage_produit_obtenue == "" and categorie_produit_obtenue == "" and marque_produit_obtenue == "" \
    #             and quantite_debut_stock_produit_obtenue == "" and rayon_produit_obtenue == "":
    #         messagebox.showerror(title="Erreur", message="Vous devez renseigner les données")
    #         return
    #     elif id_produit_obtenu == "" or nom_produit_obtenue == "" or quantite_debut_stock_produit_obtenue == "" \
    #             or cout_achat_produit_obtenu == "" or prix_vente_produit_obtenu == "":
    #         messagebox.showerror(title="Erreur", message="Les champs comportant les étoiles* sont obligatoires")
    #         return
    #     elif grammage_produit_obtenu == "" and unite_grammage_produit_obtenue != "":
    #         messagebox.showerror(title="Erreur", message="Vous devez indiquer le grammage")
    #         return
    #     elif grammage_produit_obtenu != "" and unite_grammage_produit_obtenue == "":
    #         messagebox.showerror(title="Erreur", message="Vous devez indiquer l'unité du grammage")
    #         return
    #     elif int(prix_vente_produit_obtenu) <= int(cout_achat_produit_obtenu):
    #         messagebox.showerror(title="Erreur",
    #                              message="Le prix de vente doit etre strictement superieur au cout d'achat")
    #         return
    #     else:
    #         if self.variable_control_enregis_modifprod.get():
    #             """Connexion à la base de donnees pour l'enregistrement du produit"""
    #             ma_base_donnee = connexion_bd_mysql()
    #             mise_a_jour_produit = ma_base_donnee.cursor()
    #             try:
    #                 mise_a_jour_produit.execute(
    #                     f"UPDATE `bd_gestion_del_blanco`.`produit` SET `id_produit` = '{id_produit_obtenu}', "
    #                     f"`designation_produit` = '{nom_produit_obtenue}', `grammage_produit` = '{grammage_produit_obtenu}', "
    #                     f"`unite_gramage_produit` = '{unite_grammage_produit_obtenue}', "
    #                     f"`categorie_produit` = '{categorie_produit_obtenue}', "
    #                     f"`quantite_stock_produit` = '{quantite_debut_stock_produit_obtenue}', "
    #                     f"`description_produit` = '{description_produit_obtenue}', "
    #                     f"`cout_achat_produit` = '{cout_achat_produit_obtenu}', "
    #                     f"`prix_vente_produit` = '{prix_vente_produit_obtenu}', `rayon_produit` "
    #                     f"= '{rayon_produit_obtenue}', `image_produit` = '{photo_produit_obtenue}' WHERE "
    #                     f"(`id_produit` = '{self.var_flex_id_prod_a_modi.get()}', creatAt = current_date());")
    #                 if seuil_commande_produit_obtenue:
    #                     mise_a_jour_produit.execute(f"UPDATE `bd_gestion_del_blanco`.`produit` SET `seuil_commande` "
    #                                                 f"= '{seuil_commande_produit_obtenue}' WHERE (`id_produit` = "
    #                                                 f"'{id_produit_obtenu}');")
    #                 else:
    #                     mise_a_jour_produit.execute(f"UPDATE `bd_gestion_del_blanco`.`produit` SET `seuil_commande` "
    #                                                 f"= '{select_defaut_colonne('seuil_commande', 'produit')}' WHERE (`id_produit` = "
    #                                                 f"'{id_produit_obtenu}');")
    #                 if periode_commande_produit_obtenue:
    #                     mise_a_jour_produit.execute(
    #                         f"UPDATE `bd_gestion_del_blanco`.`produit` SET `duree_limite_commande` "
    #                         f"= '{periode_commande_produit_obtenue}' WHERE (`id_produit` = '{id_produit_obtenu}');")
    #                 else:
    #                     mise_a_jour_produit.execute(
    #                         f"UPDATE `bd_gestion_del_blanco`.`produit` SET `duree_limite_commande` "
    #                         f"= '{select_defaut_colonne('duree_limite_commande', 'produit')}' WHERE (`id_produit` = '{id_produit_obtenu}');")
    #
    #             except:
    #                 if self.var_flex_id_prod_a_modi.get() != id_produit_obtenu:
    #                     mise_a_jour_produit.execute(f"SELECT id_produit FROM produit")
    #                     prod_id_duplike = mise_a_jour_produit.fetchall()
    #                     for idp in prod_id_duplike:
    #                         if id_produit_obtenu.upper() == idp[0].upper():
    #                             mise_a_jour_produit.execute(
    #                                 f"SELECT designation_produit FROM produit WHERE id_produit = '{idp[0]}'")
    #                             prod_id_dupli = mise_a_jour_produit.fetchone()
    #                             messagebox.showerror("Erreur",
    #                                                  f"Cet identifiant a déjà été utilisé pour {prod_id_dupli[0]}")
    #                             self.id_produit_champs.focus_set()
    #                             return
    #                 mise_a_jour_produit.execute(f"SELECT designation_produit FROM produit")
    #                 prod_id_duplik = mise_a_jour_produit.fetchall()
    #                 for prod in prod_id_duplik:
    #                     if nom_produit_obtenue.upper() == prod[0].upper():
    #                         mise_a_jour_produit.execute(f"SELECT id_produit, categorie_produit FROM produit WHERE "
    #                                                     f"designation_produit = '{prod[0]}'")
    #                         carct_duplik = mise_a_jour_produit.fetchone()
    #                         messagebox.showerror("Erreur", f"Ce nom a déjà été utilisé pour un(e) {carct_duplik[1]} \n"
    #                                                        f"Identifiant: {carct_duplik[0]}")
    #                         self.id_produit_champs.focus_set()
    #                         return
    #                 messagebox.showerror("Erreur", "Erreur inconnue")
    #                 return
    #             ma_base_donnee.commit()
    #             ma_base_donnee.close()
    #             self.clean_champs_prod()
    #             self.date_expiration_produit_champs.config(state=NORMAL)
    #             # self.label_img_produit.config(image=self.affiche_img)
    #             # self.label_img_produit.image = self.affiche_img
    #             self.image_produit.set(image_defaut_produit)
    #             messagebox.showinfo(title=nom_ets,
    #                                 message=f"Modifications enregistés avec succès")
    #             # bouton_enregistrer_produit_bd.config(text="", compound=LEFT)
    #             self.bouton_retablir_info_prod.grid_forget()
    #             self.bouton_annul_modif_info_prod.grid_forget()
    #             self.nom_produit_champs.focus_set()
    #             self.variable_control_enregis_modifprod.set(0)
    #             self.tableau_produit.affiche_produit_magazin()
    #             # self.affiche_liste_approv()
    #             # self.stock_critic_table.remplir_treeviiew_stock_critic()
    #             return
    #
    #         """Connexion à la base de donnees pour l'enregistrement du produit"""
    #         ma_base_donnee = connexion_bd_mysql()
    #         selection_id_produit = ma_base_donnee.cursor()
    #         """Selectionner la liste des identifiants de produit deja existant"""
    #         selection_id_produit.execute(f"SELECT upper(id_produit) from produit;")
    #         list_id_produit = []
    #         for id in selection_id_produit:
    #             list_id_produit += [id[0]]
    #
    #         """Selectionner la liste des designations de produit deja existant"""
    #         selection_designstion_produit = ma_base_donnee.cursor()
    #         selection_designstion_produit.execute(f"SELECT upper(designation_produit) from produit;")
    #         list_designstion_produit = []
    #         for designation in selection_designstion_produit:
    #             list_designstion_produit += [designation[0]]
    #         ma_base_donnee.close()
    #
    #         """Verifier si l"identifiant existe deja dans la base de donnees"""
    #
    #         if id_produit_obtenu.upper() in list_id_produit:
    #             ma_base_donnee = connexion_bd_mysql()
    #             selection_produit = ma_base_donnee.cursor()
    #             """Selectionner la liste des identifiants de produit deja existant"""
    #             selection_produit.execute(
    #                 f"SELECT designation_produit from produit WHERE id_produit = '{id_produit_obtenu}';")
    #             produit_existant = []
    #             for p in selection_produit:
    #                 produit_existant += [p[0]]
    #             ma_base_donnee.close()
    #             messagebox.showerror("Erreur", f"Vous avez déjà utilisé cet identifiant pour {produit_existant[0]}\n"
    #                                            f"Vous devez le modifier")
    #             self.id_produit_champs.focus_set()
    #
    #         else:
    #             """Verifier si le nom existe deja dans la base de donnees"""
    #             if nom_produit_obtenue.upper() in list_designstion_produit:
    #                 messagebox.showerror("Erreur", "Vous avez déjà utilisé ce nom pour un autre produit")
    #                 self.nom_produit_champs.focus_set()
    #             else:
    #                 if date_expiration_produit_obtenue and len(date_expiration_produit_obtenue) < 10:
    #                     messagebox.showerror(title="Erreur",
    #                                          message=f"La date d'expiration est incomplète, voici un exemple: {date.today()}")
    #                     self.date_expiration_produit_champs.focus_set()
    #                 else:
    #                     # try:
    #                     if 9 == 9:
    #                         try:
    #                             if date_expiration_produit_obtenue != "0000-00-00":
    #                                 daaa = parser.parse(date_expiration_produit_obtenue)
    #                         except:
    #                             messagebox.showerror("Erreur",
    #                                                  "La date d'expiration est incorrecte!")
    #                             self.date_expiration_produit_champs.focus_set()
    #                             return
    #                         if date_expiration_produit_obtenue != "0000-00-00" and date.today() >= parser.parse(
    #                                 date_expiration_produit_obtenue).date():
    #                             messagebox.showerror("Erreur",
    #                                                  "La date d'expiration doit etre superieure à la date d'aujourd'hui !")
    #                             self.date_expiration_produit_champs.focus_set()
    #                             return
    #                         # directory = os.path.join(os.getcwd(), os.path.join("image_produit", nom_produit_obtenue))
    #                         # try:
    #                         #     os.mkdir(directory)
    #                         # except:
    #                         #     pass
    #                         # list_img_all_dir = []
    #                         ma_base_donnee = connexion_bd_mysql()
    #                         enregistrer_produit = ma_base_donnee.cursor()
    #                         # for img in image_produit.get().split("??"):
    #                         #     imagesave = PIL.Image.open(img)
    #                         #     all_dir = os.path.join(directory, f"{id_produit_obtenu}photo.png")
    #                         #     imagesave.save(all_dir)
    #                         #     all_dir = all_dir.replace("\\", r"/")
    #                         #     list_img_all_dir.append(all_dir)
    #                         """Inserer les donnees dans la table des produits pour un debut de stock"""
    #                         enregistrer_produit.execute(
    #                             f"INSERT INTO `bd_gestion_del_blanco`.`produit` (`id_produit`, `designation_produit`, "
    #                             f"`grammage_produit`, `unite_gramage_produit`, `categorie_produit`, `marque_produit`, "
    #                             f" `quantite_stock_produit`, `description_produit`,"
    #                             f"`cout_achat_produit`, `prix_vente_produit`, `rayon_produit`, `image_produit`, `prix_modifiable`) VALUES "
    #                             f"('{id_produit_obtenu}', '{nom_produit_obtenue}', '{grammage_produit_obtenu}', "
    #                             f"'{unite_grammage_produit_obtenue}', '{categorie_produit_obtenue}',"
    #                             f"'{marque_produit_obtenue}', '{quantite_debut_stock_produit_obtenue}',"
    #                             f" '{description_produit_obtenue}', '{cout_achat_produit_obtenu}', '{prix_vente_produit_obtenu}',"
    #                             f"'{rayon_produit_obtenue}', '{self.image_produit.get()}', '{self.variable_control_prix_modifiabl.get()}');")
    #                         if seuil_commande_produit_obtenue:
    #                             enregistrer_produit.execute(
    #                                 f"UPDATE `bd_gestion_del_blanco`.`produit` SET `seuil_commande` "
    #                                 f"= '{seuil_commande_produit_obtenue}' WHERE (`id_produit` = "
    #                                 f"'{id_produit_obtenu}');")
    #                         if periode_commande_produit_obtenue:
    #                             enregistrer_produit.execute(
    #                                 f"UPDATE `bd_gestion_del_blanco`.`produit` SET `duree_limite_commande` "
    #                                 f"= '{periode_commande_produit_obtenue}' WHERE (`id_produit` = '{id_produit_obtenu}');")
    #                         if not date_expiration_produit_obtenue:
    #                             date_expiration_produit_obtenue = "0000-00-00"
    #                         """Enregister ces memes donnees comme approvisionnement"""
    #                         enregistrer_produit.execute(
    #                             f"INSERT INTO `bd_gestion_del_blanco`.`approvisionnement` (`nom_produit_approv`, "
    #                             f"`quantite_produit_approv`, `quantite_produit_approv_invar`, `pu_produit_approv`, `cout_unitaire_approv`"
    #                             f", `fournisseur_approv`, `date_approv`, `date_expiration_produit`) VALUES ('{nom_produit_obtenue}', "
    #                             f"'{quantite_debut_stock_produit_obtenue}', '{quantite_debut_stock_produit_obtenue}', '{prix_vente_produit_obtenu}',"
    #                             f" '{cout_achat_produit_obtenu}', "
    #                             f"'{nom_fournisseur_obtenue}','{datetime.now()}', '{date_expiration_produit_obtenue}');")
    #
    #                         ma_base_donnee.commit()
    #                         ma_base_donnee.close()
    #                         self.clean_champs_prod()
    #                         self.date_expiration_produit_champs.insert(0, str(date.today())[0:3])
    #                         self.photo_produit.image_prod_clear()
    #                         messagebox.showinfo(title=nom_ets,
    #                                             message=f"{nom_produit_obtenue} enregisté avec succès")
    #                         self.tableau_produit.affiche_produit_magazin()
    #                         self.nom_produit_champs.focus_set()
    #                         # self.stock_critic_table.remplir_treeviiew_stock_critic()
    #                     # except:
    #                     #     messagebox.showerror("Erreur",
    #                     #                          "Rassurez-vous que les champs des quantités et des prix sont des chiffres et non des lettres ")
    #                     #     fenetre_gestion_produit.focus_force()

    def clean_champs_prod(self):
        """Supprimer les champs d'enregistrement des produits necessaires"""
        for cham in self.liste_champs_add_prod_stock_a_supp:
            try:
                cham.delete(0, END)
            except:
                cham.delete("0.0", END)

    def descr_prod_open(self):
        """Ouvrir la page de description des produits lors de l'ajout"""
        self.label_frame_descript_prod_pop.place(x=190, y=50)

    def deplace_pup_descr_prod(self, event):
        self.label_frame_descript_prod_pop.place_configure(x=self.master.winfo_pointerx() - 30,
                                                           y=self.master.winfo_pointery() - 50)

    def descr_prod_quit(self, event):
        """Ouvrir la page de description des produits lors de l'ajout"""
        self.label_frame_descript_prod_pop.place_forget()

    # def modifier_produit_info(self):
    #     """Modifier les caracteriistiques d'un produit"""
    #     approv_selectionne = self.tableau_produit.tableau_produit.selection()
    #     if len(approv_selectionne) == 1:
    #         ligne_select_magazin = self.tableau_produit.tableau_produit.item(approv_selectionne[0])
    #         valeur_ligne_select_magazin = ligne_select_magazin["values"]
    #
    #         ma_base_donnee = connexion_bd_mysql()
    #         conexion_magazin = ma_base_donnee.cursor()
    #         conexion_magazin.execute(f"SELECT * from produit WHERE id_produit = '{valeur_ligne_select_magazin[0]}';")
    #         liste_produit_magazin = conexion_magazin.fetchone()
    #         ma_base_donnee.close()
    #
    #         self.id_produit_champs.delete(0, END)
    #         self.nom_produit_champs.delete(0, END)
    #         self.categorie_produit_champs.delete(0, END)
    #         self.marque_produit_champs.delete(0, END)
    #         self.cout_achat_produit_champs.delete(0, END)
    #         self.prix_vente_produit_champs.delete(0, END)
    #         self.quantite_debut_stock_produit_champs.delete(0, END)
    #         self.rayon_produit_champs.delete(0, END)
    #         self.grammage_produit_champs.delete(0, END)
    #         self.unite_grammage_produit_champs.delete(0, END)
    #         self.seuil_commande_produit_champs.delete(0, END)
    #         self.periode_commande_produit_champs.delete(0, END)
    #         self.description_prouit_champs.delete("0.0", END)
    #         # self.label_img_produit.config(image=self.affiche_img)
    #         # self.label_img_produit.image = self.affiche_img
    #
    #         try:
    #             self.id_produit_champs.insert(0, liste_produit_magazin[0])
    #         except:
    #             pass
    #         try:
    #             self.nom_produit_champs.insert(0, liste_produit_magazin[1])
    #         except:
    #             pass
    #         try:
    #             self.categorie_produit_champs.insert(0, liste_produit_magazin[4])
    #         except:
    #             pass
    #         try:
    #             self.marque_produit_champs.insert(0, liste_produit_magazin[5])
    #         except:
    #             pass
    #         try:
    #             if str(liste_produit_magazin[8]).endswith(".0"):
    #                 self.cout_achat_produit_champs.insert(0, f"{liste_produit_magazin[8]:.0f}")
    #             else:
    #                 self.cout_achat_produit_champs.insert(0, liste_produit_magazin[8])
    #         except:
    #             pass
    #         try:
    #             if str(liste_produit_magazin[9]).endswith(".0"):
    #                 self.prix_vente_produit_champs.insert(0, f"{liste_produit_magazin[9]:.0f}")
    #             else:
    #                 self.prix_vente_produit_champs.insert(0, liste_produit_magazin[9])
    #         except:
    #             pass
    #         try:
    #             self.quantite_debut_stock_produit_champs.insert(0, liste_produit_magazin[6])
    #         except:
    #             pass
    #         try:
    #             self.rayon_produit_champs.insert(0, liste_produit_magazin[10])
    #         except:
    #             pass
    #         try:
    #             self.grammage_produit_champs.insert(0, liste_produit_magazin[2])
    #         except:
    #             pass
    #         try:
    #             self.unite_grammage_produit_champs.insert(0, liste_produit_magazin[3])
    #         except:
    #             pass
    #         try:
    #             self.seuil_commande_produit_champs.insert(0, liste_produit_magazin[12])
    #         except:
    #             pass
    #         try:
    #             self.periode_commande_produit_champs.insert(0, liste_produit_magazin[13])
    #         except:
    #             pass
    #         try:
    #             self.description_prouit_champs.insert("0.0", liste_produit_magazin[7])
    #         except:
    #             pass
    #         try:
    #             image = PIL.Image.open(liste_produit_magazin[11])
    #             image.thumbnail((200, 200))
    #             affiche_img = ImageTk.PhotoImage(image)
    #             # self.label_img_produit.config(image=affiche_img)
    #             # self.label_img_produit.image = affiche_img
    #             self.image_produit.set(liste_produit_magazin[11])
    #         except:
    #             pass
    #         # bouton_enregistrer_produit_bd.config(text="Enregistrer les modifications", compound=RIGHT)
    #         self.frame_icone_pro_est.grid(row=15, column=2, sticky=EW)
    #         self.variable_control_enregis_modifprod.set(1)
    #         self.date_expiration_produit_champs.config(state=DISABLED)
    #         self.nom_founisseur_produit_champs.config(state=DISABLED)
    #         self.quantite_debut_stock_produit_champs.config(state=DISABLED)
    #         self.cout_achat_produit_champs.config(state=DISABLED)
    #         self.prix_vente_produit_champs.config(state=DISABLED)
    #         self.var_flex_id_prod_a_modi.set(valeur_ligne_select_magazin[0])
    #         liste_produit_magazinnew = []
    #         for pdo in liste_produit_magazin:
    #             liste_produit_magazinnew += [str(pdo)]
    #         self.liste_caract_prod_a_mod.set("?".join(liste_produit_magazinnew))
    #     else:
    #         messagebox.showerror("Erreur", "Vous ne pouvez éditer qu'un seul produit à la fois")

    # def retablir_modification_prod(self):
    #     """Retablir les modifications que l'utilisateur a effectue dans les caracteristiques du produit"""
    #     liste_produit_magazin = self.liste_caract_prod_a_mod.get().split("?")
    #     self.id_produit_champs.delete(0, END)
    #     self.nom_produit_champs.delete(0, END)
    #     self.categorie_produit_champs.delete(0, END)
    #     self.marque_produit_champs.delete(0, END)
    #     self.cout_achat_produit_champs.delete(0, END)
    #     self.prix_vente_produit_champs.delete(0, END)
    #     self.quantite_debut_stock_produit_champs.delete(0, END)
    #     self.rayon_produit_champs.delete(0, END)
    #     self.grammage_produit_champs.delete(0, END)
    #     self.unite_grammage_produit_champs.delete(0, END)
    #     self.seuil_commande_produit_champs.delete(0, END)
    #     self.periode_commande_produit_champs.delete(0, END)
    #     self.description_prouit_champs.delete("0.0", END)
    #
    #     try:
    #         self.id_produit_champs.insert(0, liste_produit_magazin[0])
    #     except:
    #         pass
    #     try:
    #         self.nom_produit_champs.insert(0, liste_produit_magazin[1])
    #     except:
    #         pass
    #     try:
    #         self.categorie_produit_champs.insert(0, liste_produit_magazin[4])
    #     except:
    #         pass
    #     try:
    #         self.marque_produit_champs.insert(0, liste_produit_magazin[5])
    #     except:
    #         pass
    #     try:
    #         if str(liste_produit_magazin[8]).endswith(".0"):
    #             self.cout_achat_produit_champs.insert(0, f"{int(liste_produit_magazin[8].replace('.0', ''))}")
    #         else:
    #             self.cout_achat_produit_champs.insert(0, liste_produit_magazin[8])
    #     except:
    #         pass
    #     try:
    #         if str(liste_produit_magazin[9]).endswith(".0"):
    #             self.prix_vente_produit_champs.insert(0, f"{int(liste_produit_magazin[9].replace('.0', ''))}")
    #
    #         else:
    #             self.prix_vente_produit_champs.insert(0, liste_produit_magazin[9])
    #     except:
    #         pass
    #     try:
    #         self.quantite_debut_stock_produit_champs.insert(0, liste_produit_magazin[6])
    #     except:
    #         pass
    #     try:
    #         self.rayon_produit_champs.insert(0, liste_produit_magazin[10])
    #     except:
    #         pass
    #     try:
    #         self.grammage_produit_champs.insert(0, liste_produit_magazin[2])
    #     except:
    #         pass
    #     try:
    #         self.unite_grammage_produit_champs.insert(0, liste_produit_magazin[3])
    #     except:
    #         pass
    #     try:
    #         self.seuil_commande_produit_champs.insert(0, liste_produit_magazin[12])
    #     except:
    #         self.periode_commande_produit_champs.insert(0, liste_produit_magazin[12])
    #     try:
    #         self.description_prouit_champs.insert("0.0", liste_produit_magazin[7])
    #     except:
    #         pass
    #     try:
    #         image = PIL.Image.open(liste_produit_magazin[11])
    #         image.thumbnail((200, 200))
    #         affiche_img = ImageTk.PhotoImage(image)
    #         # self.label_img_produit.config(image=affiche_img)
    #         # self.label_img_produit.image = affiche_img
    #         image_defaut_produit = liste_produit_magazin[11]
    #         self.image_produit.set(liste_produit_magazin[11])
    #     except:
    #         pass

    def annuler_modification(self):
        """Annuler l'action de modification engagé par l'utilisateur"""
        self.clean_champs_prod()
        self.variable_control_enregis_modifprod.set(0)
        self.var_flex_id_prod_a_modi.set("")
        self.frame_icone_pro_est.grid_forget()
        self.product_exp_entry.config(state=NORMAL)
        # bouton_enregistrer_produit_bd.config(text="", compound=RIGHT)
        # label_img_produit.config(image=affiche_img)
        # label_img_produit.image = affiche_img
        # image_produit = image_defaut_produit

    # def sugerer_categorie_produit(self):
    #     """Prend en parametre une categorie ou son debut, recherche dans la base de donnees et retourne la liste
    #     des elements qui commencent par celui-ci"""
    #     self.categorie_produit_champs.config(values=select_categorie_produit(self.categorie_produit_champs.get()))
    #
    # def sugerer_marque_produit(self):
    #     """Prend en parametre une marque ou son debut, recherche dans la base de donnees et retourne la liste
    #     des elements qui commencent par celle-ci"""
    #     self.marque_produit_champs.config(values=select_marque_produit(self.marque_produit_champs.get()))

    # def sugerer_nom_fournisseur(self):
    #     """Prend en parametre une marque ou son debut, recherche dans la base de donnees et retourne la liste
    #     des elements qui commencent par celle-ci"""
    #     self.nom_founisseur_produit_champs.config(
    #         values=select_nom_fournisseur(self.nom_founisseur_produit_champs.get()))
