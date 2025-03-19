import sqlite3

class Librairie:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("librairie.db")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erreur d'ouverture de la base de données : {e}")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def retirer_livre(self, id):
        sql = "DELETE FROM livres WHERE id = ?"
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            print("Livre retiré avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors du retrait du livre : {e}")

def test3(): // Petit test pour vérifier que ça marche
    lib = Librairie()
    lib.retirer_livre(1)  # Supprime le livre avec l'ID 1 (exemple)

test3()
