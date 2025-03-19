import sqlite3

class Librairie:
    def __init__(self):
        self.conn = sqlite3.connect("librairie.db")
        self.cursor = self.conn.cursor()
        
        # Création de la table si elle n'existe pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                annee INTEGER
            )
        """)
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def ajouter_livre(self, titre, auteur, annee):
        try:
            self.cursor.execute("""
                INSERT INTO livres (titre, auteur, annee)
                VALUES (?, ?, ?)
            """, (titre, auteur, annee))
            self.conn.commit()
            print("Livre ajouté avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du livre : {e}")

def test(): // Test pour verifier que ca marche
    lib = Librairie()
    lib.ajouter_livre("1984", "George Orwell", 1949)
    lib.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943)

test()
