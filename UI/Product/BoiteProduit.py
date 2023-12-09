
from DATA.SettingClass.Product import Product
from DATA.SettingClass.SaleProduct import SaleProduct
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import *
from UI.Home.Vente.VentePage import VentePage


class ProductBox:

    def __init__(self, master: Misc):
        self.master = master
        self.fonction_search_edit = self.master.register(self.on_search_input_change)

        self.frame_note_book_extrem_estbord = LabelFrame(self.master, text="",
                                                         labelanchor=N, bd=3, relief=RIDGE,
                                                         fg=couleur_police, bg=couleur_sous_fenetre)
        self.frame_note_book_extrem_estbord.place(x=1083, y=71, bordermode=INSIDE)

        self.frame_note_book_extrem_est = LabelFrame(self.frame_note_book_extrem_estbord, text="",
                                                     labelanchor=N, bd=bd_widget, relief=GROOVE,
                                                     fg=couleur_police, bg=couleur_sous_fenetre)
        self.frame_note_book_extrem_est.grid(row=1, column=1, padx=2, pady=2)

        self.label_frame_prod_vente = LabelFrame(self.frame_note_book_extrem_est,
                                                 labelanchor=N, bd=bd_widget, relief=relief_widget,
                                                 fg=couleur_police, bg=couleur_sous_fenetre)
        self.label_frame_prod_vente.pack(expand=YES)

        self.barre_defilement_prod_vente = Scrollbar(self.label_frame_prod_vente, orient=VERTICAL)
        self.barre_defilement_prod_vente.pack(fill=Y, side=RIGHT)

        self.scroll_bar_x = Scrollbar(self.label_frame_prod_vente, orient=HORIZONTAL)
        self.scroll_bar_x.pack(fill=X, side=BOTTOM)

        self.frame_recherch_champ_all_prod = LabelFrame(self.label_frame_prod_vente, bg=couleur_sous_fenetre,
                                                        bd=1, relief=SOLID, text="🔍Rechercher",
                                                        labelanchor=NW)
        self.frame_recherch_champ_all_prod.pack(side=TOP, anchor=W, pady=(0, 5), ipady=5, ipadx=2)

        # self.label_recherch_champ_all_prod_icone = Label(self.frame_recherch_champ_all_prod, text="🔍",
        #                                                  bg="whitesmoke",
        #                                                  bd=bd_widget, relief=relief_widget)
        # self.label_recherch_champ_all_prod_icone.pack(side=LEFT, fill=BOTH)

        self.recherch_champ_all_prod = Entry(self.frame_recherch_champ_all_prod,
                                             validate="key", validatecommand=
        (self.fonction_search_edit, '%P'),
                                             name="rv1", width=35)
        self.recherch_champ_all_prod.pack(fill=X)

        self.list_box_all_prod_vente = Listbox(self.label_frame_prod_vente, fg=couleur_police, bg=couleur_sous_fenetre,
                                               height=32, bd=bd_widget, relief=relief_widget
                                               , width=37, justify=LEFT,
                                               yscrollcommand=self.barre_defilement_prod_vente.set,
                                               xscrollcommand=self.scroll_bar_x.set,
                                               activestyle="dotbox",
                                               selectmode="extended")
        self.list_box_all_prod_vente.pack(expand=YES)

        self.barre_defilement_prod_vente.config(command=self.list_box_all_prod_vente.yview)
        self.scroll_bar_x.config(command=self.list_box_all_prod_vente.xview)

        self.fill_list()

        self.label_frame_prod_vente.bind("<B1-Motion>", self.move_list)
        self.frame_recherch_champ_all_prod.bind("<B1-Motion>", self.move_list)
        self.label_frame_prod_vente.bind("<Double-ButtonRelease-1>", lambda event: self.frame_note_book_extrem_estbord.destroy())
        self.frame_recherch_champ_all_prod.bind("<Double-ButtonRelease-1>", lambda event: self.frame_note_book_extrem_estbord.destroy())
        self.list_box_all_prod_vente.bind("<Double-ButtonRelease-1>", self.on_double_tap)
        # self.list_box_prod_regulier.bind("<Enter>", self.details_listbox_prod_regult)
        # self.list_box_all_prod_vente.bind("<Enter>", self.details_listbox_all_vnt_cliq)
        # self.recherch_champ_all_prod.bind("<Enter>", self.details_listbox_all_vnt)
        # self.list_box_prod_regulier.bind("<<ListboxSelect>>", self.recup_select_listbox_favoris)
        # self.list_box_all_prod_vente.bind("<<ListboxSelect>>", self.gestion_select_listbox)

    def on_double_tap(self, event):
        print("on double tap")
        shown_tab = VentePage.get_shown_page()
        if shown_tab is not None:
            products: list[Product] = self.get_selected_products()
            if len(products) > 0:
                current_supply: Supply = Supply().find_right_product_supply(product_id=products[0].id)
                if current_supply:
                    current_supply.product = products[0]
                else:
                    current_supply = Supply(product=products[0], unit_coast=0, unit_price=0)
                if not shown_tab.has_this_product(products[0]):
                    shown_tab.fill_tab_line_with_sale_product([SaleProduct(supply=current_supply, product_count=1,
                             unit_price=current_supply.unit_price if current_supply is not None else 0,
                             unit_coast=current_supply.unit_coast if current_supply is not None else 0)])
        return self.on_double_tap

    def get_selected_products(self):
        selected_line = self.list_box_all_prod_vente.curselection()
        print(selected_line)
        produit_selection = self.list_box_all_prod_vente.get(selected_line[0])
        print(produit_selection)
        return [Product().find_product_by_name(name=self.list_box_all_prod_vente.get(line_id)) for line_id in selected_line]


    def move_list(self, event):
        x, y = self.master.winfo_pointerxy()
        self.frame_note_book_extrem_estbord.place_configure(x=x - 30, y=y - 50, )

    def on_search_input_change(self, quoi):
        self.master.after(5, self.fill_list)
        return True

    # def affiche_list_box_prod(self, event):
    #     # global control_listbox_prod
    #     if not self.frame_note_book_extrem_estbord.winfo_ismapped():
    #         self.frame_note_book_extrem_estbord.place(x=1083, y=71, bordermode=INSIDE)
    #     else:
    #         self.frame_note_book_extrem_estbord.place_forget()
        # control_listbox_prod += 1

    # def recup_select_listbox_favoris(self, event):
    #     """Recuperer le produit selectionné dans la listbox des produits pour vendre"""
    #     produit_selectionne = self.list_box_prod_regulier.curselection()
    #     # print(frame_produit_qte_pu.winfo_ismapped())
    #     if not produit_selectionne or not frame_produit_qte_pu.winfo_ismapped():
    #         return
    #     produit_selection = self.list_box_prod_regulier.get(produit_selectionne[0])
    #     recup_select_listbox(produit_selection, self.remplir_listbox_regulier)
    #     info_bas_vente("Vous pouvez maintenant modifier le prix du produit que vous venez de selectionner")

    # def gestion_select_listbox(self, event):
    #     """La liste des produit est universelle, quand on selectionne un produit, il faut
    #     verifer la page sur laquelle on se trouve pour pouvoir reagir correctement"""
    #     # produ_selectionne = treeview_info_produit.selection()
    #     # ligne_select_opera = treeview_info_produit.item(produ_selectionne[0])
    #     # valeur_ligne_select_opera = ligne_select_opera["values"]
    #     if note_book_principale.tab(tab_id="current")["text"] == "Accueil":
    #         self.recup_select_listbox_all_prod()
    #         fenetre_consultation_produit.winfo_ismapped()
    #     elif note_book_principale.tab(tab_id="current")["text"] == "Approvisionnement":
    #         insert_prod_approv()
    #     elif treeview_info_produit_select(0) == "Analyse descriptive":
    #         affiche_analyse_desc_indiv()

    # def recup_select_listbox_all_prod(self):
    #
    #     """Recuperer le produit selectionné dans la listbox des produits pour vendre"""
    #     produit_selectionne = self.list_box_all_prod_vente.curselection()
    #     if not produit_selectionne or not frame_produit_qte_pu.winfo_ismapped():
    #         return
    #     produit_selection = self.list_box_all_prod_vente.get(produit_selectionne[0])
    #     # control_prod_plot.set(produit_selection)
    #     # return
    #     recup_select_listbox(produit_selection, self.remplir_list_box_all_prod_vente)
    #     info_bas_vente("Vous pouvez maintenant modifier le prix du produit que vous venez de selectionner")

    # def remplir_listbox_regulier(self, ajour_autre=0):
    #     liste_prod_deja = [p.get() for p in liste_champs_prod_vente]
    #     liste_prod_deja += [s for s in control_nbr_page_vent_rempli.get().split("?") if not s in liste_prod_deja]
    #     liste_prod_deja += [d for l in liste_prod_page_vente for d in l.get().split("?")]
    #     # for l in liste_prod_page_vente:
    #     #     liste_prod_deja += l.get().split("?")
    #     ma_base_donnee = connexion_bd_mysql()
    #     selectionner_info_produit = ma_base_donnee.cursor()
    #     selectionner_info_produit.execute(
    #         f"SELECT designation_produit FROM produit WHERE favoris = 'oui' and quantite_stock_produit != '0';")
    #     liste_prod_favoris = selectionner_info_produit.fetchall()
    #     selectionner_info_produit.execute(
    #         f"SELECT designation_produit FROM produit WHERE nombre_vendu != '0' and quantite_stock_produit != '0' "
    #         f"order BY nombre_vendu DESC;")
    #     liste_produit_regulier = selectionner_info_produit.fetchall()
    #     ma_base_donnee.close()
    #     self.list_box_prod_regulier.delete(0, END)
    #     i = 0
    #     for produits in liste_prod_favoris:
    #         if produits[0] in liste_prod_deja:
    #             continue
    #         self.list_box_prod_regulier.insert(END, produits[0])
    #         if i % 2 == 0:
    #             self.list_box_prod_regulier.itemconfig(i, background=couleur_inverse_tree,
    #                                                    foreground=couleur_police_champs)
    #         else:
    #             self.list_box_prod_regulier.itemconfig(i, background=couleur_inverse_tree,
    #                                                    foreground=couleur_invers_treeeview)
    #         i += 1
    #     liste_produit_regulier = [l for l in liste_produit_regulier if not l in liste_prod_favoris]
    #     for produits in liste_produit_regulier:
    #         if produits[0] in liste_prod_deja:
    #             continue
    #         self.list_box_prod_regulier.insert(END, produits[0])
    #         if i % 2 == 0:
    #             self.list_box_prod_regulier.itemconfig(i, background="whitesmoke", foreground=couleur_police_champs)
    #         else:
    #             self.list_box_prod_regulier.itemconfig(i, background="whitesmoke", foreground=couleur_invers_treeeview)
    #         i += 1
    #     if ajour_autre == 0:
    #         self.remplir_list_box_all_prod_vente(1)
    #     return True

    def fill_list(self):
        print(self.recherch_champ_all_prod.get())
        self.list_box_all_prod_vente.delete(0, END)
        list_product = Product().find_sale_product(self.recherch_champ_all_prod.get())
        self.list_box_all_prod_vente.insert(END, *list_product)
        # i = 0
        # for produits in list_product:
        #     self.list_box_all_prod_vente.insert(END, produits)
        #     if i % 2 == 0:
        #         self.list_box_all_prod_vente.itemconfig(i, background="whitesmoke", foreground=couleur_police_champs)
        #     else:
        #         self.list_box_all_prod_vente.itemconfig(i, background="whitesmoke", foreground=couleur_invers_treeeview)
        #     i += 1

    # def recherche_prod_vente_lisbox(self, produit):
    #     """Rechercher dans la listbox des produits en vente"""
    #     liste_prod_deja = [p.get() for p in liste_champs_prod_vente]
    #     liste_prod_deja += [s for s in control_nbr_page_vent_rempli.get().split("?") if not s in liste_prod_deja]
    #     ma_base_donnee = connexion_bd_mysql()
    #     selectionner_info_produit = ma_base_donnee.cursor()
    #     selectionner_info_produit.execute(
    #         f"SELECT designation_produit FROM produit WHERE designation_produit LIKE '%{produit}%' and quantite_stock_produit != '0'")
    #     liste_info_produit = selectionner_info_produit.fetchall()
    #     selectionner_info_produit.execute(
    #         f"SELECT designation_produit FROM produit WHERE id_produit LIKE '%{produit}%' and quantite_stock_produit != '0'")
    #     liste_info_produite = selectionner_info_produit.fetchall()
    #     liste_info_produite = [h for h in liste_info_produite if not h in liste_info_produit]
    #     liste_info_produit += liste_info_produite
    #     selectionner_info_produit.execute(
    #         f"SELECT designation_produit FROM produit WHERE categorie_produit LIKE '%{produit}%' and quantite_stock_produit != '0'")
    #     liste_info_produite1 = selectionner_info_produit.fetchall()
    #     liste_info_produite1 = [g for g in liste_info_produite1 if not g in liste_info_produit]
    #     liste_info_produit += liste_info_produite1
    #     selectionner_info_produit.execute(
    #         f"SELECT designation_produit FROM produit WHERE marque_produit LIKE '%{produit}%' and quantite_stock_produit != '0'")
    #     liste_info_produite2 = selectionner_info_produit.fetchall()
    #
    #     liste_info_produite2 = [g for g in liste_info_produite2 if not g in liste_info_produit]
    #     liste_info_produit += liste_info_produite2
    #     selectionner_info_produit.execute(
    #         f"SELECT designation_produit FROM produit WHERE description_produit LIKE '%{produit}%' and quantite_stock_produit != '0'"
    #         f"ORDER BY designation_produit ASC")
    #     liste_info_produite3 = selectionner_info_produit.fetchall()
    #     liste_info_produite3 = [g for g in liste_info_produite3 if not g in liste_info_produit]
    #     liste_info_produit += liste_info_produite3
    #     liste_prod_deja += [t for l in liste_prod_page_vente for t in l.get().split("?")]
    #     # for l in liste_prod_page_vente:
    #     #     liste_prod_deja += l.get().split("?")
    #     self.list_box_all_prod_vente.delete(0, END)
    #     i = 0
    #     for produits in liste_info_produit:
    #         if produits[0] in liste_prod_deja:
    #             continue
    #         self.list_box_all_prod_vente.insert(END, produits[0])
    #         if i % 2 == 0:
    #             self.list_box_all_prod_vente.itemconfig(i, background="whitesmoke", foreground=couleur_police_champs)
    #         else:
    #             self.list_box_all_prod_vente.itemconfig(i, background="whitesmoke", foreground=couleur_invers_treeeview)
    #         i += 1
    #     ma_base_donnee.close()
    #     return True
    #
    # def details_listbox_prod_regult(self, event):
    #     info_bas_vente(
    #         "Les produits favoris et reguliers s'affichent dans ce cadre. Selectionnez ceux dont vous voulez vendre")
    #
    # def details_listbox_all_vnt_cliq(self, event):
    #     info_bas_vente("Cliquez sur un produit")
    #
    # def details_listbox_all_vnt(self, event):
    #     info_bas_vente("Faite une recherche plus large sur les produits par rapport aux listes deroulantes")
