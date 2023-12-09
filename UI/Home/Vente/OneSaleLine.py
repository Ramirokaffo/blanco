from tkinter import *
from tkinter import ttk, messagebox

from DATA.SettingClass.Product import Product
from DATA.SettingClass.SaleProduct import SaleProduct
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import couleur_sous_fenetre, image_supp_cham, image_nettoyage

import asyncio

from Service.ImageService import ImageService
from UI.Product.ProductDetailsPage import ProductDetailsPage


class OneSaleLine(Frame):
    list_line: list = []

    def __init__(self, master, variable_total_sum_temoin: StringVar = None):
        super().__init__(master=master, bg=couleur_sous_fenetre)
        OneSaleLine.list_line.append(self)
        self.master = master
        self.pack(side=TOP)
        self.is_busy = False
        self.current_product: Product | None = None
        self.current_supply: Supply | None = None
        self.product_stock_variable = StringVar()
        self.line_total_price_variable = StringVar()
        self.line_total_price_variable.trace_add("write", lambda x, y, z: self.on_total_price_change(variable_total_sum_temoin))
        self.fonction_product_input_edit = self.register(self.on_product_input_edit)
        self.fonction_product_count_validator = self.register(self.product_count_validator)
        self.fonction_product_price_validator = self.register(self.product_price_validator)
        # self.check_digit = self.register(self.lettre_interdit)

        self.button_clear_entry = Button(self, text="Détails", relief=GROOVE, command=self.show_product_details)
        self.button_clear_entry.grid(row=1, column=3, pady=5, ipady=5, padx=5)
        self.clear_one_entry_icon = ImageService.resize_image(self, image_supp_cham)

        self.button_clear_entry = Button(self, text="Suppr.", command=self.clear_entry, relief=GROOVE,
                                         # image=self.clear_one_entry_icon, bg="red"
                                         )
        self.button_clear_entry.grid(row=1, column=4, pady=5, ipady=5, padx=5)

        self.product_name_entry = ttk.Combobox(self, postcommand=self.load_product, width=30, height=23,
                                               validate="all", validatecommand=(self.fonction_product_input_edit,
                                                                                "%P", "%d", "%S"), )
        self.product_name_entry.grid(row=1, column=5, pady=5, ipady=5, padx=5)

        self.product_count_entry = ttk.Combobox(self, values=[str(i + 1) for i in range(10)], validate="key",
                                                validatecommand=(self.fonction_product_count_validator, "%S"))
        self.product_count_entry.grid(row=1, column=6, pady=5, ipady=5, padx=5)
        self.product_count_entry.set("1")

        self.product_price_entry = ttk.Combobox(self, validate="key",
                                                validatecommand=(self.fonction_product_price_validator, "%S"))
        self.product_price_entry.grid(row=1, column=7, pady=5, ipady=5, padx=5)

        self.product_semi_total = Label(self, width=10, bg="white", textvariable=self.line_total_price_variable)
        self.product_semi_total.grid(row=1, column=9, pady=5, ipady=5, padx=5)

        self.product_stock = Label(self, width=10, bg="white", textvariable=self.product_stock_variable)
        self.product_stock.grid(row=1, column=8, pady=5, ipady=5, padx=5)

        self.product_count_entry.bind("<<ComboboxSelected>>", lambda x: self.eval_sale_line())
        self.product_price_entry.bind("<<ComboboxSelected>>", lambda x: self.eval_sale_line())

    def show_product_details(self):
        if self.current_product is not None:
            tl = Toplevel(self.master, bg=couleur_sous_fenetre)
            # tl.geometry("600x280+100+100")
            tl.transient(self.master.winfo_toplevel())
            ProductDetailsPage(master=tl, product_id=self.current_product.id).pack(pady=25, padx=25)

    def on_product_input_edit(self, value, action_type, quoi):
        # if action_type in ["0", "1"]:
        self.on_product_entry_change(0)
        return True

    def on_total_price_change(self, variable_total_sum_temoin: StringVar):
        if variable_total_sum_temoin.get() == "0":
            variable_total_sum_temoin.set("1")
        else:
            variable_total_sum_temoin.set("0")

    def load_product(self):
        list_product = Product().find_sale_product(self.product_name_entry.get())
        self.product_name_entry.config(values=list_product)

    def clear_entry(self):
        self.product_name_entry.delete(0, END)
        self.clear_other_entry()

    def clear_other_entry(self):
        self.product_price_entry.delete(0, END)
        self.product_stock_variable.set("")
        self.line_total_price_variable.set("")
        self.product_count_entry.set("1")
        self.current_product = None
        self.is_busy = False
        self.configure(background=couleur_sous_fenetre)
        self.product_stock.configure(foreground="black")

    def lettre_interdit(self, quoi):
        try:
            int(quoi)
            return True
        except:
            if quoi == ".":
                return True
            else:
                self.bell()
                return False

    def fill_with_sale_product(self, sale_product: SaleProduct):
        self.product_name_entry.set(sale_product.supply.product.name if
                                    sale_product.supply and sale_product.supply is not None else "")
        self.product_count_entry.set(sale_product.product_count)
        self.product_price_entry.set(f"{sale_product.unit_price:.0f}")
        self.on_product_entry_change(0)

    def product_count_validator(self, quoi):
        self.after(5, self.eval_sale_line)
        return self.lettre_interdit(quoi)

    def eval_sale_line(self):
        total_price = self.get_line_total_price()
        if total_price:
            self.line_total_price_variable.set(f"{total_price:.0f}")
        else:
            self.line_total_price_variable.set("")

    def product_price_validator(self, quoi):
        self.after(5, self.eval_sale_line)
        return self.lettre_interdit(quoi)

    def on_product_entry_change(self, event):
        product: Product = Product().find_product_by_name(self.product_name_entry.get())
        if product:
            self.is_busy = True
            self.current_supply: Supply = Supply().find_right_product_supply(product_id=product.id)
            self.current_product = product
            if self.current_supply:
                self.current_supply.product = product
                self.product_stock_variable.set(str(product.get_stock()))
                if not self.product_price_entry.get():
                    self.product_price_entry.set(f'{self.current_supply.unit_price:.0f}')
                self.product_stock.configure(foreground="green")
                self.eval_sale_line()
                self.product_price_entry.config(values=SaleProduct().get_last_product_sale_price(product_id=product.id))
            else:
                self.configure(background="red")
        else:
            self.clear_other_entry()
            self.is_busy = False

    def get_sale_product(self):
        product_count = self.product_count_entry.get()
        product_price = self.product_price_entry.get()
        product_stock = self.product_stock_variable.get()

        if not product_stock:
            messagebox.showerror("Stock épuisé", f'Vous avez épuisé le stock du produit '
                                                      f'{self.current_product.name}; Rassurez-vous d\'avoir enregistré '
                                                      f'le dernier approvisionnement')
            return None
        real_product_count: int = int(product_count)
        print("product_stock", product_stock)
        print("real_product_count", real_product_count)
        if int(product_stock) < real_product_count:
            messagebox.showerror("Stock insuffisant", f'Le stock du produit {self.current_product.name} ne peut '
                                                      f'pas satisfaire la demande actuelle; Rassurez-vous d\'avoir '
                                                      f'enregistré le dernier approvisionnent')
            return None
        if not product_count:
            messagebox.showerror("Erreur", f'Veuillez entrer la quantité du produit {self.current_product.name}')
            return None
        if not product_price:
            messagebox.showerror("Prix de vente non défini", f'Veuillez entrer le prix de vente du produit '
                                                             f'{self.current_product.name}')
            return None

        return SaleProduct(product_count=real_product_count,
                           unit_price=float(product_price),
                           supply=self.current_supply, unit_coast=self.current_supply.unit_coast)

    def get_line_total_price(self):
        try:
            return float(self.product_price_entry.get()) * float(self.product_count_entry.get())
        except:
            return ""
