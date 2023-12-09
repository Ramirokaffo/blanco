from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter import *

from datetime import date

from STATIC.ConstantFile import *
from UI.Product.AddProductForm import AddProductForm


class PageAjoutProduit(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.add_product_page = Frame(self.master)
        self.add_product_page.pack(expand=YES)
        # self.master.add(self.add_product_page, text="Ajouter produit", sticky=NSEW)

        # self.super_master = super_master
        # self.gestion_touch_return = gestion_touch_return



        # self.affiche_img = ImageTk.PhotoImage(self.image, master=self.master)
        # self.label_img_produit = Label(self.labelf_image_prouit, width=300, height=200, image=self.affiche_img,
        #                                bg=couleur_sous_fenetre,
        #                                anchor="w", bd=bd_widget, relief=relief_widget)
        # self.label_img_produit.image = self.affiche_img
        # self.label_img_produit.grid(sticky=W)
        # self.frame_icone_action_img = Frame(self.labelf_image_prouit, bg=couleur_sous_fenetre)
        # self.frame_icone_action_img.grid(sticky=W)
        # self.img_dossier = redimension_icone(image_dossier, 35, 20)
        # self.bouton_img_produit = Button(self.frame_icone_action_img, text="Associer une image", font="arial",
        #                                  bd=bd_widget,
        #                                  relief=relief_widget,
        #                                  command=lambda: self.photo_produit(0), image=self.img_dossier,
        #                                  bg=couleur_bouton, fg=couleur_police)
        # self.bouton_img_produit.grid(row=1, column=1, sticky=EW)
        # self.img_suppr_pic = redimension_icone(image_suppression_noir_croix, 35, 20)
        # self.bouton_img_suppr = Button(self.frame_icone_action_img, text="Supprimer une image", font="arial",
        #                                bd=bd_widget,
        #                                relief=relief_widget,
        #                                command=self.suppr_image_produit,
        #                                # command=suppr_image_produit,
        #                                image=self.img_suppr_pic,
        #                                bg=couleur_bouton, fg=couleur_police)
        # self.bouton_img_suppr.grid(row=1, column=2, sticky=EW)

        self.paned_fen_gestion_produit = PanedWindow(self.add_product_page, bg=couleur_frame, orient=HORIZONTAL,
                                                     sashwidth=2)
        self.paned_fen_gestion_produit.pack(expand=YES, fill=BOTH)

        self.label_frame_caract_prod = LabelFrame(self.paned_fen_gestion_produit, text="Caractéristiques du produit",
                                                  labelanchor=N,
                                                  bg=couleur_sous_fenetre, fg=couleur_police, bd=bd_widget,
                                                  relief=relief_widget)

        # self.label_frame_liste_prod = LabelFrame(self.paned_fen_gestion_produit, text="Liste des produits",
        #                                          labelanchor=N,
        #                                          bg=couleur_sous_fenetre, fg=couleur_police, bd=bd_widget,
        #                                          relief=relief_widget)

        self.paned_fen_gestion_produit.add(self.label_frame_caract_prod)

        # self.paned_fen_gestion_produit.add(self.label_frame_liste_prod)
        #
        # self.frame_tableau_produit = Frame(self.label_frame_liste_prod, bg=couleur_sous_fenetre, )
        # self.frame_tableau_produit.pack(expand=YES)

        # self.tableau_produit = TableauListeProduit(master=self.frame_tableau_produit,
        #                                            pupop=self.popup_action_prod_magazin, height=27)
        self.formulaire_ajout_prod = AddProductForm(master=self.label_frame_caract_prod,
                                                    # super_master=self.super_master,
                                                    # tableau_produit=self.tableau_produit
                                                    )
        # self.tableau_produit.affiche_produit_magazin()
        # self.gestion_touch_return(fenetre_to_bind=self.master,
        #                           function_to_bind=self.formulaire_ajout_prod.enregistrer_produit_stck)

    # def construire(self):
    #     # self.produit_table_service = ProduitTableService()
    #

    def popup_action_prod_magazin(self, event):
        """Menu popup de la fenetre de gestion des produits"""
        approv_selectionne = self.tableau_produit.tableau_produit.selection()
        if approv_selectionne:
            menu_popup_action_prod_magazin = Menu(self.tableau_produit.tableau_produit, tearoff=0, title="Action sur les produits",
                                                  relief=FLAT)
            menu_popup_action_prod_magazin.add_command(label="Editer", command=self.formulaire_ajout_prod.modifier_produit_info)
            menu_popup_action_prod_magazin.add_command(label=f"Spprimer "
                                                             f"{'ce produit' if len(approv_selectionne) == 1 else 'ces produits'}"
                                                       , command=self.suppr_select_prod_bd)
            x, y = self.master.winfo_pointerxy()
            menu_popup_action_prod_magazin.tk_popup(x, y)

    # def affiche_image_gestion_produit(self, event):
    #     if self.image_produit.get():
    #         afficher_image_plein_ecran(self.master, self.image_produit.get())
    #     else:
    #         afficher_image_plein_ecran(self.master, image_defaut_produit)

    # def photo_produit(self, event):
    #     global image_defaut_produit
    #     photo_lien = filedialog.askopenfilenames(title="Selectionner l'image", initialdir="/",
    #                                              filetypes=(("jpeg filles", "*.jpg"), ("png files", "*.png")
    #                                                         , ("all files", "*.*")))
    #     if photo_lien:
    #         if photo_lien[0].endswith(".jpg") or photo_lien[0].endswith(".png") or photo_lien[0].endswith(".jpeg"):
    #             image = PIL.Image.open(photo_lien[0])
    #             image.thumbnail((200, 200))
    #             affiche_img = ImageTk.PhotoImage(image)
    #             # self.label_img_produit.config(image=affiche_img)
    #             # self.label_img_produit.image = affiche_img
    #             self.image_produit.set("??".join(list(photo_lien)))
    #         else:
    #             question = messagebox.askretrycancel("Erreur", "Vous avez choisi un format de fichier incorrect")
    #             if question == True:
    #                 self.photo_produit(0)
    #     else:
    #         self.image_produit.set(image_defaut_produit)

    def suppr_select_prod_bd(self):
        """Supprimer le dernier produit enregistre dans la bd"""
        prod_selectionne = self.tableau_produit.tableau_produit.selection()
        qest = messagebox.askyesno("Attention",
                                   "Vous etes sur le point de supprimer les produits de la base de donnée\n"
                                   "Cette action est irreversible\n"
                                   "\n"
                                   "Continuer?")
        if not qest:
            return
        for ligne in prod_selectionne:
            ligne_select_magazin = self.tableau_produit.tableau_produit.item(ligne)
            valeur_ligne_select_magazin = ligne_select_magazin["values"]
            rapport = self.produit_table_service.update_to_change_column_data(column_name="etat", new_colummn_value="0",
                                                                              where_column="id_produit", where_value=valeur_ligne_select_magazin[0])
            if not rapport:
                messagebox.showerror("Erreur", f"Le produit {valeur_ligne_select_magazin[1]} n'a pas pu etre supprimé")
                break
        self.produit_table_service.conffirmer()
        # messagebox.showinfo(nom_ets, "Suppression effectuée avec succès")
        self.tableau_produit.affiche_produit_magazin()
        # self.affiche_liste_approv()
        # self.stock_critic_table.remplir_treeviiew_stock_critic()

    # def suppr_image_produit(self):
    #     """Supprimer l'image du produit"""
    #     global image_defaut_produit
    #     # self.label_img_produit.config(image=self.affiche_img)
    #     # self.label_img_produit.image = self.affiche_img
    #     self.image_produit.set(image_defaut_produit)

