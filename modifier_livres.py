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

    def modifier_livre(self, isbn, nouveau_titre, nouvel_auteur, nouvelle_annee):
        sql = "UPDATE livres SET titre = ?, auteur = ?, annee = ? WHERE isbn = ?"
        try:
            self.cursor.execute(sql, (nouveau_titre, nouvel_auteur, nouvelle_annee, isbn))
            self.conn.commit()
            print("Livre modifié avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la modification du livre : {e}")

def test2(): // Test pour verifier que ça fonctionne
    lib = Librairie()
    lib.modifier_livre(int(7777), "Animal Farm", "George Orwell", int(1945))

test()
