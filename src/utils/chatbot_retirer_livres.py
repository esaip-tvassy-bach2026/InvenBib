import sqlite3
import requests  # Pour interagir avec les API externes

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

    def retirer_livre(self, isbn):
        # Supprimer le livre de la base locale
        sql = "DELETE FROM livres WHERE id = ?"
        try:
            self.cursor.execute(sql, (isbn,))
            self.conn.commit()
            print("Livre retiré avec succès.")
            
            # Appeler l'API Mistral pour synchroniser la suppression
            self.sync_with_mistral_api(isbn)
        except sqlite3.Error as e:
            print(f"Erreur lors du retrait du livre : {e}")

    def sync_with_mistral_api(self, isbn):
        """
        Méthode pour synchroniser la suppression avec l'API Mistral.
        """
        api_url = "https://api.mistral.com/v1/books/delete"  # Remplacez par l'URL réelle de l'API
        headers = {
            "Authorization": "Mu3ZznNkoOtZvoz3sB9xjubCXzsqGEwQ2",  # Remplacez par votre token d'authentification
            "Content-Type": "application/json"
        }
        payload = {
            "isbn": isbn  # Envoyer l'identifiant du livre à supprimer
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print("Livre synchronisé avec succès sur Mistral.")
            else:
                print(f"Erreur lors de la synchronisation avec Mistral : {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Erreur lors de la communication avec l'API Mistral : {e}")

def test3():  # Petit test pour vérifier que ça marche
    lib = Librairie()
    lib.retirer_livre(1)  # Supprime le livre avec l'ID 1 (exemple)

# test3()

