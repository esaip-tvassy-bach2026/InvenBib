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

    def lister_livres(self):
        """
        Liste tous les livres enregistrés dans la base de données.
        """
        try:
            self.cursor.execute("SELECT * FROM LIVRES")
            livres = self.cursor.fetchall()

            if not livres:
                print("Aucun livre n'est enregistré dans la base.")
                return

            print("Liste des livres enregistrés :")
            print("-" * 50)
            for livre in livres:
                print(f"ID (ISBN) : {livre[0]}")
                print(f"Titre     : {livre[1]}")
                print(f"Auteur    : {livre[2]}")
                print(f"Année     : {livre[3]}")
                print(f"Note      : {livre[4]}")
                print("-" * 50)
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des livres : {e}")

    def modifier_livre(self, isbn):
        # Récupérer les caractéristiques du livre
        try:
            self.cursor.execute("SELECT * FROM LIVRES WHERE id = ?", (isbn,))
            livre = self.cursor.fetchone()
            
            if not livre:
                print("Aucun livre trouvé avec cet ISBN.")
                return
            
            print(f"Caractéristiques actuelles du livre :")
            print(f"ID: {livre[0]}")
            print(f"Titre: {livre[1]}")
            print(f"Auteur: {livre[2]}")
            print(f"Année de publication: {livre[3]}")
            print(f"Note: {livre[4]}")

            # Demander les nouvelles valeurs à l'utilisateur
            nouvel_auteur = input("Entrez le nouvel auteur (laisser vide pour conserver l'actuel): ") or livre[2]
            nouvelle_annee = input("Entrez la nouvelle année de publication (laisser vide pour conserver l'actuelle): ") or livre[3]
            nouvelle_note = input("Entrez la nouvelle note (laisser vide pour conserver l'actuelle): ") or livre[4]

            # Mettre à jour les informations dans la base de données
            sql_update = """
                UPDATE LIVRES 
                SET auteur = ?, ann_publi = ?, note = ? 
                WHERE id = ?
            """
            self.cursor.execute(sql_update, (nouvel_auteur, int(nouvelle_annee), int(nouvelle_note), isbn))
            self.conn.commit()
            
            print("Les caractéristiques du livre ont été mises à jour avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la modification du livre : {e}")

def test_liste():
    lib = Librairie()
    lib.lister_livres()

# test_liste()

