import sqlite3  # Import du module pour gérer les bases de données SQLite

def rechercher_livre(critere, valeur):
    """
    Recherche un livre dans la base de données en fonction du critère et de la valeur fournie.
    
    :param critere: Le champ à rechercher (isbn, titre, auteur, annee)
    :param valeur: La valeur à rechercher
    :return: Une liste des livres trouvés
    """
    try:
        # Connexion à la base de données (le fichier doit exister)
        conn = sqlite3.connect('librairie.db')
        cursor = conn.cursor()
        
        # Vérification que le critère fourni est valide pour éviter toute injection SQL
        if critere not in ['isbn', 'titre', 'auteur', 'annee']:
            raise ValueError("Critère invalide. Les critères valides sont : isbn, titre, auteur, annee.")
        
        # Construction de la requête SQL dynamiquement selon le critère
        # Utilisation de LIKE pour permettre la recherche partielle (sauf pour isbn et annee, qui sont numériques)
        query = f"SELECT * FROM livres WHERE {critere} LIKE ?"
        # Ajout des % pour permettre la recherche partielle (ex : "%Orwell%" trouvera "George Orwell")
        cursor.execute(query, ('%' + valeur + '%',))
        
        # Récupération de tous les résultats de la requête
        resultats = cursor.fetchall()
        
        # Fermeture de la connexion à la base de données
        conn.close()
        
        # Retourne la liste des livres trouvés (liste de tuples)
        return resultats
    
    except sqlite3.Error as e:
        # Gestion des erreurs liées à la base de données
        print(f"Erreur lors de l'accès à la base de données : {e}")
        return []
    except ValueError as ve:
        # Gestion des erreurs liées au critère invalide
        print(ve)
        return []

# --- Partie interactive pour l'utilisateur ---

print("Bienvenue dans le système de recherche de livres.")
print("Vous pouvez rechercher un livre par : isbn, titre, auteur ou annee.")

# Demande à l'utilisateur de saisir le critère de recherche
critere = input("Entrez le critère de recherche (isbn, titre, auteur, annee) : ").strip().lower()
# Demande la valeur à rechercher selon le critère choisi
valeur = input(f"Entrez la valeur à rechercher pour le critère '{critere}' : ").strip()

# Appel de la fonction pour rechercher les livres
livres_trouves = rechercher_livre(critere, valeur)

# Affichage des résultats trouvés
if livres_trouves:
    print(f"\nLivres trouvés pour {critere} contenant '{valeur}' :")
    for livre in livres_trouves:
        # Affiche chaque livre sous forme lisible
        print(f"ISBN: {livre[0]}, Titre: {livre[1]}, Auteur: {livre[2]}, Année: {livre[3]}")
else:
    print("\nAucun livre trouvé.")
