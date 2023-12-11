import os
from tkinter import *
controleur_password = 0
controleur_password_extreme = 0
tantative_max = 5

def load_image_path(path):
    return os.path.join(os.getcwd().split("blanco")[0], "blanco", "image_app", path)

couleur_bouton = "lightgray"
couleur_fenetre = couleur_bouton
couleur_note_book = "whitesmoke"
couleur_sous_fenetre = couleur_bouton
couleur_frame = "SystemButtonFace"
couleur_bordure = "blue"
couleur_fg_treeview = "#000000"
couleur_inverse_tree = "white"
couleur_champs = couleur_fg_treeview
couleur_label = couleur_bouton
couleur_police = couleur_fg_treeview
couleur_police_champs = "#000000"
couleur_invers_treeeview = couleur_fg_treeview
coul_titre_vente = couleur_bouton
couleur_nuance = "blue"
fg_nuance = "black"

relief_widget = SOLID
bd_widget = 0
hauteur_max_sous_fenetre = 768
largeur_max_sous_fenetre = 1366
hauteur_min_sous_fenetre = 768
largeur_min_sous_fenetre = 1366
(police, taille_police_texte) = ("arial", 10)
hauteur_label = 4
largeur_label = 40
largeur_champs = 30
hauteur_label_achat = 2
largeur_label_achat = 12
largeur_champs_combobox = 24
largeur_champs_achat = 17
largeur_champs_achat_combobox = 18
# dur_prix = 20
largeur_bouton_principal = 20
ipedy_bouton_principal = 20
control_connexion = 0
ipedy_frame_vente = 5
controleur_etat_bouton_inserer_valeur_entry_prix = 0
password_bd = "672279946"
hote = "localhost"
utilisateur = "root"
image_defaut_produit = load_image_path("IMG_9823.JPG")
logo = r"image_app/logo_del_blanco33.ico"
image_annuler_dernier_enreg_prod_stck = load_image_path("IMG_2331.PNG")
image_annuler_mode_midif = load_image_path("IMG_2332.PNG")
image_validation = load_image_path("IMG_2343.PNG")
image_validation_vert = load_image_path("IMG_2341.JPG")
image_validation_noir = load_image_path("IMG_2342.PNG")
image_suppression = load_image_path("IMG_2359.PNG")
image_suppression_noir = load_image_path("IMG_2362.PNG")
image_suppression_rouge = load_image_path("IMG_2361.PNG")
image_nettoyage_noir = load_image_path("IMG_2387.PNG")
image_suppression_noir_croix = load_image_path(r"image_app/IMG_2346.PNG")
image_flashback = load_image_path("IMG_2348.JPG")
image_imppression = load_image_path("IMG_2354.PNG")
image_historique = load_image_path("IMG_2335.JPG")
image_nettoyage = load_image_path("IMG_2390.JPG")
image_calculatrice = load_image_path("IMG_2385.PNG")
image_dossier = load_image_path("IMG_2350.PNG")
image_ajout_bd = load_image_path("IMG_2369.PNG")
image_recherche = load_image_path("IMG_2329.PNG")
image_ajout_liste = load_image_path("IMG_2371.PNG")  # par exemple liste approvisionnement
image_direction_gauche = load_image_path("IMG_2609.PNG")
image_direction_droite = load_image_path("IMG_2603.JPG")
image_direction_droite_petit = load_image_path("IMG_2604.PNG")
image_imga = load_image_path("IMG_3373.PNG")
image_supp_cham = load_image_path("IMG_3373 (2).PNG")
image_notification = load_image_path("IMG_3476.JPG")
image_extension = load_image_path("IMG_2605.PNG")
image_accueil = load_image_path("IMG_3640.PNG")
image_accueil_princ = load_image_path("IMG_3635.PNG")
image_stat_west_vnt = load_image_path("IMG_3648.PNG")
image_vnt_credit = load_image_path("IMG_2582.PNG")
image_cmd_vnt = load_image_path("IMG_2336.PNG")
image_stock_critic = load_image_path("IMG_3689.JPG")
image_date_critic = load_image_path("IMG_3679.PNG")
image_liste_prod = load_image_path("IMG_3696.PNG")
image_fiche_client = load_image_path("IMG_3709.PNG")
image_prod_reguier = load_image_path("IMG_3749.PNG")
image_consult_prod = load_image_path("IMG_3670.PNG")
image_liste_vente = load_image_path("IMG_3691.PNG")
image_approv = load_image_path("IMG_2370.PNG")
image_ajout_prod = load_image_path("IMG_2369.PNG")
image_alerte_urgence = load_image_path("IMG_3678.PNG")
image_list_prod_cote_client = load_image_path("IMG_3694.PNG")
image_description_prod_stock = load_image_path("IMG_3717.PNG")
image_parametre = load_image_path("IMG_2396.PNG")
image_vendre = load_image_path("th.jpg")
image_admin = load_image_path("télécharger.jpg")
image_tree_accueil = load_image_path("IMG_3747.PNG")

ANCIEN_VENDEUR = ""


liste_unite_grammage = ["ml", "mg", "g", "l"]
list_echance_credit_predefini = ["1 jour", "2 jours", "1 semaine", "2 semaines", "1 mois", "2 mois", "3 mois", "6 mois",
                                 "1 an"]

dictionnaire_mois = {1: "Janvier", 2: "Fevrier", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
                     7: "Juillet", 8: "Aout", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Decembre"}

dico_semaine = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"}


