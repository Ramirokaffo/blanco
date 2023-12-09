from tkinter import ttk

from DATA.SettingClass.Staff import Staff
from STATIC.ConstantFile import *
from Service.AuthentificationService import AuthentificationPage
from Service.CalculatorService import PrincipalCalculator, StandardCalculator
from Service.ImageService import ImageService
# from UI.BoiteProduit.BoiteProduit import ProductBox
# from UI.BoiteProduit.showProductBox import show_product_box
from UI.Product.BoiteProduit import ProductBox
from UI.Home.Vente.VentePage import VentePage


class BottomBar(Frame):
    # current_staff: Staff = None

    def __init__(self, master: Misc):
        super().__init__(master=master)
        self.configure()
        largeur_bout = 25
        ipady_bout = 5
        self.nom_vendeur_achat_champs = StringVar()
        self.master: Misc = master
        # self.master.configure(bg="brown")

        self.frame_outils_bas_vente_mere = LabelFrame(self.master, background="white")
        self.frame_outils_bas_vente_mere.pack(side=BOTTOM, fill=X)

        self.frame_outils_bas_vente = LabelFrame(self.frame_outils_bas_vente_mere, text="", relief=relief_widget,
                                                 bd=bd_widget)
        self.frame_outils_bas_vente.pack(side=LEFT, anchor=W, fill=X)
        self.taille_icone_vente = 25
        self.icone_calco = ImageService.resize_image(self.frame_outils_bas_vente, image_calculatrice, self.taille_icone_vente, self.taille_icone_vente)
        self.boutton_calculatrice = Button(self.frame_outils_bas_vente, text="Calculatrice",
                                           command=self.show_calco
                                           , width=largeur_bout,
                                           image=self.icone_calco
                                           # , foreground="white"
                                           # , bg=ColorService.primary
                                           , bd=bd_widget, relief=relief_widget)
        self.boutton_calculatrice.grid(row=0, column=0, ipadx=ipady_bout)

        self.separator1 = ttk.Separator(self.frame_outils_bas_vente, orient=VERTICAL)
        self.separator1.grid(row=0, column=1, sticky=NS)

        self.list_product_icon = ImageService.resize_image(self.frame_outils_bas_vente, image_liste_prod, self.taille_icone_vente, self.taille_icone_vente)
        self.bout_list_prodc_client = Button(self.frame_outils_bas_vente,
                                             bd=bd_widget,
                                             # foreground="white",
                                             text="Liste",
                                             font="10",
                                             image=self.list_product_icon,
                                             relief=relief_widget,
                                             # bg=ColorService.primary,
                                             command=self.show_product_list,
                                             width=largeur_bout)
        self.bout_list_prodc_client.grid(row=0, column=6, ipadx=ipady_bout)

        self.separator2 = ttk.Separator(self.frame_outils_bas_vente, orient=VERTICAL)
        self.separator2.grid(row=0, column=7, sticky=NS)

        # control_affiche_texte_info_bvt.set("Vente effectuee avec succes")
        # control_progression = IntVar()

        self.frame_info_vente = Frame(self.frame_outils_bas_vente, bg="white")

        self.label_info_vente_icon = Label(self.frame_info_vente, bg="white", fg=fg_nuance)

        self.label_info_vente = Label(self.frame_info_vente, bg="white", fg=fg_nuance,
                                      # textvariable=control_affiche_texte_info_bvt
                                      )
        self.label_info_vente_icon.grid(row=1, column=1, ipadx=ipady_bout, sticky=E)
        self.label_info_vente.grid(row=1, column=2, ipadx=ipady_bout, sticky=E)

        self.frame_bas_vente_vendeur = Frame(self.frame_outils_bas_vente_mere, bg=couleur_sous_fenetre)
        self.frame_bas_vente_vendeur.pack(side=RIGHT)
        self.nom_vendeur = Label(self.frame_bas_vente_vendeur, textvariable=self.nom_vendeur_achat_champs,
                                 bg=couleur_sous_fenetre)
        self.nom_vendeur_achat_champs.set("Aucun")
        self.nom_vendeur.pack(side=RIGHT)
        self.staff_icon = ImageService.resize_image(self.frame_outils_bas_vente, image_admin)
        self.nom_vendeur_achat = Label(self.frame_bas_vente_vendeur, text="Vendeur: ",
                                       # width=50,
                                       anchor="w",
                                       image=self.staff_icon,
                                       justify="left", font=(police, taille_police_texte), bg=couleur_sous_fenetre)
        self.nom_vendeur_achat.pack(side=RIGHT)

        self.separator1 = ttk.Separator(self.frame_bas_vente_vendeur, orient=VERTICAL)
        self.separator1.pack(side=RIGHT, fill=Y)

        self.boutton_calculatrice.bind("<ButtonRelease-3>", self.popup_choix_calculator)
        self.nom_vendeur.bind("<ButtonRelease-1>", self.show_popup_select_staff)

    def show_product_list(self):
        ProductBox(self.master)

    def show_popup_select_staff(self, event):
        staff_popup_menu = Menu(self.nom_vendeur, tearoff=0,
                                         title="Choix du vendeur")
        for staff in Staff().get_all():
            staff_popup_menu.add_command(label=staff.get_all_name(),
                                                  command=lambda x=staff.id: self.on_vendeur_select(x))
        staff_popup_menu.add_command(label="Aucun",
                                              command=lambda: self.on_vendeur_select(-1))
        x, y = self.master.winfo_pointerxy()
        staff_popup_menu.tk_popup(x, y)

    def on_vendeur_select(self, staff_id: int):
        shown_page: VentePage = VentePage.get_shown_page()
        if shown_page is not None:
            shown_page.on_hide(0)
        staff = Staff().get_by_id(line_id=staff_id)
        if staff_id == -1:
            self.nom_vendeur_achat_champs.set("Aucun")
            Staff.current_staff = None
            return
        authentification_page = AuthentificationPage(self.frame_outils_bas_vente_mere, staff=staff)
        self.master.wait_window(authentification_page.fenetre_auth)
        if authentification_page.status:
            Staff.current_staff = staff
            self.nom_vendeur_achat_champs.set(staff.get_all_name())
        if shown_page is not None:
            shown_page.on_expose(0)

    def show_calco(self):
        principal_calculator = PrincipalCalculator(self.master)
        principal_calculator.affiche_calculator2()

    def show_basic_calco(self):
        principal_calculator = StandardCalculator(self.master, self)
        principal_calculator.affiche_calculatrice()

    def popup_choix_calculator(self, event):
        menu_popup_info_vente = Menu(self.master, tearoff=0, title="Choix de la Calculatrice", relief=FLAT)
        menu_popup_info_vente.add_command(label="Basic", command=self.show_basic_calco)
        menu_popup_info_vente.add_command(label="Standard", command=self.show_calco)
        menu_popup_info_vente.tk_popup(event.x, event.y + 700)
