from tkinter import Menu, Toplevel
from tkinter.constants import ACTIVE

from customtkinter import CTkToplevel

from STATIC.ConstantFile import couleur_sous_fenetre
from UI.Product.AddProductForm import AddProductForm
from UI.Category.AddCategoryForm import AddCategoryForm
from UI.ExpenseType.AddExpenseTypeForm import AddExpenseTypeForm
from UI.Gamme.AddGammeForm import AddGammeForm
from UI.GrammageType.AddGrammageTypeForm import AddGrammageTypeForm
from UI.RecipeType.RecipeTypeForm import AddRecipeTypeForm
from UI.Users.Staff.AddStaffForm import AddStaffForm
from UI.SupplyPage.AddSupplyForm import AddSupplyForm


class AppMenu(Menu):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        menu_ca = Menu(self, tearoff=0,)
        menu_ca.add_command(label="Mensuel",)
        menu_ca.add_command(label="Hebdomadaire")
        menu_ca.add_command(label="Journalier")
        menu_ca.add_command(label="Annuel")

        menu_export_file = Menu(self, tearoff=0)
        menu_export_file.add_command(label="Liste des produis")
        menu_export_file.add_command(label="Liste des approvisionnements")
        menu_export_file.add_command(label="Liste des ventes")
        menu_export_file.add_cascade(label="Chiffres d'affaires", menu=menu_ca)

        menu_fichier = Menu(self, tearoff=0)
        menu_fichier.add_cascade(label="Exporter les données vers EXCEL", menu=menu_export_file)
        menu_fichier.add_command(label="Importer les données dépuis EXCEL")
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Aide")
        menu_fichier.add_command(label="Quitter", underline=0)

        self.add_cascade(menu=menu_fichier, label="Fichier")

        menu_article = Menu(self, tearoff=0)
        menu_article.add_command(label="Approvisionnement", command=self.add_supply)
        menu_article.add_command(label="Utilisateurs", command=self.add_user)
        menu_article.add_command(label="Produits", command=self.add_product)
        menu_article.add_command(label="Categories de produit", command=self.add_category)
        menu_article.add_command(label="Rayons de produit", command=self.add_rayon)
        menu_article.add_command(label="Gammes de produit", command=self.add_gamme)
        menu_article.add_command(label="Types de grammage", command=self.add_grammage_type)
        menu_article.add_command(label="Fournisseurs")
        menu_article.add_command(label="Types de depense", command=self.add_expense_type)
        menu_article.add_command(label="Types de recette", command=self.add_recipe_type)

        menu_employee = Menu(self, tearoff=0)
        menu_employee.add_command(label="Ajouter")

        menu_epuisement_stock = Menu(self, tearoff=0)
        menu_epuisement_stock.add_radiobutton(label="FIFO", value="oui")
        menu_epuisement_stock.add_radiobutton(label="Non définie (par defaut)", value="non", state=ACTIVE)
        menu_epuisement_stock.add_separator()
        menu_epuisement_stock.add_command(label="Aide")

        menu_reglage = Menu(self, tearoff=0)

        menu_reglage.add_cascade(label="Méthode d'epuisement des stocks",
                                 menu=menu_epuisement_stock)
        menu_reglage.add_command(label="Facturation")

        self.add_cascade(menu=menu_article, label="Parametrage")
        self.add_cascade(menu=menu_employee, label="Gerer les vendeurs")
        self.add_cascade(menu=menu_reglage, label="Réglages")
        # self.add_user()

    def add_supply(self):
        tl = CTkToplevel(self.master)
        tl.transient(self.master.winfo_toplevel())
        AddSupplyForm(tl).pack()

    def add_product(self):
        tl = Toplevel(self.master)
        tl.transient(self.master.winfo_toplevel())
        AddProductForm(master=tl).pack(pady=5, padx=5)

    def add_category(self):
        tl = Toplevel(self.master, bg=couleur_sous_fenetre)
        tl.geometry("600x280+100+100")
        tl.transient(self.master.winfo_toplevel())
        AddCategoryForm(master=tl).pack(pady=5, padx=5)

    def add_user(self):
        tl = Toplevel(self.master, bg=couleur_sous_fenetre)
        tl.geometry("450x380+100+100")
        tl.transient(self.master.winfo_toplevel())
        AddStaffForm(master=tl).pack(pady=5, padx=5)

    def add_rayon(self):
        tl = Toplevel(self.master, bg=couleur_sous_fenetre)
        tl.geometry("600x280+100+100")
        tl.transient(self.master.winfo_toplevel())
        AddCategoryForm(master=tl).pack(pady=5, padx=5)

    def add_gamme(self):
        tl = Toplevel(self.master, bg=couleur_sous_fenetre)
        tl.geometry("600x280+100+100")
        tl.transient(self.master.winfo_toplevel())
        AddGammeForm(master=tl).pack(pady=5, padx=5)

    def add_grammage_type(self):
        tl = Toplevel(self.master, bg=couleur_sous_fenetre)
        tl.geometry("600x280+100+100")
        tl.transient(self.master.winfo_toplevel())
        AddGrammageTypeForm(master=tl).pack(pady=5, padx=5)

    def add_expense_type(self):
        tl = Toplevel(self.master, bg=couleur_sous_fenetre)
        tl.geometry("600x280+100+100")
        tl.transient(self.master.winfo_toplevel())
        AddExpenseTypeForm(master=tl).pack(pady=5, padx=5)

    def add_recipe_type(self):
        tl = Toplevel(self.master, bg=couleur_sous_fenetre)
        tl.geometry("600x280+100+100")
        tl.transient(self.master.winfo_toplevel())
        AddRecipeTypeForm(master=tl).pack(pady=5, padx=5)


