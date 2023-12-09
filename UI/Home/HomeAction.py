from tkinter import *
from tkinter import ttk


class HomeActions(Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.current_instance = 0
        self.ctrl_lis_prod = 0
        self.control_list_vente = 0
        self.barre_defilement_accueil = Scrollbar(self.master, orient=VERTICAL)
        self.barre_defilement_accueil.pack(fill=Y, side=RIGHT)

        self.list_var_accueil = StringVar()
        # self.list_box_accueil = Listbox(frame_vente_info_accueil, activestyle="underline", takefocus=False,
        #                                 listvariable=self.list_var_accueil, height=10, setgrid=True,
        #                                 font=(police, 12),
        #                                 # relief=RAISED,
        #                                 selectborderwidth=0,
        #                                 yscrollcommand=self.barre_defilement_accueil.set, bg="floralwhite")
        # self.list_box_accueil.pack(expand=YES, fill=BOTH, pady=2, padx=2)
        # self.barre_defilement_accueil.configure(command=self.list_box_accueil.yview)
        # # self.barre_defilement_accueil.configure(command=self.list_box_accueil.yview_scroll)
        #
        # self.list_box_accueil.insert(0, "  Vente des produits")
        # # self.list_box_accueil.itemconfig(0, background=couleur_inverse_tree, foreground=couleur_police_champs)
        # self.list_box_accueil.insert(1, "  Liste des ventes")
        # # self.list_box_accueil.itemconfig(1, background=couleur_label, foreground=couleur_police_champs)
        # self.list_box_accueil.insert(2, "  Liste des produits")
        # # self.list_box_accueil.itemconfig(2, background=couleur_inverse_tree, foreground=couleur_police_champs)
        # self.list_box_accueil.insert(3, "  Dépenses quotidiennes")
        # # self.list_box_accueil.itemconfig(3, background=couleur_label, foreground=couleur_police_champs)
        # self.list_box_accueil.insert(4, "  Comptes de fin de journée")
        # # self.list_box_accueil.itemconfig(4, background=couleur_inverse_tree, foreground=couleur_police_champs)

        self.treeview_accueil = ttk.Treeview(self.master, yscrollcommand=self.barre_defilement_accueil.set,
                                             show="tree headings")
        self.treeview_accueil.pack(side=TOP, fill=BOTH)

        self.treeview_accueil.insert("", END, "1", text="Vente des produits")
        self.treeview_accueil.insert("", END, "2", text="Liste des ventes")
        self.treeview_accueil.insert("", END, "3", text="Liste des produits")
        self.treeview_accueil.insert("", END, "4", text="Dépenses quotidiennes")
        self.treeview_accueil.insert("", END, "5", text="Recettes quotidiennes")
        self.treeview_accueil.insert("", END, "6", text="Comptes de fin de journée")
        self.treeview_accueil.insert("", END, "7", text="Gerer le serveur")
        #
        # self.frame_liste_vente = Frame(note_book_sud_vente, bg=couleur_sous_fenetre)
        # self.frame_liste_produit = Frame(note_book_sud_vente, bg=couleur_sous_fenetre)
        #
        self.barre_defilement_accueil.config(command=self.treeview_accueil.yview)
        # self.treeview_accueil.bind("<<TreeviewSelect>>", self.on_treeviews_select)
        # self.list_box_accueil.bind("<<ListboxSelect>>", self.on_treeviews_select)
        # affiche_grille_vente()
        # self.historique = HistoriqueVente(self.frame_liste_vente, valeur=date.today().day, periode="DAY",
        #                              jour=date.today().day, height=24)
        # self.list_box_accueil.selection_anchor(0)
        # self.list_box_accueil.selection_anchor(0)
        # self.list_box_accueil.selection_set(ANCHOR, 2)
        # self.treeview_accueil.selection_set("1")
        # self.affiche_grille_vente()

    # def on_treeviews_select(self, event):
    #     if self.ctrl_lis_prod == 0:
    #         self.ctrl_lis_prod += 1
    #         return
    #     # try:
    #     indx_ligne_select = self.treeview_accueil.selection()
    #     valeur_ligne_select_opera = self.treeview_accueil.item(indx_ligne_select[0])["text"]
    #     if valeur_ligne_select_opera == "Vente des produits":
    #         affiche_grille_vente()
    #     elif valeur_ligne_select_opera == "Liste des ventes":
    #         self.display_liste_vente()
    #     elif valeur_ligne_select_opera == "Liste des produits":
    #         self.display_liste_produit()
    #     elif valeur_ligne_select_opera == "Dépenses quotidiennes":
    #         DepenseQuotidienPageInstance.displays_or_remove()
    #     # except:
    #     #     pass

    # def display_liste_vente(self):
    #     if not self.frame_liste_vente.winfo_exists():
    #         self.frame_liste_vente = Frame(note_book_sud_vente, bg=couleur_sous_fenetre)
    #         self.historique = HistoriqueVente(self.frame_liste_vente, valeur=date.today().day, periode="DAY",
    #                                           jour=date.today().day, height=24)
    #         note_book_sud_vente.add(self.frame_liste_vente, text="Liste des ventes")
    #         note_book_sud_vente.select(self.frame_liste_vente)
    #         self.historique.displays()
    #     self.current_instance += 1
    #     if self.current_instance == 1:
    #         note_book_sud_vente.add(self.frame_liste_vente, text="Liste des ventes")
    #         note_book_sud_vente.select(self.frame_liste_vente)
    #         self.historique.displays()
    #         self.historique.affiche_treeview(0)
    #     elif self.current_instance % 2 == 0:
    #         note_book_sud_vente.forget(self.frame_liste_vente)
    #     else:
    #         note_book_sud_vente.add(self.frame_liste_vente, text="Liste des ventes")
    #         note_book_sud_vente.select(self.frame_liste_vente)
    #         self.historique.displays()
    #         self.historique.affiche_treeview(0)

    # def display_liste_produit(self):
    #     if self.control_list_vente % 2 == 0:
    #         if not self.frame_liste_produit.winfo_exists():
    #             self.frame_liste_produit = Frame(note_book_sud_vente, bg=couleur_sous_fenetre)
    #         note_book_sud_vente.add(self.frame_liste_produit, text="Liste des produits")
    #         note_book_sud_vente.select(self.frame_liste_produit)
    #         tableau_produit = TableauListeProduit(self.frame_liste_produit, pupop=None, height=25)
    #         tableau_produit.affiche_produit_magazin()
    #     else:
    #         note_book_sud_vente.forget(self.frame_liste_produit)
    #         self.frame_liste_produit.destroy()
    #     self.control_list_vente += 1
