from datetime import date
from tkinter import *
from tkinter import ttk, messagebox
from customtkinter import CTkTabview

from DATA.SettingClass.Client import Client
from DATA.SettingClass.CreditSale import CreditSale
from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Refund import Refund
from DATA.SettingClass.Sale import Sale
from DATA.SettingClass.SaleProduct import SaleProduct
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supply import Supply
from STATIC.ConstantFile import couleur_sous_fenetre, image_fiche_client, image_vnt_credit
from Service.AnyService import AnyService
from Service.DateTimeService import DateTimeService
from Service.ImageService import ImageService
from UI.CreditSale.CreditSaleForm import CreditSaleForm
from UI.DailyInventory.DailyInventoryForm import DailyInventoryForm
from UI.Home.MiniDashboard import MiniDashboard
from UI.Home.Vente.OneSaleTap import OneSaleTap

from dateutil import parser

from UI.Users.Client.AddClientForm import AddClientForm
from UI.Users.Client.ChoiceClientForm import ChoiceClientForm


class VentePage(Frame):
    onglet_index = 0
    list_sale_page = []
    last_shown = None

    def __init__(self, master: ttk.Notebook):
        super().__init__(master=master)
        VentePage.onglet_index += 1
        self.master: ttk.Notebook = master
        VentePage.list_sale_page.append(self)
        self.is_shown = False
        self.is_credit = False
        self.is_client_input_fill = False
        self.variable_total_sum = StringVar(value="0")
        self.variable_total_sum_temoin = StringVar(value="0")
        self.variable_total_sum_temoin.trace_add("write", lambda x, y, z: self.on_total_price_change())

        self.master.add(self, text=f"Vente {VentePage.onglet_index}")
        self.master.select(self)
        self.frame_globale = Frame(self)
        self.frame_globale.pack(fill=BOTH, anchor=NW, expand=YES, side=LEFT)

        self.frame_params = Frame(self, background=couleur_sous_fenetre)
        self.frame_params.pack(fill=BOTH, anchor=NE, expand=YES, side=RIGHT)
        self.fiche_client = ImageService.resize_image(self.frame_globale, image_fiche_client, 50, 50)
        self.credit_sale = ImageService.resize_image(self.frame_globale, image_vnt_credit, 50, 50)

        self.client_button = Menubutton(self.frame_params, image=self.fiche_client, text="Fiche client", compound=TOP,
                                    width=80, height=80, relief=RAISED)
        self.client_button.pack(pady=(20, 20))
        my_popup = Menu(self.client_button, tearoff=0,
                                         title="Action sur les dépenses enregistrees")
        my_popup.add_command(label=f"Nouveau client",
                                              command=self.on_client_fiche_tap)
        my_popup.add_separator()
        my_popup.add_command(label=f"Choisir un client",
                                              command=self.on_choice_client_tap)
        self.client_button.configure(menu=my_popup)
        # self.client_button.
        ttk.Separator(self.frame_params, orient=HORIZONTAL).pack(fill=X)
        self.credit_sale_button = Button(self.frame_params, image=self.credit_sale, text="Vendre à crédit", compound=TOP,
               width=80, height=80, command=self.on_credit_sale_tap)
        self.credit_sale_button.pack(pady=(20, 20))
        ttk.Separator(self.frame_params, orient=HORIZONTAL).pack(fill=X)

        self.note_book_top = ttk.Notebook(self.frame_globale)
        self.note_book_top.pack(anchor=NW, side=TOP, expand=YES, fill=BOTH)

        self.my_list_sale_tab = [OneSaleTap(self.note_book_top, self.manage_child_tab, self.variable_total_sum_temoin)]

        self.frame_bottom = Frame(self.frame_globale, background=couleur_sous_fenetre)
        self.frame_bottom.pack(anchor=SW, fill=X, side=BOTTOM)

        self.button_close_tap = Button(self.frame_bottom, text="Quitter", command=lambda: self.quit_tab(),
                                       relief=GROOVE, width=15)
        self.button_close_tap.pack(side=LEFT)

        self.button_add_tap = Button(self.frame_bottom, text="Ajouter un onglet", command=lambda: self.add_tab()
                                     , relief=GROOVE, width=15)
        self.button_add_tap.pack(side=LEFT)

        self.frame_bottom_center = LabelFrame(self.frame_bottom, background=couleur_sous_fenetre, border=0)
        self.frame_bottom_center.pack(side=LEFT, fill=BOTH, padx=(120, 5,))
        #
        self.button_save_sale = Button(self.frame_bottom_center, text="Enregistrer", command=lambda: self.save_sale(0),
                                       relief=GROOVE, width=15)
        self.button_save_sale.pack(side=LEFT)
        #
        self.button_save_sale_and_print = Button(self.frame_bottom_center, text="Enregistrer et imprimer",
                                                 command=lambda: self.save_sale(0), relief=GROOVE, width=18)
        self.button_save_sale_and_print.pack(side=RIGHT)

        self.label_product_total_sum = Label(self.frame_bottom, textvariable=self.variable_total_sum, font="20",
                                                 background=couleur_sous_fenetre)
        self.label_product_total_sum.pack(side=RIGHT)
        self.label_product_total_sum_fix = Label(self.frame_bottom, text="Montant total: ", font="20",
                                                 background=couleur_sous_fenetre)
        self.label_product_total_sum_fix.pack(side=RIGHT)

        self.avance_var = StringVar()
        self.refund_date_var = StringVar()
        self.my_client = Client()
        self.bind("<Expose>", self.on_expose)
        self.bind("<Unmap>", self.on_hide)
        self.master.master.master.master.master.bind("<FocusOut>", self.on_focus_out)
        self.master.master.master.master.master.bind("<FocusIn>", self.on_focus_in)

    def on_focus_out(self, event):
        # print("On focus out")
        self.master.master.master.master.master.unbind("<KeyRelease-Return>")

    def on_focus_in(self, event):
        # print("On focus in")
        self.master.master.master.master.master.bind("<KeyRelease-Return>", self.save_sale)

    def on_expose(self, event):
        # print("On expose")
        self.is_shown = True
        self.master.master.master.master.master.bind("<KeyRelease-Return>", self.save_sale)

    def on_client_fiche_tap(self):
        self.client_button.configure(background="green", activebackground="green")
        client_fiche = AddClientForm(Toplevel(self.master), client=self.my_client)
        if client_fiche.is_client_input_fill:
            self.my_client = client_fiche.client
            self.is_client_input_fill = True
        else:
            self.client_button.configure(background="SystemButtonFace", activebackground="SystemButtonFace")
            self.is_client_input_fill = False

    def on_choice_client_tap(self):
        self.client_button.configure(background="green")
        client_fiche = ChoiceClientForm(self.master, client=self.my_client)
        if client_fiche.is_client_input_fill:
            self.my_client = client_fiche.client
            self.is_client_input_fill = True
        else:
            self.client_button.configure(background="SystemButtonFace")
            self.is_client_input_fill = False

    def on_credit_sale_tap(self):
        self.credit_sale_button.configure(background="green")
        credit_form = CreditSaleForm(self.master.winfo_toplevel(), avance_value=self.avance_var.get(),
                                     refund_value=self.refund_date_var.get())
        if credit_form.is_credit:
            self.avance_var.set(credit_form.avance)
            self.refund_date_var.set(credit_form.refund_date)
            self.is_credit = True
        else:
            self.credit_sale_button.configure(background="SystemButtonFace")
            self.is_credit = False
            self.avance_var.set("")
            self.refund_date_var.set("")

    def on_hide(self, event):
        self.is_shown = False
        VentePage.last_shown = self
        self.master.master.master.master.master.unbind("<KeyRelease-Return>")

    def get_shown_tab(self) -> OneSaleTap | None:
        shown = [one_tab for one_tab in self.my_list_sale_tab if one_tab.is_shown]
        return shown[0] if len(shown) > 0 else None

    @staticmethod
    def get_shown_page():
        shown: list[VentePage] = [sale_page for sale_page in VentePage.list_sale_page if sale_page.is_shown]
        return shown[0] if len(shown) > 0 else None

    def get_not_full_tab(self) -> list[OneSaleTap]:
        return [one_tab for one_tab in self.my_list_sale_tab if not one_tab.is_full]

    def has_this_product(self, product: Product) -> bool:
        for sale_tab in self.my_list_sale_tab:
            if sale_tab.has_this_product(product=product):
                return True
        return False

    def fill_tab_line_with_only_products(self, products: list[Product]):
        list_sale_product: list[SaleProduct] = []
        for product in products:
            current_supply: Supply = Supply().find_right_product_supply(product_id=product.id)
            if current_supply is None:
                current_supply = Supply(product=product, unit_coast=0)
            current_supply.product = product
            list_sale_product.append(SaleProduct(supply=current_supply,
                                                 product_count=1,
                                                 unit_price=current_supply.unit_price if current_supply.unit_price is not None else 0,
                                                 unit_coast=current_supply.unit_coast if current_supply.unit_coast is not None else 0))
        return self.fill_tab_line_with_sale_product(list_sale_product)

    def fill_tab_line_with_sale_product(self, list_sale_product: list[SaleProduct]):
        shown_tab: OneSaleTap | None = self.get_shown_tab()
        if shown_tab is not None:
            for sale_product in list_sale_product:
                if not shown_tab.fill_line_with_sale_product(sale_product=sale_product):
                    list_not_full:  list[OneSaleTap] = self.get_not_full_tab()
                    if len(list_not_full) > 0:
                        shown_tab = list_not_full[0]
                        shown_tab.fill_line_with_sale_product(sale_product=sale_product)
                    else:
                        shown_tab = shown_tab.add_tab()
                        shown_tab.fill_line_with_sale_product(sale_product=sale_product)

    def add_tab(self):
        return VentePage(self.master)

    def quit_tab(self):
        if len(self.master.tabs()) > 1:
            self.destroy()

    def on_total_price_change(self):
        total_price = sum(0 if not som.get_tap_total_price() else som.get_tap_total_price()
                                            for som in self.my_list_sale_tab)
        self.variable_total_sum.set(str(total_price))
        return total_price

    def manage_child_tab(self, tab: OneSaleTap, is_removing: bool = False):
        if is_removing:
            self.my_list_sale_tab.remove(tab)
        else:
            self.my_list_sale_tab.append(tab)
        return tab

    def check_date(self) -> date | bool:
        expected_date = DateTimeService.parse_date(self.refund_date_var.get())
        if expected_date is None:
            return True
        refund_date = parser.parse(expected_date).date()
        if date.today() >= refund_date:
            messagebox.showerror("Erreur",
                                 "La date de remboursement doit etre superieure à la date d'aujourd'hui !")
            return False
        return refund_date

    def save_sale(self, event):
        if AnyService.top_level_was_show:
            AnyService.top_level_was_show = False
            return
        if Staff.current_staff is None:
            messagebox.showerror("Erreur", "Veuillez choisir un vendeur")
            return
        expected_refund_date = True
        if self.is_credit:
            if not self.is_client_input_fill:
                messagebox.showerror("Error", "Pour une vente à crédit, vous devez remplir la fiche client")
                self.on_client_fiche_tap()
                return
            expected_refund_date = self.check_date()
            if not expected_refund_date:
                return
        list_sale_product: list[SaleProduct] = []
        for sale_products in list(sale_tap.get_list_sale_product() for sale_tap in self.my_list_sale_tab):
            list_sale_product += sale_products
        if len(list_sale_product) == 0:
            messagebox.showerror("Erreur", "Aucune donnée à enregistrer")
            return
        if None in list_sale_product:
            return
        client: Client = self.my_client
        client_id = None
        if self.is_client_input_fill:
            if client.id is None:
                client_id = client.save_to_db()
                client = Client.get_by_id(client_id=client_id)
        saved_sale_id = Sale(is_paid=True if not self.is_credit else False, client=client, total=self.on_total_price_change(),
                             staff=Staff.current_staff, is_credit=False, daily=Daily.get_current_daily()).save_to_db()
        sale: Sale = Sale(id=saved_sale_id, is_credit=self.is_credit, is_paid=True if not self.is_credit else False)

        list_sale_product_to_save: list[SaleProduct] = []
        list_supply_to_update = []
        for sale_product in list_sale_product:
            real_product_count: int = sale_product.product_count
            if real_product_count > sale_product.supply.product_count_rest:
                rest_product_count = real_product_count
                for supply in Supply().find_product_supply_with_stock(sale_product.supply.product.id):
                    new_sale_product = SaleProduct(unit_coast=supply.unit_coast,
                                                   unit_price=sale_product.unit_price,
                                                   supply=supply,
                                                   sale=sale)
                    if rest_product_count >= supply.cash_float:
                        rest_product_count -= supply.cash_float
                        new_sale_product.product_count = supply.cash_float
                        list_sale_product_to_save.append(new_sale_product)
                        list_supply_to_update.append((supply.cash_float, supply.id))
                    else:
                        new_sale_product.product_count = rest_product_count
                        list_sale_product_to_save.append(new_sale_product)
                        list_supply_to_update.append((rest_product_count, supply.id))
                        break
            else:
                sale_product.sale = sale
                list_sale_product_to_save.append(sale_product)
                list_supply_to_update.append((sale_product.supply.product_count_rest - real_product_count, sale_product.supply.id))

        supply_is_save = False
        sale_product_is_save = False
        first_refund_id = None
        credit_sale_id = None
        saved_sale_product_id: tuple[int] = tuple()
        supply_connection = None
        try:
            expected_avance = self.avance_var.get()
            if self.is_credit:
                if expected_avance:
                    first_refund_id = Refund(value=float(expected_avance), sale=sale).save_to_db()
                if self.refund_date_var.get():
                    credit_sale_id = CreditSale(refund_date=expected_refund_date, sale=sale).save_to_db()
            saved_sale_product_id = SaleProduct().save_many_to_db(list_sale_product_to_save)
            sale_product_is_save = True
            supply_connection = Supply().reduce_many_product_rest(list_supply_to_update)
            supply_connection.commit()
            supply_is_save = True
        except Exception as e:
            if first_refund_id is not None:
                Refund.delete_permanently(first_refund_id)
            if credit_sale_id is not None:
                CreditSale.delete_permanently(credit_sale_id)
            sale.delete_permanently()
            if client_id is not None:
                Client.delete_by_id_permanently(client_id)
            if supply_is_save:
                supply_connection.rollback()
            if sale_product_is_save:
                SaleProduct().delete_range_permanently(id_list=saved_sale_product_id)
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de "
                                           f"l'enregistrement de la vente")
            return

        messagebox.showinfo("DEL BLANCO", "Vente enregistrée avec succès")
        for tab in self.my_list_sale_tab:
            for sale_line in tab.my_list_line:
                sale_line.clear_entry()
        self.credit_sale_button.configure(background="SystemButtonFace")
        self.is_credit = False
        DailyInventoryForm.reload_all_form()
        MiniDashboard.reload_all_table()


class VentePage1(Frame):
    onglet_index = 0
    list_sale_page = []
    last_shown = None

    def __init__(self, master: ttk.Notebook):
        super().__init__(master=master)
        VentePage.onglet_index += 1
        self.master: ttk.Notebook = master
        VentePage.list_sale_page.append(self)
        # self.pack(anchor=NW, expand=YES, fill=Y)
        self.is_shown = False
        self.variable_total_sum = StringVar(value="0")
        self.variable_total_sum_temoin = StringVar(value="0")
        self.variable_total_sum_temoin.trace_add("write", lambda x, y, z: self.on_total_price_change())

        self.master.add(self, text=f"Vente {VentePage.onglet_index}")
        self.master.select(self)
        self.frame_globale = Frame(self)
        self.frame_globale.pack(fill=BOTH, anchor=NW, expand=YES)

        self.note_book_top = CTkTabview(self.frame_globale)
        self.note_book_top.pack(anchor=NW, side=TOP, expand=YES, fill=BOTH)

        self.my_list_sale_tab = [OneSaleTap(self.note_book_top, self.manage_child_tab, self.variable_total_sum_temoin)]

        self.frame_bottom = Frame(self.frame_globale, background=couleur_sous_fenetre)
        self.frame_bottom.pack(anchor=SW, fill=X, side=BOTTOM)

        self.button_close_tap = Button(self.frame_bottom, text="Quitter", command=lambda: self.quit_tab(),
                                       relief=GROOVE)
        self.button_close_tap.pack(side=LEFT)
        # self.button_close_tap.grid(sticky=W, row=1, column=2)

        self.button_add_tap = Button(self.frame_bottom, text="Ajouter un onglet", command=lambda: self.add_tab()
                                     , relief=GROOVE)
        self.button_add_tap.pack(side=LEFT)

        self.frame_bottom_center = LabelFrame(self.frame_bottom, background=couleur_sous_fenetre, border=0)
        self.frame_bottom_center.pack(side=LEFT, fill=BOTH, padx=(300, 5,))
        #
        self.button_save_sale = Button(self.frame_bottom_center, text="Enregistrer", command=lambda: self.save_sale(0),
                                       relief=GROOVE)
        self.button_save_sale.pack(side=LEFT)
        #
        self.button_save_sale_and_print = Button(self.frame_bottom_center, text="Enregistrer et imprimer",
                                                 command=lambda: self.save_sale(0), relief=GROOVE)
        self.button_save_sale_and_print.pack(side=RIGHT)

        self.label_product_total_sum = Label(self.frame_bottom, textvariable=self.variable_total_sum, font="20",
                                                 background=couleur_sous_fenetre)
        self.label_product_total_sum.pack(side=RIGHT)
        self.label_product_total_sum_fix = Label(self.frame_bottom, text="Montant total: ", font="20",
                                                 background=couleur_sous_fenetre)
        self.label_product_total_sum_fix.pack(side=RIGHT)
        # self.master.master.master.master.master.bind("<KeyRelease-Return>", self.save_sale)
        self.bind("<Expose>", self.on_expose)
        self.bind("<Unmap>", self.on_hide)

    def on_expose(self, event):
        self.is_shown = True
        self.master.master.master.master.master.bind("<KeyRelease-Return>", self.save_sale)

    def on_hide(self, event):
        self.is_shown = False
        VentePage.last_shown = self
        self.master.master.master.master.master.unbind("<KeyRelease-Return>")

    def get_shown_tab(self) -> OneSaleTap | None:
        shown = [one_tab for one_tab in self.my_list_sale_tab if one_tab.is_shown]
        return shown[0] if len(shown) > 0 else None

    @staticmethod
    def get_shown_page():
        shown: list[VentePage] = [sale_page for sale_page in VentePage.list_sale_page if sale_page.is_shown]
        return shown[0] if len(shown) > 0 else None

    def get_not_full_tab(self) -> list[OneSaleTap]:
        return [one_tab for one_tab in self.my_list_sale_tab if not one_tab.is_full]

    def has_this_product(self, product: Product) -> bool:
        for sale_tab in self.my_list_sale_tab:
            if sale_tab.has_this_product(product=product):
                return True
        return False

    def fill_tab_line_with_sale_product(self, list_sale_product: list[SaleProduct]):
        shown_tab: OneSaleTap | None = self.get_shown_tab()
        if shown_tab is not None:
            for sale_product in list_sale_product:
                if not shown_tab.fill_line_with_sale_product(sale_product=sale_product):
                    list_not_full:  list[OneSaleTap] = self.get_not_full_tab()
                    if len(list_not_full) > 0:
                        shown_tab = list_not_full[0]
                        shown_tab.fill_line_with_sale_product(sale_product=sale_product)
                    else:
                        shown_tab = shown_tab.add_tab()
                        shown_tab.fill_line_with_sale_product(sale_product=sale_product)

    def add_tab(self):
        return VentePage(self.master)

    def quit_tab(self):
        if len(self.master.tabs()) > 1:
            self.destroy()

    def on_total_price_change(self):
        total_price = sum(0 if not som.get_tap_total_price() else som.get_tap_total_price()
                                            for som in self.my_list_sale_tab)
        self.variable_total_sum.set(str(total_price))
        return total_price

    def manage_child_tab(self, tab: OneSaleTap, is_removing: bool = False):
        if is_removing:
            self.my_list_sale_tab.remove(tab)
        else:
            self.my_list_sale_tab.append(tab)
        return tab

    def save_sale(self, event):
        if Staff.current_staff is None:
            messagebox.showerror("Erreur", "Veuillez choisir un vendeur")
            return
        list_sale_product: list[SaleProduct] = []
        for sale_products in list(sale_tap.get_list_sale_product() for sale_tap in self.my_list_sale_tab):
            list_sale_product += sale_products
        if len(list_sale_product) == 0:
            messagebox.showerror("Erreur", "Aucune donnée à enregistrer")
            return
        if None in list_sale_product:
            return
        client: Client = Client()
        saved_sale_id = Sale(is_paid=True, client=client, total=self.on_total_price_change(),
                             staff=Staff.current_staff, is_credit=False).save_to_db()
        sale: Sale = Sale(id=saved_sale_id)
        list_sale_product_to_save: list[SaleProduct] = []
        list_supply_to_update = []
        for sale_product in list_sale_product:
            real_product_count: int = sale_product.product_count
            if real_product_count > sale_product.supply.product_count_rest:
                rest_product_count = real_product_count
                for supply in Supply().find_product_supply_with_stock(sale_product.supply.product.id):
                    new_sale_product = SaleProduct(unit_coast=supply.unit_coast,
                                                   unit_price=sale_product.unit_price,
                                                   supply=supply,
                                                   sale=sale)
                    if rest_product_count >= supply.cash_float:
                        rest_product_count -= supply.cash_float
                        new_sale_product.product_count = supply.cash_float
                        list_sale_product_to_save.append(new_sale_product)
                        list_supply_to_update.append((supply.cash_float, supply.id))
                    else:
                        new_sale_product.product_count = rest_product_count
                        list_sale_product_to_save.append(new_sale_product)
                        list_supply_to_update.append((rest_product_count, supply.id))
                        break
            else:
                sale_product.sale = sale
                list_sale_product_to_save.append(sale_product)
                list_supply_to_update.append((sale_product.supply.product_count_rest - real_product_count, sale_product.supply.id))

        supply_is_save = False
        sale_product_is_save = False
        saved_sale_product_id: tuple[int] = tuple()
        supply_connection = None
        try:
            saved_sale_product_id = SaleProduct().save_many_to_db(list_sale_product_to_save)
            sale_product_is_save = True
            supply_connection = Supply().reduce_many_product_rest(list_supply_to_update)
            supply_connection.commit()
            supply_is_save = True
        except Exception as e:
            print(e)
            sale.delete_permanently()
            if supply_is_save:
                supply_connection.rollback()
            if sale_product_is_save:
                SaleProduct().delete_range_permanently(id_list=saved_sale_product_id)
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de "
                                           f"l'enregistrement de la vente")
            return

        messagebox.showinfo("DEL BLANCO", "Vente enregistrée avec succès")
        for tab in self.my_list_sale_tab:
            for sale_line in tab.my_list_line:
                sale_line.clear_entry()

