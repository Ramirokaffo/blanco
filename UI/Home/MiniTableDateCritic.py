import asyncio
from tkinter import *
from tkinter import ttk, messagebox

from DATA.SettingClass.Product import Product
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import couleur_label, couleur_invers_treeeview, couleur_police_champs, couleur_inverse_tree
from UI.Home.Vente.VentePage import VentePage


class MiniTableDateCritic(Frame):

    def __init__(self, master, height: int = 12, page: int = 0, count: int = 40):
        super().__init__(master=master)
        self.master = master
        self.height = height
        self.page = page
        self.count = count
        self.fill_function = None
        self.is_fetching = False
        self.item_count = 0
        self.control_order = "ASC"
        self.barre_defilement_y = Scrollbar(self.master)
        self.barre_defilement_y.pack(fill=Y, side=RIGHT)
        self.barre_defilement_x = Scrollbar(self.master, orient=HORIZONTAL)
        self.barre_defilement_x.pack(fill=X, side=BOTTOM)
        self.table = ttk.Treeview(self.master, selectmode=EXTENDED, height=height,
                                  style="mystyle.Treeview",
                                  columns=[str(i) for i in range(4)], show="headings",
                                  # padding=[20, 8, 90, 20],
                                  yscrollcommand=self.table_y_scroll_command,
                                  xscrollcommand=self.barre_defilement_x.set)

        self.table.heading("0", text="Produits", anchor=W,
                           # command=lambda: self.remplir_treeviiew_stock_critic(
                           #     "designation_produit")
                           )
        self.table.heading("1", text="Date d'expiration", anchor=CENTER)
        self.table.heading("2", text="Stock", anchor=E)
        self.table.heading("3", text="Code", anchor=E)

        self.table.column("0", width=250, minwidth=50, anchor=W)
        self.table.column("1", width=100, minwidth=50, anchor=CENTER)
        self.table.column("2", width=50, minwidth=50, anchor=E)
        self.table.column("3", width=100, minwidth=50, anchor=E)
        self.table.pack(expand=YES)

        self.barre_defilement_y.config(command=self.table.yview)
        self.barre_defilement_x.config(command=self.table.xview)
        self.affiche_treeview(0)
        self.table.bind("<Double-ButtonRelease-1>", self.on_double_clic_product)
        self.table.bind("<ButtonRelease-3>", self.show_table_popup)

    def table_y_scroll_command(self, first, last):
        self.barre_defilement_y.set(first, last)
        if not self.is_fetching and float(last) > 0.9:
            self.is_fetching = True
            asyncio.run(self.fetch_data_async(page=self.page + 1, count=self.count))

    async def fetch_data_async(self, page: int, count: int):
        list_supply: list[Supply] = self.fill_function(page, count)
        if len(list_supply) != 0:
            self.page += 1
        self.insert_table_line(list_supply)
        self.is_fetching = False

    def get_selected(self):
        lit_line_id = self.table.selection()
        return [Product.get_by_code(product_code=self.table.item(line_id)["values"][-1]) for line_id in lit_line_id]

    def on_double_clic_product(self, event):
        self.sale_selected_product(is_new_sale=False)

    def sale_selected_product(self, is_new_sale: bool = False):
        selected_product_list: list[Product] = self.get_selected()
        if len(selected_product_list) > 0:
            if not is_new_sale:
                right_page: VentePage = VentePage.get_shown_page()
                if not right_page:
                    right_page = VentePage.last_shown
                    if not right_page:
                        right_page = VentePage.list_sale_page[0].add_tab()
                if selected_product_list[0].stock == 0:
                    messagebox.showerror("Error", "Stock insuffisant pour ce produit !")
                    return
            else:
                right_page = VentePage.list_sale_page[0].add_tab()
            right_page.fill_tab_line_with_only_products(selected_product_list)

    def show_table_popup(self, event):
        selected_line = self.table.selection()
        if selected_line:
            main_menu = Menu(self.table, tearoff=0, title="Action sur les produits qui periment bientot", relief=FLAT)
            sale_sub_menu = Menu(main_menu, tearoff=False)
            sale_sub_menu.add_command(label="Ajouter à la vente courante",
                                      command=lambda: self.sale_selected_product(is_new_sale=False))
            sale_sub_menu.add_command(label="Nouvelle vente",
                                      command=lambda: self.sale_selected_product(is_new_sale=True))
            main_menu.add_cascade(label=f"Vendre", menu=sale_sub_menu)
            x, y = self.master.winfo_pointerxy()
            main_menu.tk_popup(x, y)

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)

    def make_function(self):
        self.fill_function = lambda page, count: Supply.get_supply_with_date_critic(page=page, count=count)
        return self.fill_function

    def show_search_result(self, event):
        self.is_fetching = True
        self.clear_table()
        self.affiche_treeview(0)
        self.is_fetching = False

    def affiche_treeview(self, event):
        self.insert_table_line(self.make_function()(self.page, self.count))

    def insert_table_line(self, datas: list[Supply]):
        supply: Supply
        for i, supply in enumerate(datas):
            supply.load_product()
            self.table.insert("", index=END, iid=str(self.item_count), tags=("even" if i % 2 else "odd",),
                              values=[supply.product.name, supply.expiration_date, supply.product.stock, supply.product.code], open=False)
            self.item_count += 1
        self.table.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
        self.table.tag_configure("even", background=couleur_inverse_tree, foreground=couleur_police_champs)

