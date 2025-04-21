import sqlite3  # Importe le module sqlite3 pour manipuler des bases de données SQLite

class Librairie:
    def __init__(self):
        """
        Constructeur de la classe Librairie.
        Tente d'ouvrir une connexion à la base de données 'librairie.db'.
        Si la connexion échoue, affiche un message d'erreur.
        """
        try:
            # Connexion à la base de données SQLite (création si elle n'existe pas)
            self.conn = sqlite3.connect("librairie.db")
            # Création d'un curseur pour exécuter des requêtes SQL
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            # Gestion d'une éventuelle erreur lors de l'ouverture de la base
            print(f"Erreur d'ouverture de la base de données : {e}")

    def __del__(self):
        """
        Destructeur de la classe.
        Ferme proprement la connexion à la base de données si elle existe.
        """
        if hasattr(self, 'conn'):
            self.conn.close()  # Ferme la connexion pour éviter les fuites de ressources

    def lister_livres(self):
        """
        Méthode pour afficher tous les livres enregistrés dans la base de données.
        Affiche un message si aucun livre n'est trouvé.
        """
        try:
            # Exécute une requête SQL pour récupérer tous les livres
            self.cursor.execute("SELECT * FROM LIVRES")
            livres = self.cursor.fetchall()  # Récupère tous les résultats de la requête

            if not livres:
                # Si la liste est vide, informe l'utilisateur
                print("Aucun livre n'est enregistré dans la base.")
                return

            # Affiche un en-tête pour la liste des livres
            print("Liste des livres enregistrés :")
            print("-" * 50)
            # Parcourt la liste des livres et affiche leurs informations
            for livre in livres:
                print(f"ID (ISBN) : {livre[0]}")     # Affiche l'ISBN (identifiant unique)
                print(f"Titre     : {livre[1]}")     # Affiche le titre
                print(f"Auteur    : {livre[2]}")     # Affiche l'auteur
                print(f"Année     : {livre[3]}")     # Affiche l'année de publication
                print(f"Note      : {livre[4]}")     # Affiche la note du livre
                print("-" * 50)                      # Séparateur visuel entre les livres
        except sqlite3.Error as e:
            # Gestion d'une éventuelle erreur lors de la récupération des livres
            print(f"Erreur lors de la récupération des livres : {e}")

    def modifier_livre(self, isbn):
        """
        Permet de modifier les informations d'un livre existant à partir de son ISBN.
        Affiche les informations actuelles, puis demande à l'utilisateur de saisir
        de nouvelles valeurs (ou de laisser vide pour conserver la valeur actuelle).
        Met à jour la base de données avec les nouvelles informations.
        """
        try:
            # Recherche le livre correspondant à l'ISBN fourni
            self.cursor.execute("SELECT * FROM LIVRES WHERE id = ?", (isbn,))
            livre = self.cursor.fetchone()  # Récupère la première ligne du résultat

            if not livre:
                # Si aucun livre n'est trouvé, informe l'utilisateur et arrête la méthode
                print("Aucun livre trouvé avec cet ISBN.")
                return

            # Affiche les caractéristiques actuelles du livre
            print(f"Caractéristiques actuelles du livre :")
            print(f"ID: {livre[0]}")
            print(f"Titre: {livre[1]}")
            print(f"Auteur: {livre[2]}")
            print(f"Année de publication: {livre[3]}")
            print(f"Note: {livre[4]}")

            # Demande à l'utilisateur de saisir de nouvelles valeurs pour chaque champ
            # Si l'utilisateur appuie sur Entrée sans rien saisir, la valeur actuelle est conservée
            nouvel_auteur = input("Entrez le nouvel auteur (laisser vide pour conserver l'actuel): ") or livre[2]
            nouvelle_annee = input("Entrez la nouvelle année de publication (laisser vide pour conserver l'actuelle): ") or livre[3]
            nouvelle_note = input("Entrez la nouvelle note (laisser vide pour conserver l'actuelle): ") or livre[4]

            # Prépare la requête SQL de mise à jour
            sql_update = """
                UPDATE LIVRES 
                SET auteur = ?, ann_publi = ?, note = ? 
                WHERE id = ?
            """
            # Exécute la requête de mise à jour avec les nouvelles valeurs
            self.cursor.execute(sql_update, (nouvel_auteur, int(nouvelle_annee), int(nouvelle_note), isbn))
            self.conn.commit()  # Sauvegarde les modifications dans la base

            print("Les caractéristiques du livre ont été mises à jour avec succès.")
        except sqlite3.Error as e:
            # Gestion d'une éventuelle erreur lors de la modification
            print(f"Erreur lors de la modification du livre : {e}")

def test_liste():
    """
    Fonction de test pour vérifier l'affichage de la liste des livres.
    """
    lib = Librairie()
    lib.lister_livres()

# test_liste()  # Décommentez cette ligne pour tester la méthode lister_livres()
