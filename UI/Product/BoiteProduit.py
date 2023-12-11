from tkinter import ttk

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
                                                         labelanchor=N, bd=3, relief=RAISED,
                                                         fg=couleur_police, bg=couleur_sous_fenetre)
        self.frame_note_book_extrem_estbord.place(x=1003, y=31, bordermode=INSIDE)

        self.frame_note_book_extrem_est = LabelFrame(self.frame_note_book_extrem_estbord, text="",
                                                     labelanchor=N, bd=bd_widget, relief=FLAT,
                                                     fg=couleur_police, bg=couleur_sous_fenetre)
        self.frame_note_book_extrem_est.grid(row=1, column=1, ipadx=5, ipady=5, pady=5, padx=5)

        self.label_frame_prod_vente = LabelFrame(self.frame_note_book_extrem_est,
                                                 labelanchor=N,
                                                 # bd=1, relief=RAISED,
                                                 fg=couleur_police, bg=couleur_sous_fenetre)
        self.label_frame_prod_vente.pack(expand=YES, ipadx=5, ipady=5, pady=5, padx=5)

        self.barre_defilement_prod_vente = Scrollbar(self.label_frame_prod_vente, orient=VERTICAL)
        self.barre_defilement_prod_vente.pack(fill=Y, side=RIGHT)

        self.scroll_bar_x = Scrollbar(self.label_frame_prod_vente, orient=HORIZONTAL)
        self.scroll_bar_x.pack(fill=X, side=BOTTOM)

        self.frame_recherch_champ_all_prod = LabelFrame(self.label_frame_prod_vente, bg=couleur_sous_fenetre,
                                                        bd=0, relief=FLAT,
                                                        text="🔍Rechercher",
                                                        labelanchor=NW)
        self.frame_recherch_champ_all_prod.pack(side=TOP, anchor=CENTER, pady=(0, 2), ipady=5, ipadx=2)
        self.recherch_champ_all_prod = Entry(self.frame_recherch_champ_all_prod,
                                             validate="key", validatecommand= (self.fonction_search_edit, '%P'), width=35)
        self.recherch_champ_all_prod.pack(fill=X)
        ttk.Separator(self.label_frame_prod_vente, orient=HORIZONTAL).pack(fill=X)

        self.list_box_all_prod_vente = Listbox(self.label_frame_prod_vente, fg=couleur_police, bg=couleur_sous_fenetre,
                                               height=32, bd=0, relief=relief_widget
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
        self.frame_note_book_extrem_estbord.bind("<B1-Motion>", self.move_list)
        self.label_frame_prod_vente.bind("<Double-ButtonRelease-1>", lambda event: self.frame_note_book_extrem_estbord.destroy())
        self.frame_note_book_extrem_estbord.bind("<Double-ButtonRelease-1>", lambda event: self.frame_note_book_extrem_estbord.destroy())
        self.frame_recherch_champ_all_prod.bind("<Double-ButtonRelease-1>", lambda event: self.frame_note_book_extrem_estbord.destroy())
        self.list_box_all_prod_vente.bind("<Double-ButtonRelease-1>", self.on_double_tap)

    def on_double_tap(self, event):
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
        return [Product().find_product_by_name(name=self.list_box_all_prod_vente.get(line_id)) for line_id in selected_line]

    def move_list(self, event):
        x, y = self.master.winfo_pointerxy()
        self.frame_note_book_extrem_estbord.place_configure(x=x - 30, y=y - 50, )

    def on_search_input_change(self, quoi):
        self.master.after(5, self.fill_list)
        return True

    def fill_list(self):
        self.list_box_all_prod_vente.delete(0, END)
        list_product = Product().find_sale_product(self.recherch_champ_all_prod.get())
        self.list_box_all_prod_vente.insert(END, *list_product)
