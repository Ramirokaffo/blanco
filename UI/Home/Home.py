from tkinter import ttk

from STATIC.ConstantFile import *
from Service.ImageService import ImageService
from UI.DailyExpense.DailyExpensePage import DailyExpensePage
from UI.DailyInventory.DailyInventoryPage import DailyInventoryPage
from UI.DailyRecipe.DailyRecipePage import DailyRecipePage
from UI.Home.HomeAction import HomeActions
from UI.Home.MiniDashboard import MiniDashboard
from UI.Home.MiniTableCredit import MiniTableCredit
from UI.Home.MiniTableDateCritic import MiniTableDateCritic
from UI.Home.MiniTableStockCritik import MiniTableStockCritic
from UI.Home.Vente.VentePage import VentePage
from UI.Product.ProductTable import ProductTable
from UI.SaleTable import SaleTable
from UI.ServerPage import ServerPage


class Home(Frame):
    def __init__(self, master: ttk.Notebook):
        super().__init__(master=master)
        self.master: ttk.Notebook = master
        # Onglet de la Page d'accueil de l'app
        self.sale_product_page_is_open = None
        self.list_sale_table_page_is_open = None
        self.list_product_table_page_is_open = None
        self.daily_expense_page_is_open = None
        self.daily_recipe_page_is_open = None
        self.daily_inventory_page_is_open = None
        self.server_page_is_open = None
        self.home_page = Frame(self.master)
        self.master.add(self.home_page, text="Accueil", sticky=NSEW)

        # PanedWindow qui contient les deux parties de la page d'accueil (gauche et droite)
        self.paned_mere_vente = PanedWindow(self.home_page, bg=couleur_sous_fenetre, orient=HORIZONTAL,
                                            proxybackground=couleur_bordure, bd=2, proxyborderwidth=10)
        self.paned_mere_vente.pack(expand=YES, fill=BOTH)

        # Notebook qui contient la partie gauche de page d'accueil
        self.note_book_west_vente = ttk.Notebook(self.paned_mere_vente, style="mystyle.TNotebook")
        self.paned_mere_vente.add(self.note_book_west_vente, width=420, minsize=380)
        self.igm_accueil = ImageService.resize_image(self.note_book_west_vente, image_accueil)

        # Onglet gauche de la partie gauche de la page d'accueil
        self.frame_vente_info_accueil = LabelFrame(self.note_book_west_vente, bg=couleur_sous_fenetre, text="",
                                                   fg=couleur_police, labelanchor="n", bd=bd_widget,
                                                   relief=relief_widget)
        self.note_book_west_vente.add(self.frame_vente_info_accueil
                                      , image=self.igm_accueil
                                      , text="Accueil")
        # Partie d'en haut de l'onglet de gauche qui contient les actions de la page d'accueil
        self.home_action = HomeActions(self.frame_vente_info_accueil)
        self.home_action.pack(side=TOP, )

        # Notebook qui contient les tableaux en bas
        self.note_book_credit_cmd = ttk.Notebook(self.frame_vente_info_accueil, style="mystyle.TNotebook")
        self.note_book_credit_cmd.pack(side=BOTTOM, fill=BOTH)

        self.img_stock_critic = ImageService.resize_image(self.note_book_west_vente, image_stock_critic)

        # Onglet des produits ayant un stock critique

        self.labelfrm_tree_stck_critic = LabelFrame(self.note_book_credit_cmd, bg=couleur_sous_fenetre,
                                                    labelanchor="n", fg=couleur_police, bd=bd_widget,
                                                    relief=relief_widget)
        self.note_book_credit_cmd.add(self.labelfrm_tree_stck_critic, text="Stock",
                                      image=self.img_stock_critic
                                      )
        self.miniTableStockCritic = MiniTableStockCritic(self.labelfrm_tree_stck_critic)
        self.miniTableStockCritic.pack()
        # img_date_critic = redimension_icone(image_date_critic, 20, 20)
        self.img_date_critic = ImageService.resize_image(self.note_book_west_vente, image_date_critic)

        # Onglet des produits ayant une date de peremption critique

        self.labelfrm_tree_date_critic = LabelFrame(self.note_book_credit_cmd, bg=couleur_sous_fenetre,
                                                    labelanchor="n", fg=couleur_police, bd=bd_widget,
                                                    relief=relief_widget)
        self.note_book_credit_cmd.add(self.labelfrm_tree_date_critic, text="Date",
                                      image=self.img_date_critic
                                      )

        self.miniTableDateCritic = MiniTableDateCritic(self.labelfrm_tree_date_critic)
        self.miniTableDateCritic.pack()

        self.img_vnt_credit = ImageService.resize_image(self.note_book_west_vente, image_vnt_credit)

        # Onglet des ventes effectuées à crédit
        self.frame_mini_credit_vnt = LabelFrame(self.note_book_credit_cmd, bg=couleur_sous_fenetre, text="",
                                                fg=couleur_police, labelanchor="n", bd=bd_widget, relief=relief_widget)
        self.note_book_credit_cmd.add(self.frame_mini_credit_vnt, text="Credit",
                                      image=self.img_vnt_credit
                                      )
        self.miniTableCredit = MiniTableCredit(self.frame_mini_credit_vnt)
        self.miniTableCredit.pack()

        # Onglet du tableau de bord opérationnel
        self.igm_stat_wv = ImageService.resize_image(self.note_book_west_vente, image_stat_west_vnt)

        self.frame_vente_table_opera = LabelFrame(self.note_book_west_vente, bg=couleur_sous_fenetre,
                                                  text="Tableau de bord quotidien",
                                                  fg=couleur_police, labelanchor="n", bd=bd_widget,
                                                  relief=relief_widget)
        self.note_book_west_vente.add(self.frame_vente_table_opera, text="Mini Dashboard",
                                      image=self.igm_stat_wv)

        self.miniDashboard = MiniDashboard(self.frame_vente_table_opera)
        self.miniDashboard.grid(sticky=NSEW)

        # Notebook qui contient la partie droite de page d'accueil
        self.note_book_center_vente = ttk.Notebook(self.paned_mere_vente, style="mystyle.TNotebook")
        self.paned_mere_vente.add(self.note_book_center_vente, minsize=350, width=850)

        self.home_action.treeview_accueil.bind("<<TreeviewSelect>>", self.on_treeviews_select)
        self.home_action.treeview_accueil.selection_set("5")

    def on_treeviews_select(self, event):
        indx_ligne_select = self.home_action.treeview_accueil.selection()
        valeur_ligne_select_opera = self.home_action.treeview_accueil.item(indx_ligne_select[0])["text"]
        if valeur_ligne_select_opera == "Vente des produits":
            self.show_sale_page()
        elif valeur_ligne_select_opera == "Liste des ventes":
            self.show_sale_list_page()
        elif valeur_ligne_select_opera == "Liste des produits":
            self.show_product_list_page()
        elif valeur_ligne_select_opera == "Dépenses quotidiennes":
            self.show_daily_expense_page()
        elif valeur_ligne_select_opera == "Recettes quotidiennes":
            self.show_daily_recipe_page()
        elif valeur_ligne_select_opera == "Gerer le serveur":
            self.show_server_manager_page()
        elif valeur_ligne_select_opera == "Comptes de fin de journée":
            self.show_daily_inventory_page()

    def show_sale_page(self):
        if self.sale_product_page_is_open is not None:
            try:
                self.note_book_center_vente.select(VentePage.last_shown)
                return
            except:
                pass
        self.sale_product_page_is_open = VentePage(self.note_book_center_vente)

    def show_sale_list_page(self):
        if self.list_sale_table_page_is_open is not None:
            try:
                self.note_book_center_vente.select(self.list_sale_table_page_is_open)
                return
            except:
                pass
        sale_table_frame = Frame(self.note_book_center_vente)
        self.note_book_center_vente.add(sale_table_frame, text="Liste des ventes")
        self.note_book_center_vente.select(SaleTable(sale_table_frame).displays())
        self.list_sale_table_page_is_open = sale_table_frame

    def show_product_list_page(self):
        if self.list_product_table_page_is_open is not None:
            try:
                self.note_book_center_vente.select(self.list_product_table_page_is_open)
                return
            except:
                pass
        product_table_frame = Frame(self.note_book_center_vente)
        self.note_book_center_vente.add(product_table_frame, text="Liste des produits")
        self.note_book_center_vente.select(ProductTable(product_table_frame).displays())
        self.list_product_table_page_is_open = product_table_frame

    def show_daily_expense_page(self):
        if self.daily_expense_page_is_open is not None:
            try:
                self.note_book_center_vente.select(self.daily_expense_page_is_open)
                return
            except:
                pass
        daily_expense_frame = Frame(self.note_book_center_vente)
        self.note_book_center_vente.add(daily_expense_frame, text="Dépenses quotidiennes")
        self.note_book_center_vente.select(DailyExpensePage(daily_expense_frame).pack())
        self.daily_expense_page_is_open = daily_expense_frame

    def show_daily_recipe_page(self):
        if self.daily_recipe_page_is_open is not None:
            try:
                self.note_book_center_vente.select(self.daily_recipe_page_is_open)
                return
            except:
                pass
        daily_recipe_frame = Frame(self.note_book_center_vente, background=couleur_sous_fenetre)
        self.note_book_center_vente.add(daily_recipe_frame, text="Recettes quotidiennes")
        self.note_book_center_vente.select(DailyRecipePage(daily_recipe_frame).pack())
        self.daily_recipe_page_is_open = daily_recipe_frame

    def show_daily_inventory_page(self):
        if self.daily_inventory_page_is_open is not None:
            try:
                self.note_book_center_vente.select(self.daily_inventory_page_is_open)
                return
            except:
                pass
        daily_inventory_frame = Frame(self.note_book_center_vente, background=couleur_sous_fenetre)
        self.note_book_center_vente.add(daily_inventory_frame, text="Comptes de fin de journée")
        DailyInventoryPage(daily_inventory_frame).pack()
        self.note_book_center_vente.select(daily_inventory_frame)
        self.daily_inventory_page_is_open = daily_inventory_frame

    def show_server_manager_page(self):
        if self.server_page_is_open is not None:
            try:
                self.note_book_center_vente.select(self.server_page_is_open)
                return
            except:
                pass
        server_page_frame = Frame(self.note_book_center_vente, bg=couleur_sous_fenetre)
        self.note_book_center_vente.add(server_page_frame, text="Gerer le serveur")
        self.note_book_center_vente.select(ServerPage(server_page_frame).displays())
        self.server_page_is_open = server_page_frame


