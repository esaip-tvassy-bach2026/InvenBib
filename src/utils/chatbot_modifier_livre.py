import sqlite3
import requests

class Librairie:
    def __init__(self):
        try:
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
        except sqlite3.Error as e:
            print(f"Erreur d'ouverture de la base de données : {e}")
            self.conn = None  # Empêcher l'utilisation d'une connexion invalide

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def modifier_livre(self, isbn, nouveau_titre, nouvel_auteur, nouvelle_annee):
        if not self.conn:
            print("La base de données n'est pas ouverte.")
            return False

        sql = "UPDATE livres SET titre = ?, auteur = ?, annee = ? WHERE isbn = ?"
        try:
            self.cursor.execute(sql, (nouveau_titre, nouvel_auteur, nouvelle_annee, isbn))
            self.conn.commit()
            print("Livre modifié avec succès.")
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la modification du livre : {e}")
            return False

# Remplacez par votre clé API Mistral
API_KEY = "YOUR_MISTRAL_API_KEY"

def modifier_livre_avec_mistral(librairie, message):
    """Utilise Mistral pour extraire les informations du livre du message et le modifie."""
    if not librairie.conn:
        return "La base de données n'est pas ouverte."

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
                "messages": [{"role": "user", "content": f"Extrait l'isbn, le nouveau titre, le nouvel auteur et la nouvelle année du livre du message suivant et retourne les sous forme de dictionnaire python: {message}. Si une information n'est pas présente, retourne None."}],
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
        nouveau_titre = extracted_data.get("titre")
        nouvel_auteur = extracted_data.get("auteur")
        nouvelle_annee = extracted_data.get("annee")

        # Modifier le livre dans la base de données
        if isbn and nouveau_titre and nouvel_auteur and nouvelle_annee:
            if librairie.modifier_livre(isbn, nouveau_titre, nouvel_auteur, nouvelle_annee):
                return f"Livre modifié avec succès : ISBN {isbn}, Nouveau Titre {nouveau_titre}, Nouvel Auteur {nouvel_auteur}, Nouvelle Année {nouvelle_annee}"
            else:
                return "Erreur lors de la modification du livre."
        else:
            return "Informations incomplètes pour modifier le livre. Veuillez fournir toutes les informations (ISBN, Titre, Auteur, Année)."

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la requête à l'API Mistral : {e}"
    except (KeyError, SyntaxError, NameError) as e:
        return f"Erreur lors de l'interprétation de la réponse de l'IA : {e}. Réponse brute : {reponse_ia}"

# Exemple d'utilisation avec Mistral
def test_modifier_mistral():
    lib = Librairie()
    message_modification = "Modifie le livre avec l'isbn 1234567890, le nouveau titre est 'The Fellowship of the Ring', le nouvel auteur est J.R.R. Tolkien et la nouvelle année est 1954."
    resultat = modifier_livre_avec_mistral(lib, message_modification)
    print(resultat)

# test_modifier_mistral()
