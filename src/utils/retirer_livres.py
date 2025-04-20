import sqlite3  # Importe le module sqlite3 pour manipuler une base de données SQLite

class Librairie:
    def __init__(self):
        """
        Constructeur de la classe Librairie.
        Tente d'établir une connexion à la base de données 'librairie.db'.
        Si la connexion échoue, affiche un message d'erreur.
        """
        try:
            # Connexion à la base de données (création du fichier s'il n'existe pas)
            self.conn = sqlite3.connect("librairie.db")
            # Création d'un curseur pour exécuter les requêtes SQL
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            # Gestion d'erreur lors de l'ouverture de la base
            print(f"Erreur d'ouverture de la base de données : {e}")

    def __del__(self):
        """
        Destructeur de la classe.
        Ferme proprement la connexion à la base de données si elle existe,
        pour éviter toute fuite de ressources.
        """
        if hasattr(self, 'conn'):
            self.conn.close()

    def retirer_livre(self, isbn):
        """
        Supprime un livre de la base de données en fonction de son identifiant (ISBN).

        :param isbn: L'identifiant du livre à supprimer (doit correspondre à la colonne 'id' dans la table)
        """
        # Requête SQL pour supprimer un livre selon son ID
        sql = "DELETE FROM livres WHERE id = ?"
        try:
            # Exécution de la requête avec le paramètre fourni pour éviter les injections SQL
            self.cursor.execute(sql, (isbn,))
            self.conn.commit()  # Sauvegarde la suppression dans la base
            print("Livre retiré avec succès.")
        except sqlite3.Error as e:
            # Gestion d'erreur lors de la suppression
            print(f"Erreur lors du retrait du livre : {e}")

def test3():
    """
    Fonction de test pour vérifier que la suppression d'un livre fonctionne.
    Ici, on tente de supprimer le livre ayant l'ID 1.
    """
    lib = Librairie()
    lib.retirer_livre(1)  # Supprime le livre avec l'ID 1 (exemple)

# test3()  # Décommentez cette ligne pour tester la suppression
