from tkinter import ttk

from customtkinter import CTkScrollableFrame

from DATA.SettingClass.Product import Product
from DATA.SettingClass.ProductImage import ProductImage
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import *
from UI.Images.ImageManager import ImageManager


class ProductDetailsPage(Frame):

    def __init__(self, master, product_id: int):
        super().__init__(master)
        self.product = Product.get_by_id(product_id=product_id)
        super_main_frame = CTkScrollableFrame(self, bg_color=couleur_sous_fenetre, fg_color="white",
                                              orientation=VERTICAL, width=665,
                                              height=600)
        super_main_frame.pack()
        table_frame = Frame(super_main_frame)
        table_frame.grid(row=1, column=1)

        self.scroll_bar_y = Scrollbar(table_frame, troughcolor="blue", bg="yellow")
        self.scroll_bar_y.pack(fill=Y, side=RIGHT)
        self.scroll_bar_x = Scrollbar(table_frame, troughcolor="blue", bg="yellow",
                                      orient=HORIZONTAL)
        self.scroll_bar_x.pack(fill=X, side=BOTTOM)
        self.table = ttk.Treeview(table_frame, selectmode=EXTENDED, height=12,
                                  style="mystyle.Treeview",
                                  yscrollcommand=self.scroll_bar_y.set, columns=list(str(i) for i in range(1, 3)),
                                  show="headings",
                                  xscrollcommand=self.scroll_bar_x.set)

        self.table.heading("1", text="Caractéristique", anchor=W)
        self.table.heading("2", text="Valeur", anchor=E)

        self.table.column("1", width=350, minwidth=50, anchor=W)
        self.table.column("2", width=300, minwidth=100, anchor=E)

        self.table.pack(expand=YES)
        self.scroll_bar_y.config(command=self.table.yview)
        self.scroll_bar_x.config(command=self.table.xview)

        self.product.load_category()
        self.product.load_grammage_type()
        self.product.load_gamme()
        self.product.load_rayon()
        self.supply = Supply().find_right_product_supply(product_id=product_id)
        frame_description_product = LabelFrame(super_main_frame, text="Description du produit", background=couleur_sous_fenetre)
        frame_description_product.grid(row=2, column=1, sticky=EW, ipady=10)
        Label(frame_description_product, text=self.product.description if self.product.description is not None
        else "Aucune description", background=couleur_sous_fenetre, justify='left', anchor=W).pack(
            expand=YES, fill=BOTH, padx=5, pady=5)
        self.fill_table()
        self.images_widget = ImageManager(super_main_frame,
                                          images=ProductImage.get_by_product_id(product_id=self.product.id),
                                          borderwidth=1, background=couleur_sous_fenetre, width=230,
                                          label_anchor=NW, product_id=self.product.id, is_view_mode=True)
        self.images_widget.grid(row=3, column=1, sticky=EW)

    def fill_table(self):
        self.clear_table()
        list_value = [
            ["Code", self.product.code],
            ["Nom", self.product.name],
            ["Stock", self.product.stock],
            ["Prix unitaire actuel", self.supply.unit_price if self.supply is not None else "Aucun"],
            ["Catégorie", self.product.category.name if self.product.category is not None else "Non spécifiée"],
            ["Rayon", self.product.rayon.name if self.product.rayon is not None else "Non spécifié"],
            ["Gamme", self.product.gamme.name if self.product.gamme is not None else "Non spécifiée"],
            ["Grammage", self.product.grammage],
            ["Type de grammage", self.product.grammage_type.name if self.product.grammage_type is not None else ""],
            ["Marque", self.product.brand],
            ["Prix modifiable", "Oui" if self.product.is_price_reducible else "Non"],
            ["Prix maximum", self.product.max_salable_price if self.product.max_salable_price else "Aucun"],

        ]

        for i, value in enumerate(list_value):
            self.table.insert("", index=END, iid=str(i), tags=("even" if i % 2 else "odd",),
                              values=value, open=False)
        self.table.tag_configure("odd", background=couleur_label, foreground=couleur_invers_treeeview)
        self.table.tag_configure("even", background=couleur_inverse_tree, foreground=couleur_police_champs)

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)
