import sqlite3  # Importe le module sqlite3 pour gérer une base de données SQLite

class Librairie:
    def __init__(self):
        # Connexion à la base de données (ou création si elle n'existe pas)
        self.conn = sqlite3.connect("librairie.db")
        self.cursor = self.conn.cursor()
        
        # Création de la table 'livres' si elle n'existe pas déjà
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                isbn INTEGER PRIMARY KEY,   # Identifiant unique du livre
                titre TEXT NOT NULL,        # Titre du livre (obligatoire)
                auteur TEXT NOT NULL,       # Nom de l'auteur (obligatoire)
                annee INTEGER               # Année de publication
            )
        """)
        self.conn.commit()  # Sauvegarde les modifications dans la base de données

    def __del__(self):
        # Ferme la connexion à la base de données lors de la destruction de l'objet
        self.conn.close()

    def ajouter_livre(self, isbn, titre, auteur, annee):
        """
        Ajoute un nouveau livre à la base de données.
        Paramètres :
            isbn   : numéro ISBN du livre (doit être unique)
            titre  : titre du livre
            auteur : nom de l'auteur
            annee  : année de publication
        """
        try:
            self.cursor.execute("""
                INSERT INTO livres (isbn, titre, auteur, annee)
                VALUES (?, ?, ?, ?)
            """, (isbn, titre, auteur, annee))  # Insère les données dans la table
            self.conn.commit()  # Sauvegarde la modification
            print("Livre ajouté avec succès.")
        except sqlite3.Error as e:
            # Affiche un message d'erreur si l'insertion échoue (ex : ISBN déjà existant)
            print(f"Erreur lors de l'ajout du livre : {e}")

def test():
    """
    Fonction de test pour vérifier que l'ajout de livres fonctionne.
    """
    lib = Librairie()
    lib.ajouter_livre(int(444444444444), "1984", "George Orwell", int(1949))
    lib.ajouter_livre(int(676676767), "Le Petit Prince", "Antoine de Saint-Exupéry", int(1943))

# test()  # Décommentez cette ligne pour faire le test
