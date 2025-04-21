import sqlite3
import requests

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
                VALUES (?, ?, ?, ?)
            """, (isbn, titre, auteur, annee))
            self.conn.commit()
            print("Livre ajouté avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du livre : {e}")
            return False
        return True

    def rechercher_livre(self, critere, valeur):
        """Recherche un livre dans la base de données en fonction du critère et de la valeur fournie."""
        try:
            if critere not in ['isbn', 'titre', 'auteur', 'annee']:
                raise ValueError("Critère invalide. Les critères valides sont : isbn, titre, auteur, annee.")
            query = f"SELECT * FROM livres WHERE {critere} LIKE ?"
            self.cursor.execute(query, ('%' + valeur + '%',))
            resultats = self.cursor.fetchall()
            return resultats
        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données : {e}")
            return []
        except ValueError as ve:
            print(ve)
            return []

# Remplacez par votre clé API Mistral
API_KEY = "Mu3ZznNkoOtZvoz3sB9xjubCXzsqGEwQ"

def ajouter_livre_avec_mistral(librairie, message):
    """Utilise Mistral pour extraire les informations du livre du message et l'ajoute."""
    try:
        # Utiliser Mistral pour extraire les informations du livre
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json; charset=utf-8"
            },
            json={
                "model": "mistral-small",
                "messages": [{"role": "user", "content": f"Extrait l'isbn, le titre, l'auteur et l'année du livre du message suivant et retourne les sous forme de dictionnaire python: {message}. Si une information n'est pas présente, retourne None."}],
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        response.encoding = 'utf-8'
        reponse_json = response.json()
        reponse_ia = reponse_json["choices"][0]["message"]["content"]
        
        # Évaluer la réponse de l'IA pour extraire les informations
        extracted_data = eval(reponse_ia)
        isbn = extracted_data.get("isbn")
        titre = extracted_data.get("titre")
        auteur = extracted_data.get("auteur")
        annee = extracted_data.get("annee")

        # Ajouter le livre à la base de données
        if isbn and titre and auteur and annee:
            if librairie.ajouter_livre(isbn, titre, auteur, annee):
                return f"Livre ajouté avec succès : ISBN {isbn}, Titre {titre}, Auteur {auteur}, Année {annee}"
            else:
                return "Erreur lors de l'ajout du livre."
        else:
            return "Informations incomplètes pour ajouter le livre. Veuillez fournir toutes les informations (ISBN, Titre, Auteur, Année)."

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la requête à l'API Mistral : {e}"
    except (KeyError, SyntaxError, NameError) as e:
        return f"Erreur lors de l'interprétation de la réponse de l'IA : {e}. Réponse brute : {reponse_ia}"

# Exemple d'utilisation avec Mistral
def test_ajout_mistral():
    lib = Librairie()
    message_ajout = "Ajoute le livre avec l'isbn 1234567890, le titre est 'Le Seigneur des Anneaux', l'auteur est J.R.R. Tolkien et l'année est 1954."
    resultat = ajouter_livre_avec_mistral(lib, message_ajout)
    print(resultat)

# test_ajout_mistral()
