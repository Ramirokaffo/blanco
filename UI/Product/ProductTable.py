from customtkinter import CTkToplevel

from DATA.SettingClass.Product import Product
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import *
from tkinter import ttk, messagebox
import asyncio

from Service.ImageService import redimension_icone
from UI.Home.Vente.VentePage import VentePage
from UI.SupplyPage.AddSupplyForm import AddSupplyForm


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
        self.table = ttk.Treeview(self.frame_mil_vente, selectmode=EXTENDED, height=int(self.height),
                                  style="mystyle.Treeview",
                                  yscrollcommand=self.table_y_scroll_command, columns=[str(j) for j in range(1, 11)],
                                  show="headings",
                                  xscrollcommand=self.scroll_bar_x.set)

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
        self.table.column("2", width=350, minwidth=300, anchor=W)
        self.table.column("3", width=150, minwidth=100, anchor=W)
        self.table.column("4", width=80, minwidth=150, anchor=E)
        self.table.column("5", width=119, minwidth=100, anchor=W)
        self.table.column("6", width=119, minwidth=100, anchor=E)
        self.table.column("7", width=119, minwidth=100, anchor=W)
        self.table.column("8", width=119, minwidth=100, anchor=E)
        self.table.column("9", width=119, minwidth=100, anchor=W)
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

        self.table.bind("<ButtonRelease-3>", self.show_table_popup)
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

    def show_table_popup(self, event):
        selected_line = self.table.selection()
        if selected_line:
            main_menu = Menu(self.table, tearoff=0, title="Action sur les produits avec stock "
                                                        "critic", relief=FLAT)
            main_menu.add_command(label=f"Approvisionnement", command=self.quick_supply)
            sale_sub_menu = Menu(main_menu, tearoff=False)
            sale_sub_menu.add_command(label="Ajouter à la vente courante",
                                      command=lambda: self.sale_selected_product(is_new_sale=False))
            sale_sub_menu.add_command(label="Nouvelle vente",
                                      command=lambda: self.sale_selected_product(is_new_sale=True))
            main_menu.add_cascade(label=f"Vendre", menu=sale_sub_menu)
            x, y = self.master.winfo_pointerxy()
            main_menu.tk_popup(x, y)

    def get_selected(self):
        lit_line_id = self.table.selection()
        return [Product.get_by_code(product_code=self.table.item(line_id)["values"][0]) for line_id in lit_line_id]

    def sale_selected_product(self, is_new_sale: bool = False):
        selected_product_list: list[Product] = self.get_selected()
        if len(selected_product_list) > 0:
            if not is_new_sale:
                if selected_product_list[0].stock == 0:
                    messagebox.showerror("Error", "Stock insuffisant pour ce produit !")
                    return
                right_page: VentePage = VentePage.get_shown_page()
                if not right_page:
                    right_page = VentePage.last_shown
                    if not right_page:
                        right_page = VentePage.list_sale_page[0].add_tab()
            else:
                right_page = VentePage.list_sale_page[0].add_tab()
            right_page.fill_tab_line_with_only_products(selected_product_list)

    def quick_supply(self):
        selected_product_list = self.get_selected()
        if len(selected_product_list) > 0:
            for product in selected_product_list:
                tl = CTkToplevel(self.master)
                tl.transient(self.winfo_toplevel())
                AddSupplyForm(tl, supply=Supply(product=product)).pack()

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




