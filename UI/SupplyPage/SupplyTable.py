from tkinter import *
from tkinter import ttk

from STATIC.ConstantFile import *


class SupplyTable(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label_frame_liste_approv = LabelFrame(self.master,
                                                   text="Historique des approvisionnemnts",
                                                   labelanchor=N,
                                                   bg=couleur_sous_fenetre, fg=couleur_police, width=250,
                                                   bd=bd_widget,
                                                   relief=relief_widget)
        self.label_frame_liste_approv.pack(expand=YES)
        self.barre_defilement_prod = Scrollbar(self.label_frame_liste_approv, troughcolor="blue", bg="yellow",
                                               orient=VERTICAL)
        self.barre_defilement_prod.pack(fill=Y, side=RIGHT)
        self.barre_defilement_prod_horiz = Scrollbar(self.label_frame_liste_approv, troughcolor="blue", bg="yellow",
                                                     orient=HORIZONTAL)
        self.barre_defilement_prod_horiz.pack(fill=X, side=BOTTOM)

        self.tableau_approv = ttk.Treeview(self.label_frame_liste_approv, selectmode=EXTENDED, height=27,
                                           style="mystyle.Treeview", yscrollcommand=self.barre_defilement_prod.set,
                                           columns=("1", "2", "3", "4", "5", "7", "8", "9"), show="headings",
                                           padding=[20, 8, 90, 20], xscrollcommand=self.barre_defilement_prod_horiz.set)
        self.tableau_approv.pack(expand=YES)
        """Entete de la table"""
        self.tableau_approv.heading("1", text="N°", anchor="w")
        self.tableau_approv.heading("2", text="Produit", anchor="w")
        self.tableau_approv.heading("3", text="Quantité en stock", anchor="w")
        self.tableau_approv.heading("4", text="Quantité achetée", anchor="e")
        self.tableau_approv.heading("5", text="PU", anchor="w")
        self.tableau_approv.heading("7", text="Fournisseur", anchor="w")
        self.tableau_approv.heading("8", text="Date d'approvisionnemnt", anchor="c")
        self.tableau_approv.heading("9", text="Date de peremption", anchor="e")

        """Dimensions de la table"""
        self.tableau_approv.column("1", width=30, minwidth=50, anchor="w")
        self.tableau_approv.column("2", width=230, minwidth=75, anchor="w")
        self.tableau_approv.column("3", width=100, minwidth=50, anchor="w")
        self.tableau_approv.column("4", width=100, minwidth=50, anchor="w")
        self.tableau_approv.column("5", width=100, minwidth=50, anchor="w")
        self.tableau_approv.column("7", width=130, minwidth=75, anchor="w")
        self.tableau_approv.column("8", width=170, minwidth=50, anchor="c")
        self.tableau_approv.column("9", width=150, minwidth=50, anchor="e")
        self.barre_defilement_prod.config(command=self.tableau_approv.yview)
        self.barre_defilement_prod_horiz.config(command=self.tableau_approv.xview)

    def popup_action_approv(self, event):
        approv_selectionne = self.tableau_approv.selection()
        if approv_selectionne:
            menu_popup_action_approv = Menu(self.tableau_approv, tearoff=0, title="Action sur les approvisionnements",
                                            relief=FLAT)
            menu_popup_action_approv.add_command(label=f"Supprimer "
                                                       f"{'cet approvisionnement' if len(approv_selectionne) == 1 else 'ces approvisionnements'} "
                                                 # , command=self.supprimer_approv,
                                                 )
            x, y = self.master.winfo_pointerxy()
            menu_popup_action_approv.tk_popup(x, y)
