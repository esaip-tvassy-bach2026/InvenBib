import sqlite3

class Librairie:
    def __init__(self):
        self.conn = sqlite3.connect("librairie.db")
        self.cursor = self.conn.cursor()
        
        # Création de la table si elle n'existe pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                isbn INTEGER PRIMARY KEY,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                annee INTEGER
            )
        """)
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def ajouter_livre(self, isbn, titre, auteur, annee):
        try:
            self.cursor.execute("""
                INSERT INTO livres (isbn, titre, auteur, annee)
                VALUES (?, ?, ?)
            """, (isbn, titre, auteur, annee))
            self.conn.commit()
            print("Livre ajouté avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du livre : {e}")

def test(): // Test pour verifier que ca marche
    lib = Librairie()
    lib.ajouter_livre(int(444444444444),"1984", "George Orwell", int(1949))
    lib.ajouter_livre(int(676676767),"Le Petit Prince", "Antoine de Saint-Exupéry", int(1943))

test()
