from ConstantFile import *
import reportlab
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, A6, A7
from Ets_Info_File import *
from reportlab.platypus import paragraph, TableStyle
from reportlab.platypus.tables import Table
from reportlab.lib import colors
import subprocess
import os
from MysqlService import *
import win32api


def imprimer_vente_analyse_msedge(identifiant=0):
    """Imprimmer les ventes"""
    vente_service = VenteTableService()
    produit_table_service = ProduitTableService()
    setting_service = SettingService()
    """Selectionner la derniere vente"""
    if identifiant != 0:
        vente_service.select_id_relatif_with_id(identifiant)
        liste_vente = vente_service.select_ventes_with_id_relatif(vente_service.select_id_relatif_with_id(identifiant))
    else:
        identifiant = vente_service.select_last_vente_id_relatif()
        liste_vente = vente_service.select_ventes_with_id_relatif(identifiant)

    prix_unitaire_achat_impr = []
    quantite_achete_impr = []
    produit_achete_impr = []
    somme_totale = 0
    date_vente = ""
    for elementm in liste_vente:
        element = elementm
        # print(element)
        element = element[:-9]
        element = [i for i in element if i]
        element = [i for i in element if i is not None]
        produit_achete_impr += element[4:-4:5]
        quantite_achete_impr += element[5:-3:5]
        prix_unitaire_achat_impr += element[6:-2:5]
        date_vente = element[3]
        # print(element)
        somme_totale += elementm[-10]

    ligne_facture_produit = [["", "", f"Facture N° {identifiant}", ""],
                             ["", "",
                              f"Achat du: {str(date_vente.day).zfill(2)} {dictionnaire_mois[date_vente.month]} "
                              f"{date_vente.year} à {str(date_vente.hour).zfill(2)}H{str(date_vente.minute).zfill(2)}Min",
                              ""],
                             ["", "",
                              f"Facture du: {str(date.today().day).zfill(2)} {dictionnaire_mois[date.today().month]} "
                              f"{date_vente.year} à {datetime.today().hour}H{str(datetime.today().minute).zfill(2)}Min", ],
                             [f"{'Produit acheté' if len(produit_achete_impr) == 1 else 'Produits achetés'}",
                              f"{'Quantité' if len(produit_achete_impr) == 1 else 'Quantités'}", "Prix unitaire"
                                 , "Montant"]]
    i = 0
    for produit in produit_achete_impr:
        ligne_facture_produit += [
            [produit_table_service.select_name_with_id(produit), f"{quantite_achete_impr[i]:.0f}", f"{prix_unitaire_achat_impr[i]:.0f}"
                , f"{quantite_achete_impr[i] * prix_unitaire_achat_impr[i]:.0f}"]]
        i += 1

    ligne_facture_produit += [["Somme totale Payée", "", "", f"{somme_totale:.0f}"]]

    facture = f"facture_client_pdf\\FactureClient{identifiant}.pdf"
    canevas = Canvas(facture, pagesize=A4)
    canevas.setFont("Times-Bold", 9)
    canevas.drawString(2 * cm, 25.7 * cm, num_identifiant_unik)
    canevas.setFont("Times-Bold", 11)
    canevas.setFillColor("blue")
    canevas.drawString(8 * cm, 28 * cm, nom_ets)
    canevas.setStrokeColor("blue")
    canevas.rect(1.5 * cm, 2 * cm, 17 * cm, 26.5 * cm, fill=0)
    canevas.drawImage(logo, 2 * cm, 26 * cm, width=70, height=70, mask="auto")  # , anchor="nw")
    y = len(produit_achete_impr)

    style_tableau = TableStyle([("GRID", (0, 3), (-1, -1), 1, colors.blue), ("FONTSIZE", (0, 3), (-1, -1), 9)
                                   , ("SPAN", (0, 0), (1, 2)), ("SPAN", (2, 0), (3, 0)),
                                ("SPAN", (2, 1), (3, 1)), ("ALIGN", (0, 0), (4, 3), "RIGHT"),
                                ("SPAN", (2, 2), (3, 2)), ("BOX", (0, 0), (-1, -1), 1, colors.blue),
                                ("ALIGN", (0, 2), (-1, -1), "LEFT"),
                                ("INNERGRID", (0, 2), (-1, -1), 1, colors.blue),
                                ("VALIGN", (0, 2), (-1, -1), "MIDDLE"), ("LINEBEFORE",
                                                                         (2, 1), (2, 2), 2, colors.white),
                                ("SPAN", (0, -1), (-2, -1)), ("ALIGN", (0, 0), (3, 2), "RIGHT")])

    tableau = Table(ligne_facture_produit, colWidths=4 * cm, rowHeights=1 * cm, style=style_tableau)
    tableau.wrapOn(canevas, 0.5 * cm, 1 * cm)
    tableau.drawOn(canevas, 2 * cm, (29.7 - y - 6.25) * cm)
    canevas.save()
    # os.system("help assoc")
    # p = f"C:\\Users\\HP\\Desktop\\projet_python\\facture_client_pdf\\FactureClient{identifiant}.pdf"
    # p = f"facture_client_pdf\\FactureClient{identifiant}.pdf"
    p = os.path.join("facture_client_pdf", f"FactureClient{identifiant}.pdf")
    # facture_app = setting_service.select_setting("facture_app")

    rl_path = os.path.join(os.getcwd(), p)
    # rl_path = rl_path.replace("\\", "/")
    # print(rl_path)
    # subprocess.call(["open", rl_path])
    nfcpdf = "pdffile.pdf"
    # win32api.ShellExecute(0, "print", rl_path, None, None, 0)
    # os.startfile(rl_path, "print")
    # edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    edge = setting_service.select_setting("facture_app")
    cmd = f"{edge} /p {rl_path}"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stdr = proc.communicate()
    exit_code = proc.wait()


# imprimer_vente_analyse_msedge(1630)




