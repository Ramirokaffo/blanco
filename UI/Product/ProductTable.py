from datetime import date
from tkinter import *

from DATA.SettingClass.Product import Product
from STATIC.ConstantFile import *
from tkinter import ttk, messagebox, simpledialog
import asyncio

from Service.ImageService import redimension_icone


class ProductTable(Frame):

    def __init__(self, master: Misc, height=23, page: int = 0, count: int = 40):
        super().__init__(master, height=height)
        self.page = page
        self.count = count
        self.pack(expand=YES)
        self.master = master
        self.height = height
        self.item_count = 0
        self.fill_function = None
        self.is_fetching = False

        self.fenetre_info_vente = Frame(self.master, bg=couleur_sous_fenetre)
        self.variable_control_recherche = IntVar()
        self.variable_control_recherche.set(0)
        # self.fonction_validation_recherche_vente = self.fenetre_info_vente.register(lambda: self.show_search_result(0))

        self.frame_recherche = LabelFrame(self.fenetre_info_vente, text="", width=10,
                                          bg=couleur_sous_fenetre, bd=bd_widget, relief=relief_widget,
                                          labelanchor=N, fg=couleur_police)
        self.frame_recherche.pack(anchor="nw")
        self.variable_flexible_info_vente = StringVar()
        self.variable_flexible_montant_total = StringVar()

        self.label_rechercher = Label(self.fenetre_info_vente, bg=couleur_bouton, fg=couleur_police,
                                      textvariable=self.variable_flexible_info_vente)
        self.label_rechercher.place(x=1, y=20)
        self.recherche_icone = redimension_icone(image_recherche, 20, 15)
        self.label_recherche_icone = Label(self.frame_recherche, image=self.recherche_icone)
        self.label_recherche_icone.grid(row=1, column=0)
        self.label_recherche_icone.image = self.recherche_icone
        self.recherche_num_vente = Label(self.frame_recherche, text="Rechercher", bg=couleur_label,
                                         fg=couleur_police)
        self.recherche_num_vente.grid(row=1, column=1)
        self.product_search_input_field = Entry(self.frame_recherche,
                                                # validate="key",
                                                # validatecommand=self.fonction_validation_recherche_vente,
                                                )
        self.product_search_input_field.grid(row=1, column=2)

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

        self.scroll_bar_y = Scrollbar(self.frame_mil_vente, troughcolor="blue", bg="yellow")
        self.scroll_bar_y.pack(fill=Y, side=RIGHT)
        self.scroll_bar_x = Scrollbar(self.frame_mil_vente, troughcolor="blue", bg="yellow",
                                      orient=HORIZONTAL)
        self.scroll_bar_x.pack(fill=X, side=BOTTOM)
        self.colone = [str(j) for j in range(1, 11)]
        self.table = ttk.Treeview(self.frame_mil_vente, selectmode=EXTENDED, height=int(self.height),
                                  style="mystyle.Treeview",
                                  yscrollcommand=self.table_y_scroll_command, columns=self.colone,
                                  show="headings", padding=[20, 8, 90, 20],
                                  xscrollcommand=self.scroll_bar_x.set)

        self.table.bind("<<TreeviewSelect>>", self.affiche_auto_info_vente)
        self.table.heading("1", text="Code", anchor=W)
        self.table.heading("2", text="Nom", anchor=W)
        self.table.heading("3", text="Stock", anchor=W)
        self.table.heading("4", text="Marque", anchor=E)
        self.table.heading("5", text="Grammage", anchor=W)
        self.table.heading("6", text="Unité", anchor=E)
        self.table.heading("7", text="Catégorie", anchor=W)
        self.table.heading("8", text="Rayon", anchor=E)
        self.table.heading("9", text="Gamme", anchor=W)
        self.table.heading("10", text="Description", anchor=W)

        self.table.column("1", width=100, minwidth=50, anchor=W)
        self.table.column("2", width=350, minwidth=100, anchor=W)
        self.table.column("3", width=150, minwidth=100, anchor=E)
        self.table.column("4", width=80, minwidth=50, anchor=W)
        self.table.column("5", width=119, minwidth=150, anchor=E)
        self.table.column("6", width=119, minwidth=100, anchor=W)
        self.table.column("7", width=119, minwidth=100, anchor=E)
        self.table.column("8", width=119, minwidth=100, anchor=W)
        self.table.column("10", width=119, minwidth=500, anchor=W)

        self.table.pack(expand=YES)
        self.scroll_bar_y.config(command=self.table.yview)
        self.scroll_bar_x.config(command=self.table.xview)

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
        self.table.bind("<<TreeviewSelect>>", self.affiche_auto_info_vente)
        self.bind("<Expose>", self.bind_on_expose)
        self.affiche_treeview(0)

    def bind_on_expose(self, event):
        self.master.master.master.master.master.master.bind("<Return>", self.show_search_result)

    def table_y_scroll_command(self, first, last):
        self.scroll_bar_y.set(first, last)
        if not self.is_fetching and float(last) > 0.9:
            self.is_fetching = True
            asyncio.run(self.fetch_data_async(page=self.page + 1, count=self.count))

    async def fetch_data_async(self, page: int, count: int):
        list_product: list[Product] = self.fill_function(page, count)
        if len(list_product) != 0:
            self.page += 1
        self.insert_table_line(list_product)
        self.is_fetching = False

    def displays(self):
        self.fenetre_info_vente.pack(expand=YES)
        return self.master

    def quit_fen_vente(self):
        self.master.destroy()
        return

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
        # if index_ligne_select:
        #     if not self.is_credit:
        #         self.popup_info_vente_normale(event)
        #     else:
        #         self.popup_info_vente_credit(event)

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)

    def make_function(self):
        search_input = self.product_search_input_field.get()
        if search_input:
            self.fill_function = lambda page, count: Product().get_search_result(search_input, page=page, count=count)
        else:
            self.fill_function = lambda page, count: Product().get_product_list(page=page, count=count)
        return self.fill_function

    def show_search_result(self, event):
        self.is_fetching = True
        self.clear_table()
        self.affiche_treeview(0)
        self.is_fetching = False

    def affiche_treeview(self, event):
        self.insert_table_line(self.make_function()(self.page, self.count))

    def insert_table_line(self, datas: list[Product]):
        product: Product
        for i, product in enumerate(datas):
            product.load_category()
            product.load_grammage_type()
            product.load_gamme()
            product.load_rayon()
            self.table.insert("", index=END, iid=str(self.item_count), tags=("even" if i % 2 else "odd",),
                              values=[product.code, product.name, product.stock, product.brand, product.grammage,
                                      product.grammage_type.name if product.grammage_type is not None else "",
                                      product.category.name if product.category is not None else "",
                                      product.rayon.name if product.rayon is not None else "",
                                      product.gamme.name if product.gamme is not None else "",
                                      product.description
                                      ], open=False)
            self.item_count += 1
        self.table.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
        self.table.tag_configure("even", background=couleur_inverse_tree, foreground=couleur_police_champs)




