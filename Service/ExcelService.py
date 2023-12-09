from tkinter import filedialog
from tkinter import messagebox
# from MysqlService import connexion_bd_mysql
# from Ets_Info_File import *
import os
import pandas as pd
from datetime import date
from PIL import Image, ImageTk
import openpyxl
from openpyxl import Workbook

from DATA.SettingClass.Category import Category
from DATA.SettingClass.Gamme import Gamme
from DATA.SettingClass.GrammageType import GrammageType
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Rayon import Rayon
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supplier import Supplier
from DATA.SettingClass.Supply import Supply


class ExportData:

    @staticmethod
    def import_product(path: str):
        dframe = pd.DataFrame()
        valeurs = []
        # for fichier in liste_fich:
        wb: Workbook = openpyxl.load_workbook(path)
        feuille = wb["Table 1"]
        valeur: tuple[tuple[openpyxl.cell.Cell]] = feuille["O5:R1462"]
        for i, f in enumerate(valeur):
            print(i)
            product: Product = Product(name=f[0].value, category=Category(), gamme=Gamme(), rayon=Rayon(),
                                       grammage_type=GrammageType(), code=str(i))

            try:
                product.save_to_db()
                product.my_db.commit()
                product = product.find_product_by_name(name=f[0].value)
                supply = Supply(product=product, product_count=f[1].value, product_count_rest=f[1].value,
                                unit_price=f[2].value, unit_coast=f[2].value, saver_staff=Staff(), supplier=Supplier())
                supply.save_to_db()
                supply.my_db.commit()
            except:
                pass
            print(i)
            # break
            # print(f[0].value, f[1].value, f[2].value, f[3].value, )
        #     print(f, f[0].value)
        # print(valeur, type(valeur))
        # valeurs.append(valeur)
        # df = pd.read_excel(fichier, )

        # print(df)
        # dframe = dframe.append(df, ignore_index=True)
        # print(ds)
        # print(valeurs)
        # dframe.to_excel("fichier_combine.xlsx")

    # def export_prod(self):
    #     directory = filedialog.asksaveasfile(title="Veuillez selectionner l'emplacement du fichier Excel",
    #                                          initialdir="/", initialfile="Liste des produits", defaultextension=".xlsx",
    #                                          filetypes=(("xlsx filles", "*.xlsx"),))
    #     ma_base_donnee = connexion_bd_mysql()
    #     ds = pd.read_sql_query("SELECT * FROM produit", ma_base_donnee)
    #     noom = directory.name
    #     ds.to_excel(directory.name)
    #     directory.close()
    #     ma_base_donnee.close()
    #     ques = messagebox.askyesno(nom_ets, "Vos données ont été importées avec succès\n"
    #                                         "Voulez-vous ouvrir le fichier maintenant?")
    #     if ques:
    #         os.startfile(noom)
    #
    # def export_approv(self):
    #     directory = filedialog.asksaveasfile(title="Veuillez selectionner l'emplacement du fichier Excel",
    #                                          initialdir="/", initialfile="Liste des approvisionnements",
    #                                          defaultextension=".xlsx",
    #                                          filetypes=(("xlsx filles", "*.xlsx"),))
    #     ma_base_donnee = connexion_bd_mysql()
    #     ds = pd.read_sql_query("SELECT * FROM approvisionnement", ma_base_donnee)
    #     noom = directory.name
    #     ds.to_excel(directory.name)
    #     directory.close()
    #     ma_base_donnee.close()
    #     ques = messagebox.askyesno(nom_ets, "Vos données ont été importées avec succès\n"
    #                                         "Voulez-vous ouvrir le fichier maintenant?")
    #     if ques:
    #         os.startfile(noom)
    #
    # def export_liste_vente(self):
    #     annee = date.today().year
    #     ma_base_donnee = connexion_bd_mysql()
    #     """Selectionner les quantités de produit"""
    #     me_connect = ma_base_donnee.cursor()
    #
    #     me_connect.execute(
    #         f"SELECT quantite_achete1, quantite_achete2, quantite_achete3, quantite_achete4, quantite_achete5, "
    #         f"quantite_achete6, quantite_achete7, quantite_achete8, quantite_achete9, quantite_achete10, id_relatif"
    #         f" FROM vente WHERE YEAR(date_heure_vente) = '{annee}' ORDER by date_heure_vente ASC")
    #
    #     liste_liste = []
    #     lignen = []
    #     t = 0
    #     ir = 0
    #     for ligne in me_connect:
    #         ligne = list(ligne)
    #         while None in ligne:
    #             ligne.remove(None)
    #         while 0 in ligne:
    #             ligne.remove(0)
    #         if t == 0:
    #             ir = ligne[-1]
    #         if ligne[-1] == ir:
    #             t += 1
    #             lignen += ligne[0:-1]
    #             continue
    #         else:
    #             liste_liste += [lignen]
    #             lignen = ligne[0:-1]
    #             ir = ligne[-1]
    #     liste_liste += [lignen]
    #
    #     me_connect.execute(
    #         f"SELECT prix_unitaire1, prix_unitaire2, prix_unitaire3, prix_unitaire4, prix_unitaire5, "
    #         f"prix_unitaire6, prix_unitaire7, prix_unitaire8, prix_unitaire9, prix_unitaire10, id_relatif"
    #         f" FROM vente WHERE YEAR(date_heure_vente) = '{annee}' "
    #         f"ORDER by date_heure_vente ASC;")
    #
    #     lignen = []
    #     t = 0
    #     ir = 0
    #     liste_liste_prix = []
    #     for ligne_prix in me_connect:
    #         ligne_prix = list(ligne_prix)
    #         while None in ligne_prix:
    #             ligne_prix.remove(None)
    #         while 0 in ligne_prix:
    #             ligne_prix.remove(0)
    #         if t == 0:
    #             ir = ligne_prix[-1]
    #         if ligne_prix[-1] == ir:
    #             t += 1
    #             lignen += ligne_prix[0:-1]
    #             continue
    #         else:
    #             liste_liste_prix += [lignen]
    #             lignen = ligne_prix[0:-1]
    #             ir = ligne_prix[-1]
    #     liste_liste_prix += [lignen]
    #
    #     me_connect.execute(
    #         f"select id_relatif, nom_client, nom_vendeur, date_heure_vente, produit_achete1, produit_achete2,"
    #         f" produit_achete3, produit_achete4, produit_achete5, produit_achete6, produit_achete7,"
    #         f" produit_achete8, produit_achete9, produit_achete10,"
    #         f" somme_totale_payee, id_relatif from vente WHERE "
    #         f"YEAR(date_heure_vente) = '{annee}' ORDER by date_heure_vente ASC;")
    #
    #     liste_liste_produit = []
    #     lignen = []
    #     ligne_autre = []
    #     t = 0
    #     ir = 0
    #     autr = []
    #     sommetot = 0.0
    #     for ligne in me_connect:
    #         ligne = list(ligne)
    #         ligne = [r for r in ligne if (r != "" and r != "vide" and r is not None)]
    #         if t == 0:
    #             ir = ligne[-1]
    #         if ligne[-1] == ir:
    #             t += 1
    #             lignen += ligne[4:-2]
    #             sommetot += int(ligne[-2])
    #             autr = ligne[:4]
    #             continue
    #         else:
    #             autr.append(sommetot)
    #             ligne_autre += [autr]
    #             liste_liste_produit += [lignen]
    #             lignen = ligne[4:-2]
    #             ir = ligne[-1]
    #             autr = ligne[:4]
    #             sommetot = int(ligne[-2])
    #     autr.append(sommetot)
    #     ligne_autre += [autr]
    #     liste_liste_produit += [lignen]
    #
    #     list_list_prod = []
    #
    #     n = 0
    #     it = 0
    #     montant_totale = 0.0
    #     control_change_jour = ""
    #     for rown in liste_liste_produit:
    #         i = 0
    #         liste_pqp = []
    #         for pr in rown:
    #             liste_pqp.append(pr)
    #             liste_pqp.append(liste_liste[n][i])
    #             liste_pqp.append(liste_liste_prix[n][i])
    #             i += 1
    #         try:
    #             datee = ligne_autre[n][3]
    #         except:
    #             return
    #
    #         ligne_autren = ligne_autre[n].copy()
    #         ligne_autren[3] = datee
    #         ligne_total = ligne_autren + liste_pqp
    #
    #         list_list_prod.append(ligne_total)
    #         it += 1
    #         control_change_jour = ligne_autre[n][3].day
    #         n += 1
    #     entete = ["N°", "Nom du client", "Vendu par", "Date et heure d'achat", "Montant payé"]
    #     g = 0
    #     f = max([len(tx) for tx in list_list_prod])
    #     for qpq in range(6, f + 1, 3):
    #         entete.append(f"produit {g}")
    #         entete.append(f"Quantité {g}")
    #         entete.append(f"prix unitaire {g}")
    #         g += 1
    #     dfram = pd.DataFrame(list_list_prod, columns=entete)
    #     ma_base_donnee.close()
    #     directory = filedialog.asksaveasfile(title="Veuillez selectionner l'emplacement du fichier Excel",
    #                                          initialdir="/", initialfile="Liste des ventes",
    #                                          defaultextension=".xlsx",
    #                                          filetypes=(("xlsx filles", "*.xlsx"),))
    #
    #     noom = directory.name
    #     dfram.to_excel(directory.name)
    #     directory.close()
    #     ques = messagebox.askyesno(nom_ets, "Vos données ont été importées avec succès\n"
    #                                         "Voulez-vous ouvrir le fichier maintenant?")
    #     if ques:
    #         os.startfile(noom)
