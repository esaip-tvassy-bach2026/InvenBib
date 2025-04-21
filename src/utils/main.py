# Code realise par Thomas VASSY--ROUSSEAU.
"""
Ceci est le menu principal de notre logiciel en console.
Logiciel complet realise par :
Thomas VASSY--ROUSSEAU
Nolan MAUSSION
Primael KPONOU
Nous sommes tous en Bachelor Cybersecurite 2 a l-ESAIP a Saint-Barthelemy-d'Anjou.
"""
# Importation des bibliotheques.
from ajout_livres import Librairie as lib_add
from retirer_livres import Librairie as lib_del
from modifier_livres import Librairie as lib_edit
from lister_livres import Librairie as lib_total
from recherche_de_livres import rechercher_livre
from menu_client import menu_client
from chatbot_recherche import menu_recherche_chatbot
from gestion_emprunts import historique
from gestion_emprunts import emprunt
from gestion_emprunts import rendu

print("PRE-REQUIS : LANCEZ LE SCRIPT creation_base_de_donnees.py AVANT DE LANCER CELUI-CI SI CE N-EST PAS DEJA FAIT !")

def afficher_menu_principal():
    """
    Ceci est la fonction permettant d-afficher le menu principal.
    """
    print("\n=== MENU PRINCIPAL INVENBIB ===")
    print("1. Gestion des livres")
    print("2. Gestion des emprunteurs")
    print("3. Gestion des emprunts")
    print("4. Recherche avancée")
    print("5. Chatbot IA Mistral")
    print("0. Quitter")

def menu_gestion_livres():
    """
    Ceci est la fonction permettant d-afficher le menu de gestion des livres.
    """
    print("\n=== GESTION DES LIVRES ===")
    print("1. Créer un livre")
    print("2. Modifier un livre")
    print("3. Supprimer un livre")
    print("4. Lister tous les livres")
    print("0. Retour au menu principal")
    
    choix_m1 = str(input("Votre choix : "))
    if choix_m1 == "1":
        isbn1 = int(input("ISBN (13 chiffres) : "))
        titre = str(input("Titre du livre : "))
        auteur = str(input("Auteur : "))
        annee = int(input("Année de publication : "))
        lib_add.ajouter_livre(isbn1,titre,auteur,annee)
    elif choix_m1 == "2":
        isbn2 = int(input("ISBN du livre à modifier : "))
        nouveau_titre = str(input("Nouveau titre : "))
        nouvel_auteur = str(input("Nouvel auteur : "))
        nouvelle_annee = int(input("Nouvelle année : "))
        lib_edit.modifier_livre(isbn2,nouveau_titre,nouvel_auteur,nouvelle_annee)
    elif choix_m1 == "3":
        isbn3 = int(input("ISBN du livre à supprimer : "))
        lib_del.retirer_livre(isbn3)
    elif choix_m1 == "4":
        lib_total.lister_livres()

def menu_gestion_emprunteurs():
    """
    Ceci est la fonction permettant de lancer la fonction de gestion des emprunteurs.
    """
    menu_client()

def menu_de_gestion_des_emprunts():
    """
    Ceci est la fonction permettant d-afficher et de gerer le menu de gestion des emprunts.
    """
    print("\n=== GESTION DES EMPRUNTS ===")
    print("1. Voir l-historique des emprunts d-un emprunteur.")
    print("2. Emprunter un livre.")
    print("3. Rendre un livre.")
    print("0. Retour au menu principal")
    
    choix_m3 = str(input("Que voulez-vous faire ? (0/1/2/3)"))
    if choix_m3 == "1":
        print("Vous pouvez utiliser la gestion des emprunts depuis le menu principal pour plus d-informations.")
        id_utilisateur = int(input("Quel est l-ID de l-utilisateur(trice) dont vous souhaitez visionner l-historique ?"))
        historique(id_utilisateur)
    elif choix_m3 == "2":
        print("Vous pouvez faire une recherche via la fonction correspondante en revenant au menu principal au besoin.")
        isbn_emprunt = int(input("Quel est le numero ISBN (13 chiffres) du livre que vous souhaitez emprunter ?"))
        print("Vous pouvez utiliser la gestion des emprunts depuis le menu principal pour plus d-informations.")
        iden_user = int(input("Quel est l-identifiant de l-utilisateur (ID) a associer a cet emprunt ?"))
        emprunt(isbn_emprunt,iden_user)
    elif choix_m3 == "3":
        print("Vous pouvez faire une recherche via la fonction correspondante en revenant au menu principal au besoin.")
        isbn_rendu = int(input("Quel est le numero ISBN (13 chiffres) du livre que vous sohaitez rendre ?"))
        print("Vous pouvez utiliser la gestion des emprunts depuis le menu principal pour plus d-informations.")
        iden_user2 = int(input("Quel est l-identifiant de l-utilisateur (ID) qui est en train de rendre un livre ?"))
        rendu(isbn_rendu,iden_user2)

def menu_recherche_avancee():
    """
    Ceci est la fonction permettant d-afficher le menu de la recherche avancee.
    """
    print("\n=== RECHERCHE AVANCÉE ===")
    print("1. Par titre")
    print("2. Par auteur")
    print("3. Par année")
    print("4. Par ISBN")
    print("0. Retour au menu principal")
    
    choix_m2 = int(input("Votre choix : "))
    valeur = str(input("Terme de recherche : "))
    criteres = {1: 'titre', 2: 'auteur', 3: 'annee', 4: 'isbn'}
    resultats = rechercher_livre(criteres[choix_m2], valeur)
    print(f"\n{len(resultats)} résultats trouvés :")
    for livre in resultats:
        print(f"ISBN: {livre[0]} | {livre[1]} par {livre[2]} ({livre[3]})")

def menu_chatbot():
    """
    Ceci est la fonction permettant de lancer le chatbot.
    """
    print("\n=== CHATBOT ===")
    menu_recherche_chatbot()

def dev_launch(mode):
    """
    Cette fonction permet de passer le menu en mode dev.
    
    Param:
        mode: str,
    Result:
        Affichage du menu.
    """
    assert isinstance(mode,str) and (mode == "Oui" or mode == "Non"),"ERREUR : Vous avez du faire une faute de frappe."
    if mode == "Oui":
        print("Lancement du mode DEV.")
        
        afficher_menu_principal()
        choix = str(input("Votre choix : "))
        
        # Dictionnaire permettant de gerer les choix disponibles pour le menu et de gerer les erreurs simplement en cas de probleme.
        menus = {
            '1': menu_gestion_livres,
            '2': menu_gestion_emprunteurs,
            '3': menu_de_gestion_des_emprunts,
            '4': menu_recherche_avancee,
            '5': menu_chatbot,
            '0': lambda: print("Au revoir !")
        }
           
        if choix in menus:
            # Lancement de la fonction correspondante au choix effectue par l-utilisateur.
            menus[choix]()
        else:
            # Message d-erreur en cas d-erreur d-entree.
            print("Option invalide")
    elif mode == "Non":
        print("Lancement en mode normal.")
        
        # Lancement du menu, execution a l-infini jusqu-a la fermeture du logiciel.
        while True:
            afficher_menu_principal()
            choix = str(input("Votre choix : "))
            
            # Dictionnaire permettant de gerer les choix disponibles pour le menu et de gerer les erreurs simplement en cas de probleme.
            menus = {
                '1': menu_gestion_livres,
                '2': menu_gestion_emprunteurs,
                '3': menu_de_gestion_des_emprunts,
                '4': menu_recherche_avancee,
                '5': menu_chatbot,
                '0': lambda: exit("Au revoir !") # Permet de fermer Python en cas d-appui sur zero.
            }
            
            if choix in menus:
                # Lancement de la fonction correspondante au choix effectue par l-utilisateur.
                menus[choix]()
            else:
                # Message d-erreur en cas d-erreur d-entree.
                print("Option invalide")

# Verification du mode dev
dev_mode = str(input("Sommes-nous en mode de developpement ? (Oui/Non)"))
dev_launch(dev_mode)
