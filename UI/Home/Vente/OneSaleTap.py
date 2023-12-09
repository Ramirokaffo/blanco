from tkinter import *
from tkinter import ttk, messagebox

from customtkinter import CTkTabview

from DATA.SettingClass.Client import Client
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Sale import Sale
from DATA.SettingClass.SaleProduct import SaleProduct
from STATIC.ConstantFile import couleur_sous_fenetre
from UI.Home.Vente.OneSaleLine import OneSaleLine


class OneSaleTap(Frame):
    list_sale_tap = []
    onglet_index = 0

    def __init__(self, master: ttk.Notebook, manage_tab=None, variable_total_sum_temoin: StringVar = None):
        super().__init__(master=master)
        OneSaleTap.onglet_index += 1
        master.add(self, text=f"Tab {OneSaleTap.onglet_index}", sticky=NSEW)
        self.is_shown = True
        self.is_full = False
        self.master: ttk.Notebook = master
        self.my_list_line: [OneSaleLine] = []
        self.variable_total_sum_temoin: StringVar = variable_total_sum_temoin
        self.variable_total_sum_temoin.trace_add("write", lambda x, y, z: self.on_total_price_change(variable_total_sum_temoin))

        master.select(self)
        self.manage_tab = manage_tab
        OneSaleTap.list_sale_tap.append(self)
        self.global_sale_frame = Frame(self, bg=couleur_sous_fenetre)
        self.global_sale_frame.pack(expand=YES, fill=BOTH)

        self.sale_frame = Frame(self.global_sale_frame, background=couleur_sous_fenetre)
        self.sale_frame.pack(anchor=NW, expand=YES, side=TOP)

        self.add_sale_line_frame = Frame(self.sale_frame, background=couleur_sous_fenetre)
        self.add_sale_line_frame.pack(anchor=NW, side=BOTTOM, padx=5)

        self.button_close_tap = Button(self.add_sale_line_frame, text="-", command=lambda: self.remove_line(), width=3,
                                       relief=RIDGE)
        self.button_close_tap.grid(sticky=W, row=2, column=1)

        self.button_close_tap = Button(self.add_sale_line_frame, text="+", command=lambda: self.add_line(), width=3,
                                       relief=RIDGE)
        self.button_close_tap.grid(sticky=W, row=2, column=2)

        self.my_list_line.append(OneSaleLine(self.sale_frame, self.variable_total_sum_temoin))
        self.my_list_line.append(OneSaleLine(self.sale_frame, self.variable_total_sum_temoin))

        self.frame_bottom = Frame(self.global_sale_frame, background=couleur_sous_fenetre)
        self.frame_bottom.pack(anchor=SW, fill=X, side=BOTTOM)

        self.button_close_tap = Button(self.frame_bottom, text="Fermer", command=lambda: self.quit_tab(),
                                       relief=GROOVE, width=15)
        self.button_close_tap.pack(side=LEFT)

        self.button_add_tap = Button(self.frame_bottom, text="Ajouter un tab", command=lambda: self.add_tab(),
                                     relief=GROOVE, width=15)
        self.button_add_tap.pack(side=LEFT)
        self.bind("<Expose>", self.on_expose)
        self.bind("<Unmap>", self.on_hide)

    def on_expose(self, event):
        self.is_shown = True
        # self.master.master.master.master.master.bind("<KeyRelease-Return>", self.save_sale)

    def on_hide(self, event):
        self.is_shown = False
        # self.master.master.master.master.master.unbind("<KeyRelease-Return>")

    def quit_tab(self):
        if len(self.master.tabs()) > 1:
            self.manage_tab(tab=self, is_removing=True)
            self.destroy()
            if self.variable_total_sum_temoin.get() == "0":
                self.variable_total_sum_temoin.set("1")
            else:
                self.variable_total_sum_temoin.set("0")

            # self.manage_tab()

    def on_total_price_change(self, variable_total_sum_temoin: StringVar):
        if variable_total_sum_temoin.get() == "0":
            variable_total_sum_temoin.set("1")
        else:
            variable_total_sum_temoin.set("0")

    def add_tab(self):
       return self.manage_tab(tab=OneSaleTap(self.master, self.manage_tab, self.variable_total_sum_temoin), is_removing=False)

    def add_line(self) -> bool:
        if len(self.my_list_line) <= 10:
            self.my_list_line.append(OneSaleLine(self.sale_frame, self.variable_total_sum_temoin))
            return True
        else:
            return False

    def get_free_line(self) -> list[OneSaleLine]:
        return [line for line in self.my_list_line if not line.is_busy]

    def get_busy_line(self) -> list[OneSaleLine]:
        return [line for line in self.my_list_line if line.is_busy]

    def has_this_product(self, product: Product) -> bool:
        return True if product.name in [prod.current_product.name for prod in self.get_busy_line()] else False

    def fill_line_with_sale_product(self, sale_product: SaleProduct):
        list_free_line: list[OneSaleLine] = self.get_free_line()
        if len(list_free_line) > 0:
            list_free_line[0].fill_with_sale_product(sale_product=sale_product)
            return True
        else:
            if self.add_line():
                self.my_list_line[-1].fill_with_sale_product(sale_product=sale_product)
                return True
            else:
                self.is_full = True
                return False

    def remove_line(self):
        OneSaleLine.list_line.pop()
        self.my_list_line.pop().destroy()

    def get_tap_total_price(self) -> float | str:
        try:
            return sum(0 if not sous_total.get_line_total_price() else sous_total.get_line_total_price()
                       for sous_total in self.my_list_line)
        except:
            return ""

    def get_list_sale_product(self):
        return [sale_line.get_sale_product() for sale_line in self.my_list_line if sale_line.current_product]


class OneSaleTap1(Frame):
    list_sale_tap = []
    onglet_index = 0

    def __init__(self, master: CTkTabview, manage_tab=None, variable_total_sum_temoin: StringVar = None):
        super().__init__(master=master)
        OneSaleTap.onglet_index += 1
        main_frame = master.add(name=f"Tab {OneSaleTap.onglet_index}")
        self.is_shown = True
        self.is_full = False
        self.master: CTkTabview = master
        self.my_list_line: [OneSaleLine] = []
        self.variable_total_sum_temoin: StringVar = variable_total_sum_temoin
        self.variable_total_sum_temoin.trace_add("write", lambda x, y, z: self.on_total_price_change(variable_total_sum_temoin))
        # self.pack(expand=YES)
        master.set(f"Tab {OneSaleTap.onglet_index}")
        self.manage_tab = manage_tab
        OneSaleTap.list_sale_tap.append(self)
        self.global_sale_frame = Frame(main_frame, bg=couleur_sous_fenetre)
        self.global_sale_frame.pack(expand=YES, fill=BOTH)

        self.sale_frame = Frame(self.global_sale_frame, background=couleur_sous_fenetre)
        self.sale_frame.pack(anchor=NW, expand=YES, side=TOP)

        self.add_sale_line_frame = Frame(self.sale_frame, background=couleur_sous_fenetre)
        self.add_sale_line_frame.pack(anchor=NW, side=BOTTOM, padx=5)

        self.button_close_tap = Button(self.add_sale_line_frame, text="-", command=lambda: self.remove_line(), width=3,
                                       relief=RIDGE)
        self.button_close_tap.grid(sticky=W, row=2, column=1)

        self.button_close_tap = Button(self.add_sale_line_frame, text="+", command=lambda: self.add_line(), width=3,
                                       relief=RIDGE)
        self.button_close_tap.grid(sticky=W, row=2, column=2)

        self.my_list_line.append(OneSaleLine(self.sale_frame, self.variable_total_sum_temoin))
        self.my_list_line.append(OneSaleLine(self.sale_frame, self.variable_total_sum_temoin))

        self.frame_bottom = Frame(self.global_sale_frame, background=couleur_sous_fenetre)
        self.frame_bottom.pack(anchor=SW, fill=X, side=BOTTOM)

        self.button_close_tap = Button(self.frame_bottom, text="Fermer", command=lambda: self.quit_tab(), relief=GROOVE)
        self.button_close_tap.pack(side=LEFT)

        self.button_add_tap = Button(self.frame_bottom, text="Ajouter un tab", command=lambda: self.add_tab(), relief=GROOVE)
        self.button_add_tap.pack(side=LEFT)
        self.bind("<Expose>", self.on_expose)
        self.bind("<Unmap>", self.on_hide)

    def on_expose(self, event):
        self.is_shown = True
        # self.master.master.master.master.master.bind("<KeyRelease-Return>", self.save_sale)

    def on_hide(self, event):
        self.is_shown = False
        # self.master.master.master.master.master.unbind("<KeyRelease-Return>")

    def quit_tab(self):
        if len(self.master.children) > 1:
            self.manage_tab(tab=self, is_removing=True)
            self.destroy()
            if self.variable_total_sum_temoin.get() == "0":
                self.variable_total_sum_temoin.set("1")
            else:
                self.variable_total_sum_temoin.set("0")

            # self.manage_tab()

    def on_total_price_change(self, variable_total_sum_temoin: StringVar):
        if variable_total_sum_temoin.get() == "0":
            variable_total_sum_temoin.set("1")
        else:
            variable_total_sum_temoin.set("0")

    def add_tab(self):
       return self.manage_tab(tab=OneSaleTap(self.master, self.manage_tab, self.variable_total_sum_temoin), is_removing=False)

    def add_line(self) -> bool:
        if len(self.my_list_line) <= 10:
            self.my_list_line.append(OneSaleLine(self.sale_frame, self.variable_total_sum_temoin))
            return True
        else:
            return False

    def get_free_line(self) -> list[OneSaleLine]:
        return [line for line in self.my_list_line if not line.is_busy]

    def get_busy_line(self) -> list[OneSaleLine]:
        return [line for line in self.my_list_line if line.is_busy]

    def has_this_product(self, product: Product) -> bool:
        return True if product.name in [prod.current_product.name for prod in self.get_busy_line()] else False

    def fill_line_with_sale_product(self, sale_product: SaleProduct):
        list_free_line: list[OneSaleLine] = self.get_free_line()
        if len(list_free_line) > 0:
            list_free_line[0].fill_with_sale_product(sale_product=sale_product)
            return True
        else:
            if self.add_line():
                self.my_list_line[-1].fill_with_sale_product(sale_product=sale_product)
                return True
            else:
                self.is_full = True
                return False

    def remove_line(self):
        OneSaleLine.list_line.pop()
        self.my_list_line.pop().destroy()

    def get_tap_total_price(self) -> float | str:
        try:
            return sum(0 if not sous_total.get_line_total_price() else sous_total.get_line_total_price()
                       for sous_total in self.my_list_line)
        except:
            return ""

    def get_list_sale_product(self):
        return [sale_line.get_sale_product() for sale_line in self.my_list_line if sale_line.current_product]
