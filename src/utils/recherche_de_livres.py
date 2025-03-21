import sqlite3

def rechercher_livre(critere, valeur):
    """
    Recherche un livre dans la base de données en fonction du critère et de la valeur fournie.
    
    :param critere: Le champ à rechercher (isbn, titre, auteur, annee)
    :param valeur: La valeur à rechercher
    :return: Une liste des livres trouvés
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('librairie.db')
        cursor = conn.cursor()
        
        # Vérification que le critère est valide
        if critere not in ['isbn', 'titre', 'auteur', 'annee']:
            raise ValueError("Critère invalide. Les critères valides sont : isbn, titre, auteur, annee.")
        
        # Requête SQL pour rechercher les livres
        query = f"SELECT * FROM livres WHERE {critere} LIKE ?"
        cursor.execute(query, ('%' + valeur + '%',))
        
        # Récupération des résultats
        resultats = cursor.fetchall()
        
        # Fermeture de la connexion
        conn.close()
        
        return resultats
    
    except sqlite3.Error as e:
        print(f"Erreur lors de l'accès à la base de données : {e}")
        return []
    except ValueError as ve:
        print(ve)
        return []

# Exemple d'utilisation
print("Bienvenue dans le système de recherche de livres.")
print("Vous pouvez rechercher un livre par : isbn, titre, auteur ou annee.")

critere = input("Entrez le critère de recherche (isbn, titre, auteur, annee) : ").strip().lower()
valeur = input(f"Entrez la valeur à rechercher pour le critère '{critere}' : ").strip()

# Appel de la fonction pour rechercher les livres
livres_trouves = rechercher_livre(critere, valeur)

# Affichage des résultats
if livres_trouves:
    print(f"\nLivres trouvés pour {critere} contenant '{valeur}' :")
    for livre in livres_trouves:
        print(f"ISBN: {livre[0]}, Titre: {livre[1]}, Auteur: {livre[2]}, Année: {livre[3]}")
else:
    print("\nAucun livre trouvé.")
