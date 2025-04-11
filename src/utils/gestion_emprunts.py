# Code realise par Thomas VASSY--ROUSSEAU.
"""
Ces fonctions permettent de gerer le rendu de livres, leur emprunt et l-affichage de l-historique d-emprunts des utilisateurs.
"""
# import sqlite3

def verif_isbn(isbn):
    """
    Cette fonction permet de verifier que le code ISBN donne est correct (nombre de chiffres).
    
    Param:
        isbn: int,
    Result: bool.
    """
    assert isinstance(isbn,int),"ERREUR : L-ISBN donne n-est pas un entier."
    if len(str(isbn)) == 13:
        print("Le code ISBN est correct.")
        return True
    elif len(str(isbn)) != 13:
        print("Le code ISBN donne est incorrect.")
        return False

def historique(idn):
    """
    Cette fonction permet d-afficher l-hostorique des emprunts d-un utilisateur en fonction de son numero d-identification (ID).
    
    Param:
        idn: int,
    Result:
        histo: list.
    """
    assert isinstance(idn,int), "ERREUR : L-ID donne n-est pas une variable de type entier." # Assertion pour afficher les erreurs.
    print(f"Fonction en cours de developpement. Variable donnee en parametre : {idn}.")
    histo = ["coucou"]
    return histo

def emprunt(isbn,idn):
    """
    Cette fonction permet d-emprunter un livre a partir de son ISBN et de l-ID utilisateur.
    
    Param:
        isbn: int,
        idn: int,
    Result:
        succ: str.
    """
    # Assertion pour verifier les variables en parametres.
    assert isinstance(idn,int) and isinstance(isbn,int) and verif_isbn(isbn)==True,"ERREUR : L-ID ou l-ISBN donne n-est pas une variable de type entier ou l-ISBN donne n-a pas 13 chiffres."
    print(f"Fonction en cours de developpement. Variables donnees en parametres : {idn} ; {isbn}.")
    succ = "Le livre a ete emprunte avec succes."
    return succ

def rendu(isbn,idn):
    """
    Cette fonction permet de rendre un livre via l-ISBN du livre et le numero d-identification de l-utilisateur (ID).
    
    Param:
        isbn: int,
        idn: int,
    Result:
        succ: str.
    """
    # Assertion pour verifier les variables en parametres.
    assert isinstance(idn,int) and isinstance(isbn,int) and verif_isbn(isbn)==True,"ERREUR : L-ID ou l-ISBN donne n-est pas une variable de type entier ou l-ISBN donne n-a pas 13 chiffres."
    print(f"Fonction en cours de developpement. Variables donnees en parametres : {idn} ; {isbn}.")
    succ = "Le livre a bien ete rendu avec succes."
    return succ

# Tests pour tester ces fonctions
# print("\nTests en cours !")
# isbn_a_tester = int(input("Donnez un ISBN a tester : "))
# idn_a_tester = int(input("Donnez un ID utilisateur a tester : "))
# print(verif_isbn(isbn_a_tester))
# historique(idn_a_tester)
# emprunt(isbn_a_tester,idn_a_tester)
# rendu(isbn_a_tester,idn_a_tester)
