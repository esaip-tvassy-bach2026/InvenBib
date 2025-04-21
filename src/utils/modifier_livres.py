import sqlite3  # Importe le module sqlite3 pour travailler avec une base de données SQLite

class Librairie:
    def __init__(self):
        """
        Constructeur de la classe Librairie.
        Tente d'établir une connexion à la base de données 'librairie.db'.
        Si la connexion échoue, affiche un message d'erreur.
        """
        try:
            # Connexion à la base de données (création si elle n'existe pas)
            self.conn = sqlite3.connect("librairie.db")
            # Création d'un curseur pour exécuter les requêtes SQL
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            # Affiche une erreur si la connexion échoue
            print(f"Erreur d'ouverture de la base de données : {e}")

    def __del__(self):
        """
        Destructeur de la classe.
        Ferme la connexion à la base de données si elle existe,
        pour libérer les ressources.
        """
        if hasattr(self, 'conn'):
            self.conn.close()

    def modifier_livre(self, isbn, nouveau_titre, nouvel_auteur, nouvelle_annee):
        """
        Modifie les informations d'un livre existant dans la base de données.

        Paramètres :
            isbn           : identifiant unique du livre à modifier
            nouveau_titre  : nouveau titre à enregistrer
            nouvel_auteur  : nouvel auteur à enregistrer
            nouvelle_annee : nouvelle année de publication à enregistrer
        """
        # Prépare la requête SQL de mise à jour
        sql = "UPDATE livres SET titre = ?, auteur = ?, annee = ? WHERE isbn = ?"
        try:
            # Exécute la requête avec les nouvelles valeurs
            self.cursor.execute(sql, (nouveau_titre, nouvel_auteur, nouvelle_annee, isbn))
            self.conn.commit()  # Sauvegarde les modifications
            print("Livre modifié avec succès.")
        except sqlite3.Error as e:
            # Affiche une erreur si la modification échoue
            print(f"Erreur lors de la modification du livre : {e}")

def test2():
    """
    Fonction de test pour vérifier que la modification d'un livre fonctionne.
    Modifie le livre ayant l'ISBN 7777.
    """
    lib = Librairie()
    lib.modifier_livre(int(7777), "Animal Farm", "George Orwell", int(1945))

# test2()  # Décommentez cette ligne pour tester la modification
