from tkinter import *
from tkinter import ttk


class MiniTreeviewCmd(Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.control_id = 0
        self.barre_defilement_mini_treeview_cmd = Scrollbar(self.master, orient=VERTICAL)
        self.barre_defilement_mini_treeview_cmd.pack(fill=Y, side=RIGHT)
        self.barre_defilement_mini_treeview_cmd_hori = Scrollbar(self.master, orient=HORIZONTAL)
        self.barre_defilement_mini_treeview_cmd_hori.pack(fill=X, side=BOTTOM)

        self.mini_treeview_cmd = ttk.Treeview(self.master, selectmode=EXTENDED, height=11,
                                              style="mystyle.Treeview",
                                              yscrollcommand=self.barre_defilement_mini_treeview_cmd.set,
                                              columns=("1", "2", "3", "4", "5"), show="tree headings",
                                              xscrollcommand=self.barre_defilement_mini_treeview_cmd_hori.set)

        self.mini_treeview_cmd.heading("1", text="N°", anchor="w",
                                       # command=lambda: self.remplir_treeview_cmd_save_mini_order("id_commande")
                                       )
        self.mini_treeview_cmd.heading("2", text="Panier", anchor="w",
                                       # command=lambda: self.remplir_treeview_cmd_save_mini_order("produit_commande")
                                       )
        self.mini_treeview_cmd.heading("3", text="Par", anchor="w",
                                       # command=lambda: self.remplir_treeview_cmd_save_mini_order("vendeur")
                                       )
        self.mini_treeview_cmd.heading("4", text="Date", anchor="w",
                                       # command=lambda: self.remplir_treeview_cmd_save_mini_order("date_save_commande")
                                       )
        self.mini_treeview_cmd.heading("5", text="Client", anchor="e",
                                       # command=lambda: self.remplir_treeview_cmd_save_mini_order("client")
                                       )

        self.mini_treeview_cmd.column("1", width=25, minwidth=25, anchor="w")
        self.mini_treeview_cmd.column("2", width=75, minwidth=300, anchor="w")
        self.mini_treeview_cmd.column("3", width=75, minwidth=75, anchor="w")
        self.mini_treeview_cmd.column("4", width=75, minwidth=100, anchor="w")
        self.mini_treeview_cmd.column("5", width=75, minwidth=75, anchor="e")
        self.mini_treeview_cmd.pack(expand=YES)
        self.barre_defilement_mini_treeview_cmd.config(command=self.mini_treeview_cmd.yview)
        self.barre_defilement_mini_treeview_cmd_hori.config(command=self.mini_treeview_cmd.xview)

        # self.mini_treeview_cmd.bind("<ButtonRelease-3>", self.popup_action_tree_cmd_mini)
        # self.mini_treeview_cmd.bind("<Double-ButtonRelease-1>", self.commande_save_use_mini)
        # self.mini_treeview_cmd.bind("<Double-ButtonRelease-1>", self.commande_save_use_mini)
        # self.mini_treeview_cmd.bind("<Expose>", self.remplir_on_expose)
        # self.mini_treeview_cmd.bind("<<TreeviewSelect>>", self.commande_save_use_mini)

    # def remplir_treeview_cmd_save_mini(self):
    #     """Remplir le tableau des commandes enregistrees"""
    #     ma_base_donnee = connexion_bd_mysql()
    #     me_connect = ma_base_donnee.cursor()
    #     me_connect.execute("SELECT * FROM commande ORDER BY id_commande ASC;")
    #     liste_cmd = me_connect.fetchall()
    #     el = 0
    #     while self.mini_treeview_cmd:
    #         try:
    #             self.mini_treeview_cmd.delete(str(el))
    #         except:
    #             break
    #         el += 1
    #     h = 880000000
    #     for it, cmd in enumerate(liste_cmd):
    #         h -= 1
    #         liste_prod_cmd = cmd[1].split(",")
    #         liste_qte_cmd = cmd[2].split(",")
    #         chaine = ""
    #         list_qte_prod = [[q, p] for q, p in zip(liste_qte_cmd, liste_prod_cmd)]
    #         for i, p in enumerate(liste_prod_cmd):
    #             chaine += f" {chr(9658)} {liste_qte_cmd[i]} {p}"
    #             if i == 1:
    #                 chaine += "..."
    #                 break
    #         if it % 2 == 0:
    #             self.mini_treeview_cmd.insert("", index=0, id=f"{it}",
    #                                           values=(
    #                                               cmd[0], chaine, cmd[4], change_date_format(cmd[3].date()), cmd[-2]),
    #                                           tags=("even",))
    #
    #         else:
    #             self.mini_treeview_cmd.insert("", index=0, id=f"{it}",
    #                                           values=(
    #                                               cmd[0], chaine, cmd[4], change_date_format(cmd[3].date()), cmd[-2]),
    #                                           tags=("odd",))
    #         for couple in list_qte_prod:
    #             self.mini_treeview_cmd.insert(str(it), END, str(h), values=couple)
    #             h -= 1
    #     ma_base_donnee.close()
    #     self.mini_treeview_cmd.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
    #     self.mini_treeview_cmd.tag_configure("even", background=couleur_inverse_tree, foreground=couleur_police_champs)

    # def remplir_on_expose(self, event):
    #     self.remplir_treeview_cmd_save_mini_order("date_save_commande")

    # def remplir_treeview_cmd_save_mini_order(self, colonn):
    #     """Remplir le tableau des commandes enregistrees selon l'ordre et la colonne en cours"""
    #     if self.control_id % 2 == 0:
    #         order = "ASC"
    #     else:
    #         order = "DESC"
    #     ma_base_donnee = connexion_bd_mysql()
    #     me_connect = ma_base_donnee.cursor()
    #     me_connect.execute(f"SELECT * FROM commande ORDER BY {colonn} {order};")
    #     liste_cmd = me_connect.fetchall()
    #     el = 0
    #     while self.mini_treeview_cmd:
    #         try:
    #             self.mini_treeview_cmd.delete(str(el))
    #         except:
    #             break
    #         el += 1
    #     h = 880000000
    #     for it, cmd in enumerate(liste_cmd):
    #         h -= 1
    #         liste_prod_cmd = cmd[1].split(",")
    #         liste_qte_cmd = cmd[2].split(",")
    #         chaine = ""
    #         list_qte_prod = [[q, p] for q, p in zip(liste_qte_cmd, liste_prod_cmd)]
    #         for i, p in enumerate(liste_prod_cmd):
    #             chaine += f" {chr(9658)} {liste_qte_cmd[i]} {p}"
    #             if i == 1:
    #                 chaine += "..."
    #                 break
    #         if it % 2 == 0:
    #             self.mini_treeview_cmd.insert("", index=0, id=f"{it}",
    #                                           values=(
    #                                               cmd[0], chaine, cmd[4], change_date_format(cmd[3].date()), cmd[-2]),
    #                                           tags=("even",))
    #
    #         else:
    #             self.mini_treeview_cmd.insert("", index=0, id=f"{it}",
    #                                           values=(
    #                                               cmd[0], chaine, cmd[4], change_date_format(cmd[3].date()), cmd[-2]),
    #                                           tags=("odd",))
    #         for couple in list_qte_prod:
    #             self.mini_treeview_cmd.insert(str(it), END, str(h), values=couple)
    #             h -= 1
    #     ma_base_donnee.close()
    #     self.mini_treeview_cmd.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
    #     self.mini_treeview_cmd.tag_configure("even", background=couleur_inverse_tree, foreground=couleur_police_champs)
    #     self.control_id += 1
    #
    # def popup_action_tree_cmd_mini(self, event):
    #     selection = self.mini_treeview_cmd.selection()
    #     if selection and len(selection) == 1:
    #         menu_popup_action_credit = Menu(self.mini_treeview_cmd, tearoff=0,
    #                                         title="Action sur les commandes enregistrees")
    #         menu_popup_action_credit.add_command(label=f"Utiliser cette commande",
    #                                              command=lambda: self.commande_save_use_mini(0))
    #         menu_popup_action_credit.add_command(label=f"Vendre sans modifier", command=self.vendre_direct_cmd_mini)
    #         menu_popup_action_credit.add_separator()
    #         menu_popup_action_credit.add_command(label=f"Supprimer cette commande", command=self.supp_cmdv_save_mini)
    #         x, y = fenetre_principale.winfo_pointerxy()
    #         menu_popup_action_credit.tk_popup(x, y)
    #
    # def vendre_direct_cmd_mini(self):
    #     """Vendre directement une commande preenregistree"""
    #     if control_mode_panier_pu.get() == 1:
    #         desactiv_mode_panier()
    #     self.commande_save_use_mini(0)
    #     fenetre_principale.after(25, enregistrer_vente, 0)
    #
    # def supp_cmdv_save_mini(self):
    #     """Supprimer une commande enregistree"""
    #     selection = self.mini_treeview_cmd.selection()
    #     valeur_select = self.mini_treeview_cmd.item(selection[0])
    #     ma_base_donnee = connexion_bd_mysql()
    #     connexion_use_vente = ma_base_donnee.cursor()
    #     num_cmd = valeur_select["values"]
    #     connexion_use_vente.execute(
    #         f"DELETE FROM `bd_gestion_del_blanco`.`commande` WHERE (`id_commande` = '{num_cmd[0]}');")
    #     ma_base_donnee.commit()
    #     ma_base_donnee.close()
    #     messagebox.showinfo(nom_ets, "Commande suppprimée avec succès")
    #     mini_cmd.remplir_treeview_cmd_save_mini_order("date_save_commande")
    #
    # def commande_save_use_mini(self, event):
    #     """Utiliser une commande enregistrees"""
    #     bouton_plus_prod1.invoke()
    #     selection = self.mini_treeview_cmd.selection()
    #     valeur_select = self.mini_treeview_cmd.item(selection[0])
    #     ma_base_donnee = connexion_bd_mysql()
    #     connexion_use_vente = ma_base_donnee.cursor()
    #     num_cmd = valeur_select["values"]
    #     connexion_use_vente.execute(f"SELECT * FROM commande WHERE id_commande = '{num_cmd[0]}';")
    #     data_cmd = connexion_use_vente.fetchone()
    #     ma_base_donnee.close()
    #     produit_cmd = data_cmd[1].split(",")
    #     qte_cmd = data_cmd[2].split(",")
    #     pu_cmd = data_cmd[-1].split(",")
    #     while len(produit_cmd) < 100:
    #         produit_cmd.append("")
    #     while len(qte_cmd) < 100:
    #         qte_cmd.append("")
    #     while len(pu_cmd) < 100:
    #         pu_cmd.append("")
    #
    #     for ch in liste_champs_prod_vente:
    #         ch.delete(0, END)
    #     for ch in liste_champs_qte_vente:
    #         ch.delete(0, END)
    #     for ch in liste_champs_pu_vente:
    #         ch.config(state=NORMAL)
    #         ch.delete(0, END)
    #     i = 0
    #     for champ in liste_champs_prod_vente:
    #         try:
    #             champ.insert(0, produit_cmd[i])
    #         except:
    #             break
    #         i += 1
    #     i = 0
    #     for champs in liste_champs_qte_vente:
    #         try:
    #             champs.insert(0, qte_cmd[i])
    #         except:
    #             break
    #         i += 1
    #     if data_cmd[-2]:
    #         ficheClient.nom_client_champs.delete(0, END)
    #         ficheClient.nom_client_champs.insert(0, data_cmd[-2])
    #
    #     i = 0
    #     for p in range(0, 90, 10):
    #         liste_prod_page_vente[i].set("?".join(produit_cmd[p:p + 10]))
    #         liste_qte_page_vente[i].set("?".join(qte_cmd[p:p + 10]))
    #         liste_pu_page_vente[i].set("?".join(pu_cmd[p:p + 10]))
    #         liste_result_page_vente[i].set(
    #             str(sum(int(check_empty_and_replace_with_give(qte_cmd[p:p + 10][produit_cmd[p:p + 10].index(h)], 0)) *
    #                     float(check_empty_and_replace_with_give(pu_cmd[p:p + 10][produit_cmd[p:p + 10].index(h)], 0))
    #                     for h in produit_cmd[p:p + 10] if h)))
    #         i += 1
    #
    #     if (not ficheClient.nom_client_champs.get()) and data_cmd[-1]:
    #         ficheClient.nom_client_champs.insert(0, data_cmd[-1])
    #
    #     fenetre_principale.after(5, supp_all_prod_no_pu)
