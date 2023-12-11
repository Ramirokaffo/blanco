from datetime import datetime, date, timedelta
from tkinter import ttk

from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Sale import Sale
from STATIC.ConstantFile import *


class MiniDashboard(Frame):
    table_list = []

    def __init__(self, master):
        super().__init__(master=master)
        MiniDashboard.table_list.append(self)
        self.master = master
        self.table = ttk.Treeview(master, selectmode=EXTENDED, height=25,
                                  style="mystyle.Treeview",
                                  columns=("colonne1", "colonne2"), show="headings")
        """Entete de la table"""
        self.table.heading("colonne1", text="Indicateur", anchor="w")
        self.table.heading("colonne2", text="Mesure", anchor="e")

        """Dimensions de la table"""
        self.table.column("colonne1", width=245, minwidth=50, anchor="w")
        self.table.column("colonne2", width=100, minwidth=50, anchor="e")
        self.table.grid(row=1, column=1, columnspan=2, sticky=EW)
        self.load_table_data()

    def clear_table(self):
        for el in self.table.get_children():
            self.table.delete(el)

    @staticmethod
    def reload_all_table():
        if len(MiniDashboard.table_list) > 0:
            table: MiniDashboard
            for table in MiniDashboard.table_list:
                if table.winfo_exists():
                    table.load_table_data()

    def load_table_data(self):
        liste_info_opera_tree = []
        ca_today = Sale.get_ca_by_daily()
        liste_info_opera_tree += [["Recette actuelle", ca_today]]
        client_count = Sale.get_sale_count_by_daily()
        liste_info_opera_tree += [['Clients reçus', client_count]]
        try:
            sale_period = datetime.now() - Sale.get_first_sale_date_time()
            sale_period = str(sale_period).split(":")
            sale_period_by_hours = int(sale_period[0]) + round(
                int(sale_period[1]) / 60, 2)
            liste_info_opera_tree += [
                ["Frequence(Clients/heure)", f"{round(client_count / sale_period_by_hours, 2)}"]]
        except:
            liste_info_opera_tree += [["Frequence", f"Non disponible"]]
        sale_product_count = Sale.get_sale_product_count_by_daily()
        liste_info_opera_tree += [[f"{'Produit vendu' if sale_product_count == 1 else 'Produits vendus'}",
                                   sale_product_count]]
        liste_info_opera_tree += [["Vente annulée", Sale.get_sale_count_by_daily(deleted=True)]]
        current_daily = Daily.get_current_daily()
        ca_yesterday = Sale.get_ca_by_daily(daily_id=current_daily.id if current_daily else None)
        # ca_yesterday = Sale.get_ca_by_date(ca_date=date.today() - timedelta(days=1))
        liste_info_opera_tree += [["Recette d'hier", round(ca_yesterday if ca_yesterday else 0)]]
        try:
            taux_jour = f"{round(ca_today / ca_yesterday * 100, 2)}%"
        except:
            taux_jour = "RAS"
        liste_info_opera_tree += [["Taux(%)", taux_jour]]
        ca_relatif_yesterday = Sale.get_ca_by_daily(max_hours=datetime.now().hour,
                                                    daily_id=current_daily.id if current_daily else None)
        liste_info_opera_tree += [["Recette relative d'hier", ca_relatif_yesterday]]
        try:
            taux_relatif_jour = f"{round(ca_today / ca_relatif_yesterday * 100, 2)}%"
        except:
            taux_relatif_jour = "RAS"
        liste_info_opera_tree += [["Taux relatif(%)", taux_relatif_jour]]
        # else:
        #     liste_info_opera_tree += [["CAR-hier", "RAS"]]
        # try:
        #     taux_relatif_semaine = f"{round(somme_caj / ca_relatif_hier[0] * 100, 2)}%"
        # except:
        #     taux_relatif_semaine = "RAS"
        # liste_info_opera_tree += [["Taux relatif1", taux_relatif_semaine]]
        # if ca_semaine_dernier[0]:
        #     liste_info_opera_tree += [["CA semaine passée", round(ca_semaine_dernier[0])]]
        # else:
        #     liste_info_opera_tree += [["CA semaine passée", "RAS"]]
        # if ca_semaine[0]:
        #     liste_info_opera_tree += [["CA de la semaine", round(ca_semaine[0])]]
        # else:
        #     liste_info_opera_tree += [["CA de la semaine", "RAS"]]
        # try:
        #     taux_semaine = f"{round(ca_semaine[0] / ca_semaine_dernier[0] * 100, 2)}%"
        # except:
        #     taux_semaine = "RAS"
        # liste_info_opera_tree += [["Taux2", taux_semaine]]
        # if ca_relatif_semaine[0]:
        #     liste_info_opera_tree += [["CAR-semaine", round(ca_relatif_semaine[0])]]
        # else:
        #     liste_info_opera_tree += [["CAR-semaine", "RAS"]]
        # try:
        #     taux_relatif_semaine = f"{round(ca_semaine[0] / ca_relatif_semaine[0] * 100, 2)}%"
        # except:
        #     taux_relatif_semaine = "RAS"
        # liste_info_opera_tree += [["Taux relatif", taux_relatif_semaine]]
        # if ca_mois_dernier[0]:
        #     liste_info_opera_tree += [["CA du mois dernier", round(ca_mois_dernier[0])]]
        # else:
        #     liste_info_opera_tree += [["CA du mois dernier", "RAS"]]
        # if ca_mois[0]:
        #     liste_info_opera_tree += [["CA du mois", round(ca_mois[0])]]
        # else:
        #     liste_info_opera_tree += [["CA du mois", "RAS"]]
        # try:
        #     taux_mois = f"{round(ca_mois[0] / ca_mois_dernier[0] * 100, 2)}%"
        # except:
        #     taux_mois = "RAS"
        # liste_info_opera_tree += [["Taux3", taux_mois]]
        # if ca_relatif_mois[0]:
        #     liste_info_opera_tree += [["CAR-mois", round(ca_relatif_mois[0])]]
        # else:
        #     liste_info_opera_tree += [["CAR-mois", "RAS"]]
        # try:
        #     taux_relatif_mois = f"{round(ca_mois[0] / ca_relatif_mois[0] * 100, 2)}%"
        # except:
        #     taux_relatif_mois = "RAS"
        # liste_info_opera_tree += [["Taux relatif", taux_relatif_mois]]
        #
        # liste_info_opera_tree += [["Crédit non payé", nbr_ventec_impaye]]
        #
        # ma_base_donnee.close()
        # el = 0
        self.clear_table()
        tit = 0
        for ligne in reversed(liste_info_opera_tree):
            if tit % 2 == 0:
                self.table.insert("", index=0, id=f"{tit}", open=True,
                                  values=ligne, tags=("even",))
            else:
                self.table.insert("", index=0, id=f"{tit}", open=True,
                                  values=ligne, tags=("odd",))
            tit += 1
        self.table.tag_configure("odd", background=couleur_label,
                                 foreground=couleur_invers_treeeview)
        self.table.tag_configure("even", background=couleur_inverse_tree,
                                 foreground=couleur_fg_treeview)

