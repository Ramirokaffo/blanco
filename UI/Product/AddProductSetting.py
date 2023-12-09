from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter import *

from datetime import date

from STATIC.ConstantFile import *


class PageParametreAjoutProduit:

    def __init__(self, master,
                 # select_default_pu_modifiable,
                 # fonction_interdit_lettre,
                 # liste_champs_add_prod_stock_a_supp,
                 # nom_founisseur_produit_champs,
                 # date_expiration_produit_champs,
                 # rayon_produit_champs,
                 # id_produit_champs,
                 # nom_produit_champs,
                 # grammage_produit_champs,
                 # unite_grammage_produit_champs,
                 # categorie_produit_champs,
                 # marque_produit_champs,
                 # quantite_debut_stock_produit_champs,
                 # description_prouit_champs,
                 # cout_achat_produit_champs,
                 # prix_vente_produit_champs,
                 # seuil_commande_produit_champs,
                 # periode_commande_produit_champs,
                 # id_produit
                 ):
        # self.id_produit = id_produit
        # self.select_default_pu_modifiable = select_default_pu_modifiable
        # self.nom_founisseur_produit_champs= nom_founisseur_produit_champs
        # self.date_expiration_produit_champs = date_expiration_produit_champs
        # self.liste_champs_add_prod_stock_a_supp = liste_champs_add_prod_stock_a_supp
        # self.rayon_produit_champs = rayon_produit_champs
        # self.id_produit_champs = id_produit_champs
        # self.nom_produit_champs = nom_produit_champs
        # self.grammage_produit_champs = grammage_produit_champs
        # self.unite_grammage_produit_champs = unite_grammage_produit_champs
        # self.categorie_produit_champs = categorie_produit_champs
        # self.marque_produit_champs = marque_produit_champs
        # self.quantite_debut_stock_produit_champs = quantite_debut_stock_produit_champs
        # self.description_prouit_champs = description_prouit_champs
        # self.cout_achat_produit_champs = cout_achat_produit_champs
        # self.prix_vente_produit_champs = prix_vente_produit_champs
        # self.seuil_commande_produit_champs = seuil_commande_produit_champs
        # self.periode_commande_produit_champs = periode_commande_produit_champs
        # self.produit_table_service = ProduitTableService()

        self.master = master
        self.label_frame_param_prod = LabelFrame(self.master, labelanchor=N,
                                                 bg=couleur_sous_fenetre, fg=couleur_police, bd=bd_widget + 5,
                                                 relief=RIDGE)
        self.labelf_parametre_prouit = LabelFrame(self.label_frame_param_prod, text="Parametre par defaut produit",
                                                  bg=couleur_label, fg=couleur_police, labelanchor=N, width=20,
                                                  font=(police, taille_police_texte), bd=bd_widget,
                                                  relief=relief_widget)
        self.labelf_parametre_prouit.grid(row=1, column=1)

        self.labelf_spinbox_seuil_cmd = LabelFrame(self.labelf_parametre_prouit, bg=couleur_sous_fenetre,
                                                   fg=couleur_police
                                                   , text="Seuil d'alerte par defaut", labelanchor=N, bd=bd_widget,
                                                   relief=relief_widget)
        self.labelf_spinbox_seuil_cmd.grid(row=1, column=1, sticky=EW, ipadx=11)

        self.labelf_spinbox_palerte_cmd = LabelFrame(self.labelf_parametre_prouit, bg=couleur_sous_fenetre,
                                                     fg=couleur_police
                                                     , text="Periode d'alerte par defaut", labelanchor=N, bd=bd_widget,
                                                     relief=relief_widget)
        self.labelf_spinbox_palerte_cmd.grid(row=2, column=1, sticky=EW, ipadx=11)

        self.labelf_type_id_prod = LabelFrame(self.labelf_parametre_prouit, bg=couleur_sous_fenetre, fg=couleur_police
                                              , text="Mode d'identification des produits", labelanchor=N, bd=bd_widget,
                                              relief=relief_widget)
        self.labelf_type_id_prod.grid(row=3, column=1, sticky=EW)

        self.labelf_prix_modifiable = LabelFrame(self.labelf_parametre_prouit, bg=couleur_sous_fenetre,
                                                 fg=couleur_police
                                                 , text="Modifiabilité des prix lors des ventes", labelanchor=N,
                                                 bd=bd_widget,
                                                 relief=relief_widget)
        self.labelf_prix_modifiable.grid(row=4, column=1, sticky=EW)

        self.bouton_quit_param_prod = Button(self.label_frame_param_prod, text="<<Terminer>>",
                                             command=lambda: self.param_prod_quit(0)
                                             , height=2, bd=bd_widget, bg=couleur_nuance, fg=fg_nuance)
        self.bouton_quit_param_prod.grid(row=16, column=1, columnspan=1, sticky=EW)

        self.spinbox_defaut_seuil_cmd = Spinbox(self.labelf_spinbox_seuil_cmd, from_=0, to=50, wrap=True, bd=bd_widget,
                                                relief=relief_widget,
                                                command=self.affiche_bout_ok_seuil_cmd,
                                                increment=5, validate="key",
                                                # validatecommand=(fonction_interdit_lettre, "%S")
                                                )
        self.spinbox_defaut_seuil_cmd.grid(row=1, column=1, columnspan=2)
        self.spinbox_defaut_seuil_cmd.delete(0, END)
        # self.spinbox_defaut_seuil_cmd.insert(0, select_defaut_colonne("seuil_commande", "produit"))
        self.label_defaut_seuil_cmd = Label(self.labelf_spinbox_seuil_cmd, text="Unité", bg=couleur_sous_fenetre,
                                            fg=couleur_police
                                            , bd=bd_widget, relief=relief_widget)
        self.label_defaut_seuil_cmd.grid(row=1, column=2)
        self.bouton_defaut_seuil_cmd = Button(self.labelf_spinbox_seuil_cmd, text="ok", bg=couleur_bouton,
                                              fg=couleur_police,
                                              # command=self.save_seuil_cmd,
                                              bd=bd_widget, relief=relief_widget)
        self.bouton_defaut_seuil_cmd_annul = Button(self.labelf_spinbox_seuil_cmd, text="Annuler", bg=couleur_bouton,
                                                    fg=couleur_police,
                                                    command=self.annul_mod_seuil_cmd, bd=bd_widget,
                                                    relief=relief_widget)

        self.spinbox_defaut_periode_cmd = Spinbox(self.labelf_spinbox_palerte_cmd, from_=1, to=12, wrap=True,
                                                  command=self.affiche_bout_ok_duree_cmd, bd=bd_widget,
                                                  relief=relief_widget
                                                  , validate="key",
                                                  # validatecommand=(fonction_interdit_lettre, "%S")
                                                  )
        self.spinbox_defaut_periode_cmd.grid(row=1, column=1, columnspan=2)
        self.spinbox_defaut_periode_cmd.delete(0, END)
        # self.spinbox_defaut_periode_cmd.insert(0, select_defaut_colonne("duree_limite_commande", "produit"))
        self.label_defaut_periode_cmd = Label(self.labelf_spinbox_palerte_cmd, text="Mois", bg=couleur_sous_fenetre,
                                              fg=couleur_police
                                              , bd=bd_widget, relief=relief_widget)
        self.label_defaut_periode_cmd.grid(row=1, column=2)
        self.bouton_defaut_periode_cmd = Button(self.labelf_spinbox_palerte_cmd, text="ok", bg=couleur_bouton,
                                                fg=couleur_police,
                                                # command=self.save_duree_limit_cmd,
                                                bd=bd_widget, relief=relief_widget)
        self.bouton_defaut_periode_cmd_annul = Button(self.labelf_spinbox_palerte_cmd, text="Annuler",
                                                      bg=couleur_bouton,
                                                      fg=couleur_police, command=self.annul_mod_duree_cmd, bd=bd_widget,
                                                      relief=relief_widget)
        self.valeur_defaut_seuil_a_mod = StringVar()
        self.valeur_defaut_periode_a_mod = StringVar()
        self.valeur_defaut_seuil_a_mod.set(self.spinbox_defaut_seuil_cmd.get())
        self.valeur_defaut_periode_a_mod.set(self.spinbox_defaut_periode_cmd.get())

        self.variable_control_type_id_prod = StringVar()
        self.radio_bout_type_id_manuel = Radiobutton(self.labelf_type_id_prod,
                                                     variable=self.variable_control_type_id_prod,
                                                     value="Manuel"
                                                     , bg=couleur_sous_fenetre, fg=couleur_police_champs, text="Manuel"
                                                     , selectcolor=couleur_inverse_tree, bd=bd_widget,
                                                     relief=relief_widget
                                                     # , command=lambda: self.select_mode_id_prod_manuel("a")
                                                     , activebackground="blue")
        self.radio_bout_type_id_manuel.grid(row=1, column=1, sticky=EW)
        self.radio_bout_type_id_manuel.invoke()
        self.radio_bout_type_id_auto = Radiobutton(self.labelf_type_id_prod,
                                                   variable=self.variable_control_type_id_prod,
                                                   value="Automatique"
                                                   , bg=couleur_sous_fenetre, fg=couleur_police_champs,
                                                   text="Automatique"
                                                   , selectcolor=couleur_inverse_tree,
                                                   # command=self.select_mode_id_prod_auto,
                                                   activebackground="blue", bd=bd_widget, relief=relief_widget)
        self.radio_bout_type_id_auto.grid(row=1, column=2)
        self.ctrl_r_b = 0
        self.var = StringVar(
            # value=select_defaut_colonne("prix_modifiable", "produit")
                             )
        self.radio_bout_pu_mod_non = Radiobutton(self.labelf_prix_modifiable, value="non", variable=self.var
                                                 , bg=couleur_sous_fenetre, fg=couleur_police_champs,
                                                 text="Non modifiable"
                                                 , selectcolor=couleur_inverse_tree,
                                                 # command=lambda: self.pu_modifiable_vente("non") ,
                                                 activebackground="blue", bd=bd_widget, relief=relief_widget)
        self.radio_bout_pu_mod_non.grid(row=1, column=1, sticky=EW)

        self.radio_bout_pu_mod_oui = Radiobutton(self.labelf_prix_modifiable, value="oui", variable=self.var
                                                 , bg=couleur_sous_fenetre, fg=couleur_police_champs, text="Modifiable"
                                                 , selectcolor=couleur_inverse_tree,
                                                 # command=lambda: self.pu_modifiable_vente("oui"),
                                                 activebackground="blue", bd=bd_widget, relief=relief_widget)
        self.radio_bout_pu_mod_oui.grid(row=1, column=2)

        self.lf_check_bout_champ_clean = LabelFrame(self.label_frame_param_prod, bg=couleur_sous_fenetre, bd=bd_widget,
                                                    relief=relief_widget,
                                                    text="Selectionner les champs qui ne seront pas supprimer")
        self.lf_check_bout_champ_clean.grid(row=2, column=1)
        self.var_check_bout = IntVar()
        self.check_b_champ_clean_nom = Checkbutton(self.lf_check_bout_champ_clean, text="Nom du produit",
                                                   bg=couleur_sous_fenetre,
                                                   # command=lambda: self.select_check_bout_supp(self.nom_produit_champs)
                                                   )
        self.check_b_champ_clean_nom.grid(row=1, column=1, sticky=W)

        self.check_b_champ_clean_categori = Checkbutton(self.lf_check_bout_champ_clean, text="Catégorie du produit",
                                                        bg=couleur_sous_fenetre,
                                                        # command=lambda: self.select_check_bout_supp(
                                                            # self.categorie_produit_champs)
                                                        )
        self.check_b_champ_clean_categori.grid(row=2, column=1, sticky=W)

        self.check_b_champ_clean_marque = Checkbutton(self.lf_check_bout_champ_clean, text="marque du produit",
                                                      bg=couleur_sous_fenetre,
                                                      # command=lambda: self.select_check_bout_supp(
                                                      #     self.marque_produit_champs)
                                                      )
        self.check_b_champ_clean_marque.grid(row=3, column=1, sticky=W)

        self.check_b_champ_clean_ca = Checkbutton(self.lf_check_bout_champ_clean, text="Cout d'achat du produit",
                                                  bg=couleur_sous_fenetre,
                                                  # command=lambda: self.select_check_bout_supp(
                                                  #     self.cout_achat_produit_champs)
                                                  )
        self.check_b_champ_clean_ca.grid(row=4, column=1, sticky=W)

        self.check_b_champ_clean_pv = Checkbutton(self.lf_check_bout_champ_clean, text="Prix de vente du produit",
                                                  bg=couleur_sous_fenetre,
                                                  # command=lambda: self.select_check_bout_supp(
                                                  #     self.prix_vente_produit_champs)
                                                  )
        self.check_b_champ_clean_pv.grid(row=5, column=1, sticky=W)

        self.check_b_champ_clean_qte = Checkbutton(self.lf_check_bout_champ_clean, text="Quantité du produit",
                                                   bg=couleur_sous_fenetre,
                                                   # command=lambda: self.select_check_bout_supp(
                                                   #     self.quantite_debut_stock_produit_champs)
                                                   )
        self.check_b_champ_clean_qte.grid(row=6, column=1, sticky=W)

        self.check_b_champ_clean_nf = Checkbutton(self.lf_check_bout_champ_clean, text="Nom du fournisseur",
                                                  bg=couleur_sous_fenetre,
                                                  # command=lambda: self.select_check_bout_supp(
                                                  #     self.nom_founisseur_produit_champs)
                                                  )
        self.check_b_champ_clean_nf.grid(row=7, column=1, sticky=W)

        self.check_b_champ_clean_ray = Checkbutton(self.lf_check_bout_champ_clean, text="Rayon",
                                                   bg=couleur_sous_fenetre,
                                                   # command=lambda: self.select_check_bout_supp(
                                                   #     self.rayon_produit_champs)
                                                   )
        self.check_b_champ_clean_ray.grid(row=8, column=1, sticky=W)

        self.check_b_champ_clean_gram = Checkbutton(self.lf_check_bout_champ_clean, text="Grammage",
                                                    bg=couleur_sous_fenetre,
                                                    # command=lambda: self.select_check_bout_supp(
                                                    #     self.grammage_produit_champs)
                                                    )
        self.check_b_champ_clean_gram.grid(row=9, column=1, sticky=W)

        self.check_b_champ_clean_ungram = Checkbutton(self.lf_check_bout_champ_clean, text="Unité du grammage",
                                                      bg=couleur_sous_fenetre,
                                                      # command=lambda: self.select_check_bout_supp(
                                                      #     self.unite_grammage_produit_champs)
                                                      )
        self.check_b_champ_clean_ungram.grid(row=10, column=1, sticky=W)

        self.check_b_champ_clean_seuicmd = Checkbutton(self.lf_check_bout_champ_clean, text="Seuil des commandes",
                                                       bg=couleur_sous_fenetre,
                                                       # command=lambda: self.select_check_bout_supp(
                                                       #     self.seuil_commande_produit_champs)
                                                       )
        self.check_b_champ_clean_seuicmd.grid(row=11, column=1, sticky=W)

        self.check_b_champ_clean_periodcmd = Checkbutton(self.lf_check_bout_champ_clean, text="Periode des commandes",
                                                         bg=couleur_sous_fenetre,
                                                         # command=lambda: self.select_check_bout_supp(
                                                         #     self.periode_commande_produit_champs)
                                                         )
        self.check_b_champ_clean_periodcmd.grid(row=12, column=1, sticky=W)
        # self.pu_mod_oui_non = select_defaut_colonne("prix_modifiable", "produit")
        #
        # self.select_default_pu_modifiable()

        # if self.pu_mod_oui_non == "oui":
        #     print("c'est oui debut")
        #     self.radio_bout_pu_mod_oui.select()
        #     self.radio_bout_pu_mod_oui.invoke()
        #     print("c'est oui fin")
        # else:
        #     self.radio_bout_pu_mod_non.invoke()
        #     self.radio_bout_pu_mod_non.select()

        self.label_frame_param_prod.bind("<B1-Motion>", self.deplace_pup_param_stock)
        self.label_frame_param_prod.bind("<Double-ButtonRelease-1>", self.param_prod_quit)

    def param_prod_open(self):
        """Ouvrir la page de parametrage des produits lors de l'ajout"""
        self.label_frame_param_prod.place(x=400, y=50)

    def param_prod_quit(self, event):
        """Ouvrir la page de description des produits lors de l'ajout"""
        self.label_frame_param_prod.place_forget()

    def affiche_bout_ok_seuil_cmd(self):
        """Afficher le bouton ok et annuler pour la validation/annulation du seuil de la quantite seuil d'alerte de passation des commandes par
        defaut """
        self.bouton_defaut_seuil_cmd.grid(row=2, column=1, sticky=EW)
        self.bouton_defaut_seuil_cmd_annul.grid(row=2, column=2, sticky=EW)

    # def save_seuil_cmd(self):
    #     """Valider la quantite seuil d'alerte de passation des commandes par defaut"""
    #     seuil_cmd_defaut_obt = self.spinbox_defaut_seuil_cmd.get()
    #     if not seuil_cmd_defaut_obt:
    #         return
    #     ma_base_donnee = connexion_bd_mysql()
    #     connexion_seuil_defaut = ma_base_donnee.cursor()
    #     connexion_seuil_defaut.execute("ALTER TABLE `bd_gestion_del_blanco`.`produit` CHANGE COLUMN `seuil_commande` "
    #                                    f"`seuil_commande` INT NULL DEFAULT '{seuil_cmd_defaut_obt}' ;")
    #     ma_base_donnee.commit()
    #     ma_base_donnee.close()
    #     self.valeur_defaut_seuil_a_mod.set(self.spinbox_defaut_seuil_cmd.get())
    #     self.bouton_defaut_seuil_cmd.grid_forget()
    #     self.bouton_defaut_seuil_cmd_annul.grid_forget()
    #     self.spinbox_defaut_seuil_cmd.delete(0, END)
    #     self.spinbox_defaut_seuil_cmd.insert(0, select_defaut_colonne("seuil_commande", "produit"))

    def annul_mod_seuil_cmd(self):
        """Annuler l'operation du changement de la valeur par defaut des seuils de passation des commandes"""
        self.spinbox_defaut_seuil_cmd.delete(0, END)
        self.spinbox_defaut_seuil_cmd.insert(0, self.valeur_defaut_seuil_a_mod.get())
        self.bouton_defaut_seuil_cmd.grid_forget()
        self.bouton_defaut_seuil_cmd_annul.grid_forget()

    def affiche_bout_ok_duree_cmd(self):
        """Afficher le bouton ok pour la validation du seuil de la quantite seuil d'alerte de passation des commandes par
        defaut """
        self.bouton_defaut_periode_cmd.grid(row=2, column=1, sticky=EW)
        self.bouton_defaut_periode_cmd_annul.grid(row=2, column=2, sticky=EW)

    # def save_duree_limit_cmd(self):
    #     """Valider la periode d'alerte de passation des commandes par defaut"""
    #     duree_cmd_defaut_obt = self.spinbox_defaut_periode_cmd.get()
    #     if not duree_cmd_defaut_obt:
    #         return
    #     ma_base_donnee = connexion_bd_mysql()
    #     connexion_seuil_defaut = ma_base_donnee.cursor()
    #     connexion_seuil_defaut.execute(
    #         "ALTER TABLE `bd_gestion_del_blanco`.`produit` CHANGE COLUMN `duree_limite_commande` "
    #         f"`duree_limite_commande` INT NULL DEFAULT '{duree_cmd_defaut_obt}' ;")
    #     ma_base_donnee.commit()
    #     ma_base_donnee.close()
    #     messagebox.showinfo(nom_ets, "Parametre enregistré avec succès")
    #     self.valeur_defaut_periode_a_mod.set(self.spinbox_defaut_periode_cmd.get())
    #     self.bouton_defaut_periode_cmd.grid_forget()
    #     self.bouton_defaut_periode_cmd_annul.grid_forget()
    #     self.spinbox_defaut_periode_cmd.delete(0, END)
    #     self.spinbox_defaut_periode_cmd.insert(0, select_defaut_colonne("duree_limite_commande", "produit"))

    def annul_mod_duree_cmd(self):
        """Annuler l'operation du changement de la valeur par defaut des seuil de passation des commandes"""
        self.spinbox_defaut_periode_cmd.delete(0, END)
        self.spinbox_defaut_periode_cmd.insert(0, self.valeur_defaut_periode_a_mod.get())
        self.bouton_defaut_periode_cmd.grid_forget()
        self.bouton_defaut_periode_cmd_annul.grid_forget()

    # def select_mode_id_prod_auto(self):
    #     """Configurer le mode d'identification des produits à automatique"""
    #     self.id_produit_champs.grid_forget()
    #     self.id_produit.grid_forget()
    #     ma_base_donnee = connexion_bd_mysql()
    #     connexion_mode_id = ma_base_donnee.cursor()
    #     connexion_mode_id.execute(
    #         f"UPDATE `bd_gestion_del_blanco`.`parametre` SET `courant` = 'oui' WHERE (`nom_parametre` = 'id_auto_prod');")
    #     ma_base_donnee.commit()
    #     ma_base_donnee.close()
    #     messagebox.showinfo(nom_ets, "Mode IDENTIFICATION AUTOMATIQUE des produits activé avec succès")

    # def select_mode_id_prod_manuel(self, control):
    #     """Configurer le mode d'identification des produits à manuel"""
    #     self.id_produit.grid(row=1, column=1, sticky=EW, columnspan=1)
    #     self.id_produit_champs.grid(row=1, column=2, sticky=EW, columnspan=1)
    #     ma_base_donnee = connexion_bd_mysql()
    #     connexion_mode_id = ma_base_donnee.cursor()
    #     connexion_mode_id.execute(
    #         f"UPDATE `bd_gestion_del_blanco`.`parametre` SET `courant` = 'non' WHERE (`nom_parametre` = 'id_auto_prod');")
    #     ma_base_donnee.commit()
    #     ma_base_donnee.close()

    # def pu_modifiable_vente(self, new_value):
    #     """Est-ce que le prix de ce produit sera modifiable lors des ventes parametre par defaut"""
    #     # if self.ctrl_r_b == 0:
    #     #     self.ctrl_r_b += 1
    #     #     self.var.set(new_value)
    #     #     self.select_default_pu_modifiable()
    #     #     return
    #
    #     if self.produit_table_service.alter_table_to_change_default_value(new_value):
    #         self.produit_table_service.conffirmer()
    #     self.var.set(new_value)
    #     self.select_default_pu_modifiable()
    #
    # # def pu_non_modifiable_vente(self):
    # #     if self.ctrl_r_b % 2 == 0:
    # #         return
    # #     """Est-ce que le prix de ce produit sera modifiable lors des ventes parametre par defaut"""
    # #     ma_base_donnee = connexion_bd_mysql()
    # #     connexion__defaut_colonne = ma_base_donnee.cursor()
    # #     connexion__defaut_colonne.execute(f"ALTER TABLE `bd_gestion_del_blanco`.`produit` CHANGE COLUMN "
    # #                                       f"`prix_modifiable` `prix_modifiable` VARCHAR(4) NULL DEFAULT 'non' ;")
    # #     ma_base_donnee.commit()
    # #     ma_base_donnee.close()
    # #     self.select_default_pu_modifiable()
    #
    # def select_check_bout_supp(self, champs):
    #     """Utilisateur a selectionne ou deselectionne le bouton en question"""
    #     if champs in self.liste_champs_add_prod_stock_a_supp:
    #         self.liste_champs_add_prod_stock_a_supp.remove(champs)
    #     else:
    #         self.liste_champs_add_prod_stock_a_supp.append(champs)

    def deplace_pup_param_stock(self, event):
        self.label_frame_param_prod.place_configure(x=self.master.winfo_pointerx() - 30,
                                                    y=self.master.winfo_pointery() - 50)
