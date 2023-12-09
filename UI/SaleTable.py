from datetime import date
from tkinter import *

from DATA.SettingClass.Sale import Sale
from DATA.SettingClass.SaleProduct import SaleProduct
from STATIC.ConstantFile import *
from tkinter import ttk, messagebox, simpledialog
import asyncio

from Service.DateTimeService import DateTimeService
from Service.ImageService import redimension_icone


class SaleTable(Frame):

    def __init__(self, master: Misc, height=23, is_credit: bool = False, page: int = 0, count: int = 40):

        super().__init__(master, height=height)
        self.is_credit = is_credit
        self.page = page
        self.count = count
        # self.vendeur_service = VendeurTableService()
        # self.liste_vendeur = self.vendeur_service.select_from_vendeur("prenom_vendeur")
        # self.service_table_vente = VenteTableService()
        # self.produit_table_service = ProduitTableService()
        self.pack(expand=YES)
        self.master = master
        self.height = height
        self.item_count = 0
        self.fill_function = None
        self.is_fetching = False
        # self.periode = periode
        # self.valeur = valeur
        # self.annee = annee
        # self.jour = jour
        # self.etat = etat
        # self.type_vente = type_vente

        self.fenetre_info_vente = Frame(self.master, bg=couleur_sous_fenetre)
        self.variable_control_recherche = IntVar()
        self.variable_control_recherche.set(0)
        self.fonction_validation_recherche_vente = self.fenetre_info_vente.register(self.fonction_recherche)

        self.frame_recherche = LabelFrame(self.fenetre_info_vente, text="", width=10,
                                          bg=couleur_sous_fenetre, bd=bd_widget, relief=relief_widget,
                                          labelanchor=N, fg=couleur_police)
        self.frame_recherche.pack(anchor="nw")
        self.variable_flexible_info_vente = StringVar()
        self.variable_flexible_montant_total = StringVar()
        # self.label_recherche = Label(self.fenetre_info_vente, bg=couleur_label, fg=couleur_police,
        #                              textvariable=self.variable_flexible_montant_total)
        # self.label_recherche.pack(anchor="se")
        self.label_rechercher = Label(self.fenetre_info_vente, bg=couleur_bouton, fg=couleur_police,
                                      textvariable=self.variable_flexible_info_vente)
        self.label_rechercher.place(x=1, y=20)
        self.recherche_icone = redimension_icone(image_recherche, 20, 15)
        self.label_recherche_icone = Label(self.frame_recherche, image=self.recherche_icone)
        self.label_recherche_icone.grid(row=1, column=0)
        self.label_recherche_icone.image = self.recherche_icone
        self.recherche_num_vente = Label(self.frame_recherche, text="N° de la vente:", bg=couleur_label,
                                         fg=couleur_police)
        self.recherche_num_vente.grid(row=1, column=1)
        self.recherche_num_vente_champs = Entry(self.frame_recherche, validate="key",
                                                validatecommand=self.fonction_validation_recherche_vente)
        self.recherche_num_vente_champs.grid(row=1, column=2)

        self.recherche_nom_client_vente = Label(self.frame_recherche, text="Nom du Client:", bg=couleur_label,
                                                fg=couleur_police)
        self.recherche_nom_client_vente.grid(row=1, column=3)
        self.recherche_nom_client_vente_champs = ttk.Combobox(self.frame_recherche, width=largeur_champs_achat,
                                                              style="mystyle.TCombobox",
                                                              font=(police, taille_police_texte),
                                                              # values=self.service_table_vente.selectionner_client_regulier(),
                                                              validate="key",
                                                              validatecommand=self.fonction_validation_recherche_vente,
                                                              # postcommand=self.service_table_vente.selectionner_client_regulier()
                                                              )
        self.recherche_nom_client_vente_champs.grid(row=1, column=4)

        self.recherche_nom_vendeur_vente = Label(self.frame_recherche, text="Vendu par:", bg=couleur_label,
                                                 fg=couleur_police)
        self.recherche_nom_vendeur_vente.grid(row=1, column=5)
        self.recherche_nom_vendeur_vente_champs = ttk.Combobox(self.frame_recherche, width=largeur_champs_achat,
                                                               font=(police,
                                                                     taille_police_texte),
                                                               validate="key",
                                                               validatecommand=self.fonction_validation_recherche_vente,
                                                               # postcommand=lambda: self.vendeur_service.select_from_vendeur(
                                                               #     "prenom_vendeur"), values=self.liste_vendeur,
                                                               # style="mystyle.TCombobox"
                                                               )
        self.recherche_nom_vendeur_vente_champs.grid(row=1, column=6)
        # self.recherche_nom_vendeur_vente_champs["values"] = liste_vendeur
        # if jour == date.today().day:
        self.recherche_heure_Jour_vente = Label(self.frame_recherche, text="Jour/Heure de la vente:", bg=couleur_label,
                                                fg=couleur_police)
        self.recherche_heure_Jour_vente.grid(row=1, column=7)
        self.recherche_heure_Jour_vente_champs = Entry(self.frame_recherche, validate="key",
                                                       validatecommand=self.fonction_validation_recherche_vente)
        self.recherche_heure_Jour_vente_champs.grid(row=1, column=8)
        self.recherche_heure_Jour_vente_champs.focus_set()
        # elif valeur in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
        #     self.recherche_heure_Jour_vente = Label(self.frame_recherche, text="Jour:", bg=couleur_label,
        #                                             fg=couleur_police)
        #     self.recherche_heure_Jour_vente.grid(row=1, column=7)
        #     self.recherche_heure_Jour_vente_champs = Entry(self.frame_recherche, validate="key",
        #                                                    validatecommand=self.fonction_validation_recherche_vente)
        #     self.recherche_heure_Jour_vente_champs.grid(row=1, column=8)
        #     self.recherche_heure_Jour_vente_champs.focus_set()

        # else:
        #     self.recherche_heure_Jour_vente = Label(self.frame_recherche, text="Trimestre:", bg=couleur_label,
        #                                             fg=couleur_police)
        #     # recherche_heure_Jour_vente.grid(row=1, column=7)
        #     self.recherche_heure_Jour_vente_champs = Entry(self.frame_recherche)
        #     # recherche_heure_Jour_vente_champs.grid(row=1, column=8)

        style_label = ttk.Style()
        style_label.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=(police, taille_police_texte),
                              bg="red",
                              fg="orange")
        style_label.configure("mystyle.Treeview.Heading", font=(police, taille_police_texte, "bold"), background="red")
        style_label.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])
        self.frame_mil_vente = LabelFrame(self.fenetre_info_vente, text="", width=10,
                                          bg=couleur_sous_fenetre, bd=bd_widget, relief=relief_widget,
                                          labelanchor=N, fg=couleur_police)
        self.frame_mil_vente.pack(expand=YES)

        self.barre_defilement = Scrollbar(self.frame_mil_vente, troughcolor="blue", bg="yellow")
        self.barre_defilement.pack(fill=Y, side=RIGHT)
        self.barre_defilement_horiz_vent = Scrollbar(self.frame_mil_vente, troughcolor="blue", bg="yellow",
                                                     orient=HORIZONTAL)
        self.barre_defilement_horiz_vent.pack(fill=X, side=BOTTOM)
        # self.is_credit = self.type_vente == "credit"
        # max_count = self.service_table_vente.select_max_count_id_relatif(type_vente=self.type_vente, etat=self.etat,
        #                                                                  periode=self.periode, valeur=self.valeur)
        self.colone = [str(j) for j in range(1, 7)]
        self.table = ttk.Treeview(self.frame_mil_vente, selectmode=EXTENDED, height=int(self.height),
                                  style="mystyle.Treeview",
                                  yscrollcommand=self.table_y_scroll_command, columns=self.colone,
                                show="tree headings", padding=[20, 8, 90, 20],
                                  xscrollcommand=self.barre_defilement_horiz_vent.set)
        # values = [sale.id, sale.is_paid, sale.create_at, sale.total])

        self.table.bind("<<TreeviewSelect>>", self.affiche_auto_info_vente)
        self.table.heading("1", text="N°", anchor="w")
        # self.table.heading("2", text="Nom du client", anchor="w")
        self.table.heading("2", text="Vendu par", anchor="w")
        self.table.heading("3", text="Date et heure de vente", anchor="c")
        self.table.heading("4", text="Montant total", anchor="c")
        self.table.heading("5", text="Client", anchor="w")
        self.table.heading("6", text="Type de vente", anchor="w")
        # if self.is_credit:
        #     self.table.heading("6", text="Avance", anchor="c")
        #     self.table.heading("7", text="Echéance", anchor="w")

        self.table.column("1", width=50, minwidth=50, anchor="w")
        self.table.column("2", width=250, minwidth=100, anchor="w")
        self.table.column("3", width=150, minwidth=100, anchor="c")
        self.table.column("4", width=200, minwidth=100, anchor="c")
        self.table.column("5", width=119, minwidth=150, anchor="w")
        self.table.column("6", width=119, minwidth=100, anchor="w")


        # for g, qpq in enumerate(range(8, int(max_count) * 30 - 2, 3)):
        #     self.table.heading(f"{qpq}", text=f"produit {g + 1}", anchor="w")
        #     self.table.heading(f"{qpq + 1}", text=f"Quantité {g + 1}", anchor="w")
        #     self.table.heading(f"{qpq + 2}", text=f"prix unitaire {g + 1}", anchor="w")
        #     self.table.column(f"{qpq}", width=200, minwidth=100, anchor="w")
        #     self.table.column(f"{qpq + 1}", width=100, minwidth=50, anchor="w")
        #     self.table.column(f"{qpq + 2}", width=150, minwidth=75, anchor="w")

        self.table.pack(expand=YES)
        self.barre_defilement.config(command=self.table.yview)
        self.barre_defilement_horiz_vent.config(command=self.table.xview)

        self.lf_retour_vente = LabelFrame(self.fenetre_info_vente, bg=couleur_sous_fenetre, bd=bd_widget,
                                          relief=relief_widget)
        self.lf_retour_vente.pack(side=BOTTOM, anchor=SW, fill=X)
        self.bout_retour_vente = Button(self.lf_retour_vente, text="<<Fermer>>", anchor=SW, command=self.quit_fen_vente)
        self.bout_retour_vente.pack(side=LEFT, anchor=SW)

        self.label_montant_vente = Label(self.lf_retour_vente, textvariable=self.variable_flexible_montant_total,
                                         anchor=SW, bg=couleur_sous_fenetre,
                                         font=(police, taille_police_texte + 3, "bold"))
        # if self.periode == "DAY":
        self.label_montant_vente.pack(side=RIGHT, anchor=SE)

        self.table.bind("<ButtonRelease-3>", self.popup_info_vente)
        # self.fenetre_info_vente.bind("<Expose>", appui_onglet_all)
        self.recherche_nom_client_vente_champs.bind("<<ComboboxSelected>>", self.affiche_treeview)
        self.recherche_nom_vendeur_vente_champs.bind("<<ComboboxSelected>>", self.affiche_treeview)

        # self.recherche_num_vente_champs.bind("<Enter>", self.details_seacrch_num_vnt)
        # self.recherche_nom_client_vente_champs.bind("<Enter>", self.details_search_combinee_vnt)
        # self.recherche_nom_vendeur_vente_champs.bind("<Enter>", self.details_search_combinee_vnt)
        # self.recherche_heure_Jour_vente_champs.bind("<Enter>", self.details_search_combinee_vnt)
        # self.table.bind("<Enter>", self.details_liste_vnt)
        # self.table.bind("<Expose>", self.affiche_treeview)
        self.table.bind("<<TreeviewSelect>>", self.affiche_auto_info_vente)
        self.bind("<Expose>", self.bind_on_expose)
        self.affiche_treeview(0)

    def bind_on_expose(self, event):
        self.master.master.master.master.master.master.bind("<Return>", self.show_search_result)

    def table_y_scroll_command(self, first, last):
        # print(first, last, type(last))
        self.barre_defilement.set(first, last)
        # print([self.table.size][0])
        # print(len(self.table.keys()), self.table.keys())
        # print(len(self.table.get_children()), self.table.get_children())

        if not self.is_fetching and float(last) > 0.9:
            self.is_fetching = True
            asyncio.run(self.fetch_data_async(page=self.page + 1, count=self.count))

    async def fetch_data_async(self, page: int, count: int):
        list_sale: list[Sale] = self.fill_function(page, count)
        if len(list_sale) != 0:
            self.page += 1
        self.insert_table_line(list_sale)
        self.is_fetching = False

    def displays(self):
        self.fenetre_info_vente.pack(expand=YES)
        return self.master

    def quit_fen_vente(self):
        self.master.destroy()
        return

    def annuler_vente_jr_selectionnee(self, table):
        index_ligne_select = table.selection()
        # question = messagebox.askyesno("DEL BLANCO", f"Voulez-vous vraiment supprimer "
        #                                         f"{'cette vente?' if len(index_ligne_select) == 1 else 'ces ventes?'}\ncette opération est ireversible")
        # if question:
        #     list_id_vent = []
        #     liste_statut = []
        #     if 5 == 5:
        #         for idt in index_ligne_select:
        #             list_id_vent += [((table.item(idt))["values"])[0]]
        #             liste_statut += [annul_vente_wid(((table.item(idt))["values"])[0], str(date.today()))]
        #         for i in index_ligne_select:
        #             table.delete(int(i))
        #         if len(liste_statut) == 1 and liste_statut == [False]:
        #             return
        #         elif len(liste_statut) != 1 and False in liste_statut:
        #             messagebox.showinfo(nom_ets,
        #                                 f"{liste_statut.count(True)} vente{'' if liste_statut.count(True) == 1 else 's'} "
        #                                 f"supprimée{'' if liste_statut.count(True) == 1 else 's'} sur {len(liste_statut)}!")
        #         else:
        #             messagebox.showinfo(nom_ets, f"Vente{'' if len(index_ligne_select) == 1 else 's'} "
        #                                          f"supprimée{'' if len(index_ligne_select) == 1 else 's'} avec succès!")
        #         # tableau_operationnel_manager.remplir_treeview_opera()
        #         # stock_critic_table.remplir_treeviiew_stock_critic()
        #         # ListeProduitVenteBoxInstance.remplir_listbox_regulier()
        #         # ListeProduitVenteBoxInstance.remplir_list_box_all_prod_vente()
        #     # except:
        #     #     messagebox.showerror("Erreur", "Erreur inconnue")

    def facturier(self, table):
        # global index_ligne_select
        index_ligne_select = table.selection()
        # if index_ligne_select:
        #     ma_base_donnee = connexion_bd_mysql()
        #     conexion_imprimer_vente = ma_base_donnee.cursor()
        #     for h in index_ligne_select:
        #         ligne_select = table.item(h)
        #         idvt = ligne_select["values"][0]
        #         conexion_imprimer_vente.execute(f"SELECT id_vente FROM vente WHERE id_vente = '{idvt}';")
        #         dd = conexion_imprimer_vente.fetchone()
        #         imprimer_vente_analyse_msedge(dd[0])
        # else:
        #     messagebox.showerror("Erreur", "Aucune vente sélectionnée")

    def affiche_auto_info_vente(self, event):
        """Afficher automatiquement les informations de la vente lorsque l'utilisateur clique sur une vente"""
        """variable_flexible_info_vente"""
        # print(fenetre_info_vente.focus_get())
        index_ligne_select = self.table.selection()
        if index_ligne_select:
            #     print(table.item(index_ligne_select[0])["values"])
            #     valeur_ligne_select =f"{chr(9658)} {((table.item(index_ligne_select[0])['values'])[4].replace(f'{chr(9658)}', '+'))[2:]}"
            #     variable_flexible_info_vente.set(valeur_ligne_select)
            pass

    def fonction_recherche(self):
        # self.master.after(5, self.affiche_treeview, 0)
        return True

    def popup_info_vente_credit(self, event):
        index_ligne_select = self.table.selection()
        menu_popup_info_vente = Menu(self.table, tearoff=0, title="Opérations sur les ventes à crédit", relief=FLAT)
        menu_popup_info_vente.add_command(label="Valider la vente", command=self.valider_vente)
        menu_popup_info_vente.add_command(label=f"Imprimer {'la' if len(index_ligne_select) == 1 else 'les'} "
                                                f"Facture{' de cette vente' if len(index_ligne_select) == 1 else 's de ces ventes'}",
                                          command=lambda: self.facturier(self.table), compound=LEFT)
        menu_popup_info_vente.add_separator()
        menu_popup_info_vente.add_command(label="Ajouter une tranche", command=self.ajouter_tranche_credit)
        menu_popup_info_vente.add_command(label="Modifier l'échéance", command=self.modifier_echeance)
        menu_popup_info_vente.add_separator()
        menu_popup_info_vente.add_command(
            label=f"Supprimer {'cette' if len(index_ligne_select) == 1 else 'ces'} vente"
                  f"{'' if len(index_ligne_select) == 1 else 's'}", compound=LEFT,
            command=lambda: self.annuler_vente_jr_selectionnee(self.table))

        menu_popup_info_vente.tk_popup(self.master.winfo_pointerx(), self.master.winfo_pointery())

    def popup_info_vente_normale(self, event):
        index_ligne_select = self.table.selection()
        if index_ligne_select:
            menu_popup_info_vente = Menu(self.table, tearoff=0, title="Opérations sur les ventes", relief=FLAT)
            menu_popup_info_vente.add_command(
                label=f"Supprimer {'cette' if len(index_ligne_select) == 1 else 'ces'} vente"
                      f"{'' if len(index_ligne_select) == 1 else 's'}", compound=LEFT,
                command=lambda: self.annuler_vente_jr_selectionnee(self.table))
            menu_popup_info_vente.add_command(label=f"Imprimer {'la' if len(index_ligne_select) == 1 else 'les'} "
                                                    f"Facture{' de cette vente' if len(index_ligne_select) == 1 else 's de ces ventes'}",
                                              command=lambda: self.facturier(self.table), compound=LEFT)
            menu_popup_info_vente.tk_popup(self.master.winfo_pointerx(), self.master.winfo_pointery())
        index_ligne_select = self.table.selection()
        menu_popup_info_vente = Menu(self.table, tearoff=0, title="Opérations sur les ventes", relief=FLAT)
        menu_popup_info_vente.add_command(
            label=f"Supprimer {'cette' if len(index_ligne_select) == 1 else 'ces'} vente"
                  f"{'' if len(index_ligne_select) == 1 else 's'}", compound=LEFT,
            command=lambda: self.annuler_vente_jr_selectionnee(self.table))
        menu_popup_info_vente.add_command(label=f"Imprimer {'la' if len(index_ligne_select) == 1 else 'les'} "
                                                f"Facture{' de cette vente' if len(index_ligne_select) == 1 else 's de ces ventes'}",
                                          command=lambda: self.facturier(self.table), compound=LEFT)
        menu_popup_info_vente.tk_popup(self.master.winfo_pointerx(), self.master.winfo_pointery())

    def popup_info_vente(self, event):
        index_ligne_select = self.table.selection()
        if index_ligne_select:
            if not self.is_credit:
                self.popup_info_vente_normale(event)
            else:
                self.popup_info_vente_credit(event)

    def ajouter_tranche_credit(self):
        index_ligne_select = self.table.selection()
        # if index_ligne_select:
        #     montant_tot_add = simpledialog.askfloat(title=nom_ets,
        #                                             prompt="Veuillez entrer le montant de la tranche à ajouter !")
        #     if montant_tot_add:
        #         if self.service_table_vente.update_vente_to_add_tranche(
        #                 id_r_vente=self.table.item(index_ligne_select[0])["values"][0],
        #                 tranche_amount=montant_tot_add):
        #             self.service_table_vente.confirmer()
        #             self.affiche_treeview(0)
        #             messagebox.showinfo(nom_ets, "Mise à jour éffectuée avec succès !")
        #         else:
        #             messagebox.showinfo(nom_ets, "Une erreur s'est produite !")

    def modifier_echeance(self):
        selection = self.table.selection()
        # ligne_select = self.table.item(selection[0])
        # valeur_ligne_select = ligne_select["values"]
        # new_value = simpledialog.askstring(title=nom_ets, prompt="Nouvelle échéance(AAAA-MM-JJ):")
        # if new_value:
        #     if self.service_table_vente.update_vente_change_column_data(column_name="echeance",
        #                                                                 new_value=new_value,
        #                                                                 where_column="id_relatif",
        #                                                                 where_value=valeur_ligne_select[0]):
        #         self.service_table_vente.confirmer()
        #         self.affiche_treeview(0)
        #         messagebox.showinfo(nom_ets, "Mise à jour éffectuée avec succès !")
        #     else:
        #         messagebox.showinfo(nom_ets, "Une erreur s'est produite !")

    def valider_vente(self):
        selection = self.table.selection()
        # ligne_select = self.table.item(selection[0])
        # if self.service_table_vente.update_vente_change_type("normal", ligne_select["values"][0]):
        #     self.service_table_vente.confirmer()
        #     messagebox.showinfo(nom_ets, "Vente validée avec succès !")
        #     self.affiche_treeview(0)
        # else:
        #     messagebox.showerror("Erreur", "Une erreur s'est produite lors de la validation de vente !")

    # def details_seacrch_num_vnt(self, event):
    #     info_bas_vente("Recherchez exclusivement avec le numero de la vente")

    # def details_search_combinee_vnt(self, event):
    #     info_bas_vente("Faites une recherche combinée avec le nom du vendeur, le nom du client et la date à laquelle"
    #                    " la vente a été éffectuée")

    # def details_liste_vnt(self, event):
    #     info_bas_vente(
    #         "Ici s'affiche la liste des ventes que vous avez éffectué; Cliquez sur une ou plusieurs ventes"
    #         " pour y éffectuer des actions")

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)

    def make_function(self):
        heure_vente_recherche_table = self.recherche_heure_Jour_vente_champs.get()
        staff_name = self.recherche_nom_vendeur_vente_champs.get()
        client_name = self.recherche_nom_client_vente_champs.get()
        sale_id = self.recherche_num_vente_champs.get()
        if sale_id or staff_name or client_name:
            self.fill_function = lambda page, count: Sale().get_sale_search(sale_id=sale_id,
                                                                            client_name=client_name,
                                                                            staff_name=staff_name,
                                                                            page=page, count=count)
        else:
            self.fill_function = lambda page, count: Sale().get_sale_list(page=page, count=count)
        return self.fill_function

    def show_search_result(self, event):
        self.is_fetching = True
        self.clear_table()
        self.affiche_treeview(0)
        self.is_fetching = False

    def affiche_treeview(self, event):
        self.insert_table_line(self.make_function()(self.page, self.count))

    def insert_table_line(self, datas: list[Sale]):
        for i, sale in enumerate(datas):
            sale.load_client()
            sale.load_staff()
            self.table.insert("", index=END, iid=str(self.item_count), tags=("even" if i % 2 else "odd",),
                              values=[sale.id, sale.staff.get_all_name() if sale.staff is not None else "",
                                      DateTimeService.format_date_time(sale.create_at), sale.total, sale.client.get_all_name() if sale.client is not None else "",
                                      "Crédit" if sale.is_credit else "Normale"], open=False)
            sub_line_parent = self.item_count
            self.item_count += 1
            for j, sale_product in enumerate(SaleProduct().get_sale_product_sale_with_id(sale.id)):
                sale_product.load_supply().load_product()
                self.table.insert(str(sub_line_parent), END, str(self.item_count), tags=("even1" if j % 2 else "odd1",),
                                  open=False,
                                  values=[sale_product.product_count, sale_product.supply.product.name,
                                          sale_product.unit_price])
                self.item_count += 1
        self.table.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
        self.table.tag_configure("even", background=couleur_inverse_tree, foreground=couleur_police_champs)


