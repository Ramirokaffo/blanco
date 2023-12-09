from tkinter import *
from tkinter import ttk


class MiniTableCredit(Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.control_order = 0
        # self.ma_base_donnee = connexion_bd_mysql()
        # self.me_connect = self.ma_base_donnee.cursor()
        # self.service_table_vente = VenteTableService()
        self.bare_defil_mini_tcredit = Scrollbar(self.master, orient=VERTICAL)
        self.bare_defil_mini_tcredit.pack(side=RIGHT, fill=Y)
        self.bare_defil_mini_tcredit_hori = Scrollbar(self.master, orient=HORIZONTAL)
        self.bare_defil_mini_tcredit_hori.pack(side=BOTTOM, fill=X)
        self.mini_treeview_credit = ttk.Treeview(self.master, selectmode=EXTENDED, height=12,
                                                 yscrollcommand=self.bare_defil_mini_tcredit.set,
                                                 columns=("1", "2", "3", "4"), show="headings",
                                                 style="mystyle.Treeview",
                                                 xscrollcommand=self.bare_defil_mini_tcredit_hori.set)

        self.mini_treeview_credit.heading("1", text="Client", anchor="w",
                                          # command=lambda: self.remplir_treeview_credit_mini_order("nom_client")
                                          )
        self.mini_treeview_credit.heading("2", text="Echéance ", anchor="c",
                                          # command=lambda: self.remplir_treeview_credit_mini_order("echeance")
                                          )
        self.mini_treeview_credit.heading("3", text="Avance ", anchor="w",
                                          # command=lambda: self.remplir_treeview_credit_mini_order("avance")
                                          )
        self.mini_treeview_credit.heading("4", text="Total ", anchor="e",
                                          # command=lambda: self.remplir_treeview_credit_mini_order("somme_totale_payee")
                                          )

        self.mini_treeview_credit.column("1", width=130, minwidth=50, anchor="w")
        self.mini_treeview_credit.column("2", width=120, minwidth=50, anchor="c")
        self.mini_treeview_credit.column("3", width=120, minwidth=50, anchor="w")
        self.mini_treeview_credit.column("4", width=120, minwidth=50, anchor="e")
        self.mini_treeview_credit.pack(expand=YES)
        self.bare_defil_mini_tcredit.configure(command=self.mini_treeview_credit.yview)
        self.bare_defil_mini_tcredit_hori.configure(command=self.mini_treeview_credit.xview)

    #     self.mini_treeview_credit.bind("<ButtonRelease-3>", self.popup_action_treeview_credit_mini)
    #     self.mini_treeview_credit.bind("<Expose>", self.remplir_on_expose)
    #
    # def remplir_on_expose(self, event):
    #     self.remplir_treeview_credit_mini_order("id_vente")
    #
    # def remplir_treeview_credit_mini_order(self, colon="id_vente"):
    #     """Remplir le tableau des ventes effectuee a credit selon un certain ordre"""
    #     if self.control_order % 2 == 0:
    #         order = "ASC"
    #     else:
    #         order = "DESC"
    #
    #     self.me_connect.execute(
    #         f"select nom_client, echeance, avance, somme_totale_payee, id_relatif from vente WHERE type_vente = "
    #         f"'credit' AND somme_totale_payee != '0.0' and etat <> '0' AND YEAR(date_heure_vente) = "
    #         f"'{parser.parse(current_date.get()).year}' ORDER BY {colon} {order};")
    #     el = 0
    #     while True:
    #         try:
    #             self.mini_treeview_credit.delete(str(el))
    #         except:
    #             break
    #         el += 1
    #
    #     for it, row in enumerate(self.me_connect):
    #         rown = list(row)
    #         rown[-2] = int(rown[-2])
    #         rown[-3] = int(rown[-3])
    #         echeanc = rown[1]
    #         if type(echeanc) == type(date.today()) and echeanc <= date.today():
    #             self.mini_treeview_credit.insert("", index=0, id=f"{it}", values=rown, tags=("dif",))
    #         else:
    #             if echeanc is None or echeanc == "0000-00-00" or echeanc == ".":
    #                 rown[1] = "Aucune"
    #             if it % 2 == 0:
    #                 self.mini_treeview_credit.insert("", index=0, id=f"{it}", values=rown, tags=("even",))
    #             else:
    #                 self.mini_treeview_credit.insert("", index=0, id=f"{it}", values=rown, tags=("odd",))
    #     ma_base_donnee.close()
    #     self.mini_treeview_credit.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
    #     self.mini_treeview_credit.tag_configure("even", background=couleur_inverse_tree,
    #                                             foreground=couleur_police_champs)
    #     self.mini_treeview_credit.tag_configure("dif", background=couleur_inverse_tree, foreground="red")
    #     self.control_order += 1
    #
    # def popup_action_treeview_credit_mini(self, event):
    #     produ_selectionne = self.mini_treeview_credit.selection()
    #     if produ_selectionne:
    #         menu_popup_action_prod_magazin = Menu(self.mini_treeview_credit, tearoff=0,
    #                                               title="Action sur les ventes à crédit",
    #                                               relief=FLAT)
    #         menu_popup_action_prod_magazin.add_command(label=f"Valider la vente", command=self.valider_credit_vente)
    #         menu_popup_action_prod_magazin.add_command(label=f"Annuler la vente", command=self.annul_vente_credit)
    #         menu_popup_action_prod_magazin.add_separator()
    #         menu_popup_action_prod_magazin.add_command(label=f"Ajouter une tranche", command=self.ajouter_tranche)
    #         menu_popup_action_prod_magazin.add_command(label=f"Modifier l'échéance", command=self.modifier_echeance)
    #         menu_popup_action_prod_magazin.add_separator()
    #         menu_popup_action_prod_magazin.add_command(label=f"Détails", command=self.affiche_vente_credit)
    #         x, y = fenetre_principale.winfo_pointerxy()
    #         menu_popup_action_prod_magazin.tk_popup(x, y)
    #
    # def modifier_echeance(self):
    #     selection = self.mini_treeview_credit.selection()
    #     ligne_select = self.mini_treeview_credit.item(selection[0])
    #     valeur_ligne_select = ligne_select["values"]
    #     new_value = simpledialog.askstring(title=nom_ets, prompt="Nouvelle échéance(AAAA-MM-JJ):")
    #     if new_value:
    #         if self.service_table_vente.update_vente_change_column_data(column_name="echeance",
    #                                                                     new_value=new_value,
    #                                                                     where_column="id_relatif",
    #                                                                     where_value=valeur_ligne_select[-1]):
    #             self.service_table_vente.confirmer()
    #             self.remplir_treeview_credit_mini_order()
    #             messagebox.showinfo(nom_ets, "Mise à jour éffectuée avec succès !")
    #         else:
    #             messagebox.showinfo(nom_ets, "Une erreur s'est produite !")
    #
    # def ajouter_tranche(self):
    #     selection = self.mini_treeview_credit.selection()
    #     if selection[0]:
    #         ligne_select = self.mini_treeview_credit.item(selection[0])
    #         valeur_ligne_select = ligne_select["values"]
    #         new_value = simpledialog.askfloat(title=nom_ets, prompt="Montant de la tranche")
    #         if new_value:
    #             if vente_table_service.update_vente_to_add_tranche(new_value, valeur_ligne_select[-1]):
    #                 vente_table_service.confirmer()
    #                 self.remplir_treeview_credit_mini_order("id_vente")
    #             else:
    #                 messagebox.showerror("Erreur", "Une erreur s'est produite !")
    #
    # def affiche_vente_credit(self):
    #     instancier_historique_vente(note_book_sud_vente, periode="YEAR", valeur=date.today().year, type_vente="credit", title="Ventes à crédit")
    #
    # def annul_vente_credit(self):
    #     selection = self.mini_treeview_credit.selection()
    #     ligne_select = self.mini_treeview_credit.item(selection[0])
    #     valeur_ligne_select = ligne_select["values"]
    #     if annul_vente_wid(valeur_ligne_select[-1], current_date.get(), "credit"):
    #         self.remplir_treeview_credit_mini_order("nom_client")
    #         messagebox.showinfo(nom_ets, "Vente à crédit annulée avec succès !")
    #
    # def valider_credit_vente(self):
    #     """Valider la vente a credit"""
    #     selection = self.mini_treeview_credit.selection()
    #     ligne_select = self.mini_treeview_credit.item(selection[0])
    #     valeur_ligne_select = ligne_select["values"]
    #     if (vente_table_service.update_vente_change_column_data(column_name="type_vente", new_value="normal",
    #     where_column="id_relatif", where_value=valeur_ligne_select[-1]) and
    #             vente_table_service.update_vente_change_column_data(column_name="date_remboursement", new_value=str(datetime.now()),
    #     where_column="id_relatif", where_value=valeur_ligne_select[-1])):
    #         vente_table_service.confirmer()
    #         self.remplir_treeview_credit_mini_order("nom_client")
    #         info_bas_vente(texte="Vente à crédit validée avec succès !!", indication="validation", mode="admin")
    #     else:
    #         messagebox.showerror("Erreur", "Une erreur est survenue lors de la validation de la vente !")
