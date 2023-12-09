from tkinter import ttk

from customtkinter import CTkToplevel

from STATIC.ConstantFile import *
from UI.Product.AddProductForm import AddProductForm
from UI.Product.AjoutProduitPage import PageAjoutProduit
from UI.AppMenu.AppMenu import AppMenu
from UI.BottomBar import BottomBar
from UI.Home.Home import Home


class App(Tk):
    main_window = None

    def __init__(self):
        super().__init__()
        App.main_window = self
        self.title("Del blanco")
        self.configure(bg="lightgray")
        # self.configure(bg="yellow")
        self.geometry(
            f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        # fenetre_principale.iconbitmap(logo)
        self.state("zoomed")
        self.my_app_menu = AppMenu(self)
        self.config(menu=self.my_app_menu)

        """********************** Note book qui contient tout le reste ******************"""
        self.note_book_principale = ttk.Notebook(self, style="mystyle.TNotebook")
        self.note_book_principale.pack(expand=True, fill=BOTH, side=TOP, )

        self.home_page = Home(self.note_book_principale)

        # self.add_product_page = PageAjoutProduit(self.note_book_principale)
        # self.note_book_principale.add(self.add_product_page, text="Ajouter produit", sticky=NSEW)

        self.bottom_bar = BottomBar(self)
        self.bottom_bar.pack()

    def add_product(self):
        tl = Toplevel(self)
        tl.transient(self)
        AddProductForm(master=tl).pack(pady=5, padx=5)



