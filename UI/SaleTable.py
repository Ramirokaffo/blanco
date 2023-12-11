from DATA.SettingClass.Client import Client
from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Sale import Sale
from DATA.SettingClass.SaleProduct import SaleProduct
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import *
from tkinter import ttk, messagebox
import asyncio

from Service.DateTimeService import DateTimeService
from Service.ImageService import redimension_icone
from UI.Home.MiniDashboard import MiniDashboard


class SaleTable(Frame):

    def __init__(self, master: Misc, height=23, is_credit: bool = False, page: int = 0, count: int = 40,
                 is_daily: bool = True, daily_id: int = Daily.get_current_daily().id):

        super().__init__(master, height=height)
        self.is_credit = is_credit
        self.is_daily = is_daily
        self.daily_id = daily_id
        self.page = page
        self.count = count
        self.pack(expand=YES)
        self.master = master
        self.height = height
        self.item_count = 0
        self.fill_function = None
        self.is_fetching = False
        self.current_function = None

        self.fenetre_info_vente = Frame(self.master, bg=couleur_sous_fenetre)
        self.variable_control_recherche = IntVar()
        self.variable_control_recherche.set(0)
        self.fonction_validation_recherche_vente = self.fenetre_info_vente.register(self.fonction_recherche)

        self.frame_recherche = LabelFrame(self.fenetre_info_vente, text="", width=10,
                                          bg=couleur_sous_fenetre, bd=bd_widget, relief=relief_widget,
                                          labelanchor=N, fg=couleur_police)
        self.frame_recherche.pack(anchor=NW)
        self.variable_flexible_info_vente = StringVar()
        self.variable_flexible_montant_total = StringVar()
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
        self.search_client_entry = ttk.Combobox(self.frame_recherche, width=largeur_champs_achat,
                                                style="mystyle.TCombobox",
                                                font=(police, taille_police_texte),
                                                validate="key", postcommand=self.on_client_select,
                                                validatecommand=self.fonction_validation_recherche_vente,
                                                )
        self.search_client_entry.grid(row=1, column=4)

        self.recherche_nom_vendeur_vente = Label(self.frame_recherche, text="Vendu par:", bg=couleur_label,
                                                 fg=couleur_police)
        self.recherche_nom_vendeur_vente.grid(row=1, column=5)
        self.search_seller_entry = ttk.Combobox(self.frame_recherche, width=largeur_champs_achat,
                                                font=(police, taille_police_texte),
                                                validate="key", postcommand=self.on_seller_select)
        self.search_seller_entry.grid(row=1, column=6)

        self.frame_mil_vente = LabelFrame(self.fenetre_info_vente, text="", width=10,
                                          bg=couleur_sous_fenetre, bd=bd_widget, relief=relief_widget,
                                          labelanchor=N, fg=couleur_police)
        self.frame_mil_vente.pack(expand=YES)

        self.barre_defilement = Scrollbar(self.frame_mil_vente, troughcolor="blue", bg="yellow")
        self.barre_defilement.pack(fill=Y, side=RIGHT)
        self.barre_defilement_horiz_vent = Scrollbar(self.frame_mil_vente, troughcolor="blue", bg="yellow",
                                                     orient=HORIZONTAL)
        self.barre_defilement_horiz_vent.pack(fill=X, side=BOTTOM)
        self.table = ttk.Treeview(self.frame_mil_vente, selectmode=EXTENDED, height=int(self.height),
                                  yscrollcommand=self.table_y_scroll_command, columns=[str(j) for j in range(1, 7)],
                                show="tree headings", xscrollcommand=self.barre_defilement_horiz_vent.set)

        self.table.bind("<<TreeviewSelect>>", self.affiche_auto_info_vente)
        self.table.heading("1", text="N°", anchor="w")
        self.table.heading("2", text="Vendu par", anchor="w")
        self.table.heading("3", text="Date et heure de vente", anchor="c")
        self.table.heading("4", text="Montant total", anchor="c")
        self.table.heading("5", text="Client", anchor="w")
        self.table.heading("6", text="Type de vente", anchor="w")

        self.table.column("1", width=50, minwidth=50, anchor="w")
        self.table.column("2", width=250, minwidth=100, anchor="w")
        self.table.column("3", width=150, minwidth=100, anchor="c")
        self.table.column("4", width=200, minwidth=100, anchor="c")
        self.table.column("5", width=119, minwidth=150, anchor="w")
        self.table.column("6", width=119, minwidth=100, anchor="w")

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
        self.label_montant_vente.pack(side=RIGHT, anchor=SE)

        self.table.bind("<ButtonRelease-3>", self.popup_info_vente)
        self.search_client_entry.bind("<<ComboboxSelected>>", self.show_search_result)
        self.search_seller_entry.bind("<<ComboboxSelected>>", self.show_search_result)
        self.table.bind("<<TreeviewSelect>>", self.affiche_auto_info_vente)
        self.bind("<Expose>", self.bind_on_expose)
        self.affiche_treeview(0)

    def bind_on_expose(self, event):
        self.winfo_toplevel().bind("<Return>", self.show_search_result)
        self.reload_same_function()

    def on_client_select(self):
        self.search_client_entry.configure(values=[client.firstname for client in Client.get_all()])

    def on_seller_select(self):
        self.search_seller_entry.configure(values=[seller.firstname for seller in Staff.get_all()])

    def table_y_scroll_command(self, first, last):
        self.barre_defilement.set(first, last)
        if not self.is_fetching and float(last) > 0.9:
            self.is_fetching = True
            asyncio.run(self.fetch_data_async(page=self.page + 1, count=self.count))

    async def fetch_data_async(self, page: int, count: int):
        list_sale: list[Sale] = self.fill_function(page, count)
        if len(list_sale) != 0:
            self.page += 1
        self.insert_table_line(list_sale)
        self.is_fetching = False

    def get_selected_sale(self) -> list[Sale]:
        list_line_id = self.table.selection()
        list_selected_sale: list[Sale] = []
        for line_id in list_line_id:
            line_data = self.table.item(line_id)
            if "sale" in line_data["tags"]:
                list_selected_sale.append(Sale.get_by_id(line_data["values"][0]))
        return list_selected_sale

    def get_selected_sale_sale_product(self):
        sale_line_id = self.table.selection()[0]
        list_line_id = self.table.get_children(sale_line_id)
        list_selected_sale_sale_product: list[SaleProduct] = []
        for line_id in list_line_id:
            line_data = self.table.item(line_id)
            if "sale_product" in line_data["tags"]:
                list_selected_sale_sale_product.append(SaleProduct.get_by_id(sale_product_id=int(line_data["tags"][-1])))
        return list_selected_sale_sale_product

    def get_selected_sale_product(self):
        list_line_id = self.table.selection()[0]
        list_selected_sale_sale_product: list[SaleProduct] = []
        for line_id in list_line_id:
            line_data = self.table.item(line_id)
            if "sale_product" in line_data["tags"]:
                list_selected_sale_sale_product.append(SaleProduct.get_by_id(sale_product_id=int(line_data["values"][0])))
        print(self.table.item(list_line_id[0]))
        print(self.table.item(list_line_id[0])["values"])
        return list_selected_sale_sale_product

    def delete_selected_sale(self):
        selected_sales = self.get_selected_sale()
        list_re_stock = []
        if not messagebox.askyesno("DEL BLANCO", "Vous etes sur de vouloir supprimer cette vente ?"):
            return
        for sale in selected_sales:
            sale.soft_delete()
            list_re_stock += [[sale_product.product_count, sale_product.supply.id] for sale_product in SaleProduct.get_by_sale_id(sale_id=sale.id)]
        Supply.re_stock_many(list_re_stock)
        self.reload_same_function()
        messagebox.showinfo("DEL BLANCO", "Vente supprimée avec succès")
        MiniDashboard.reload_all_table()

    def reload_same_function(self):
        self.clear_table()
        self.affiche_treeview(0)

    def displays(self):
        self.fenetre_info_vente.pack(expand=YES)
        return self.master

    def quit_fen_vente(self):
        self.master.destroy()
        return

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
        index_ligne_select = self.table.selection()
        if index_ligne_select:
            #     print(table.item(index_ligne_select[0])["values"])
            #     valeur_ligne_select =f"{chr(9658)} {((table.item(index_ligne_select[0])['values'])[4].replace(f'{chr(9658)}', '+'))[2:]}"
            #     variable_flexible_info_vente.set(valeur_ligne_select)
            pass

    def fonction_recherche(self):
        # self.master.after(5, self.affiche_treeview, 0)
        return True

    def popup_info_vente_normale(self, event):
        self.get_selected_sale()
        index_ligne_select = self.table.selection()
        if index_ligne_select:
            menu_popup_info_vente = Menu(self.table, tearoff=0, title="Opérations sur les ventes", relief=FLAT)
            menu_popup_info_vente.add_command(
                label=f"Supprimer {'cette' if len(index_ligne_select) == 1 else 'ces'} vente"
                      f"{'' if len(index_ligne_select) == 1 else 's'}", compound=LEFT, command=self.delete_selected_sale)
            menu_popup_info_vente.add_command(label=f"Imprimer {'la' if len(index_ligne_select) == 1 else 'les'} "
                                                    f"Facture{' de cette vente' if len(index_ligne_select) == 1 else 's de ces ventes'}",
                                              command=lambda: self.facturier(self.table), compound=LEFT)
            menu_popup_info_vente.tk_popup(self.master.winfo_pointerx(), self.master.winfo_pointery())

    def popup_info_vente(self, event):
        index_ligne_select = self.table.selection()
        if index_ligne_select:
            if not self.is_credit:
                self.popup_info_vente_normale(event)
            # else:
            #     self.popup_info_vente_credit(event)

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

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)

    def make_function(self):
        staff_name = self.search_seller_entry.get()
        client_name = self.search_client_entry.get()
        sale_id = self.recherche_num_vente_champs.get()
        if sale_id or staff_name or client_name:
            self.fill_function = lambda page, count: Sale.get_sale_search(sale_id=sale_id,
                                                                            client_name=client_name,
                                                                            staff_name=staff_name,
                                                                            page=page, count=count,
                                                                          is_daily=self.is_daily,
                                                                          daily_id=self.daily_id)
        else:
            self.fill_function = lambda page, count: Sale.get_sale_list(page=page, count=count,
                                                                          is_daily=self.is_daily,
                                                                          daily_id=self.daily_id)
        return self.fill_function

    def show_search_result(self, event):
        self.is_fetching = True
        self.page = 0
        self.clear_table()
        self.affiche_treeview(0)
        self.is_fetching = False

    def affiche_treeview(self, event):
        self.current_function = lambda: self.insert_table_line(self.make_function()(self.page, self.count))
        self.current_function()

    def insert_table_line(self, datas: list[Sale]):
        for i, sale in enumerate(datas):
            sale.load_client()
            sale.load_staff()
            self.table.insert("", index=END, iid=str(self.item_count), tags=("even" if i % 2 else "odd", "sale"),
                              values=[sale.id, sale.staff.get_all_name() if sale.staff is not None else "",
                                      DateTimeService.format_date_time(sale.create_at), sale.total, sale.client.get_all_name() if sale.client is not None else "",
                                      "Crédit" if sale.is_credit else "Normale"], open=False)
            sub_line_parent = self.item_count
            self.item_count += 1
            sale_product: SaleProduct
            for j, sale_product in enumerate(SaleProduct.get_sale_product_sale_with_id(sale.id)):
                sale_product.load_supply().load_product()
                self.table.insert(str(sub_line_parent), END, str(self.item_count), tags=("even1" if j % 2 else "odd1", "sale_product", str(sale_product.id)),
                                  open=False,
                                  values=[sale_product.product_count, sale_product.supply.product.name,
                                          sale_product.unit_price])
                self.item_count += 1
        self.table.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
        self.table.tag_configure("even", background=couleur_inverse_tree, foreground=couleur_police_champs)


