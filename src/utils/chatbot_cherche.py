import sqlite3
import random
import requests

# Remplacez par votre clé API Mistral
API_KEY = "Mu3ZznNkoOtZvoz3sB9xjubCXzsqGEwQ"

def rechercher_livre(critere, valeur):
    try:
        conn = sqlite3.connect('librairie.db')
        cursor = conn.cursor()
        if critere not in ['isbn', 'titre', 'auteur', 'annee']:
            raise ValueError("Critère invalide. Les critères valides sont : isbn, titre, auteur, annee.")
        query = f"SELECT * FROM livres WHERE {critere} LIKE ?"
        cursor.execute(query, ('%' + valeur + '%',))
        resultats = cursor.fetchall()
        conn.close()
        return resultats
    except sqlite3.Error as e:
        print(f"Erreur lors de l'accès à la base de données : {e}")
        return []
    except ValueError as ve:
        print(ve)
        return []

def ajouter_livre(isbn, titre, auteur, annee):
    try:
        conn = sqlite3.connect('librairie.db')
        cursor = conn.cursor()
        query = "INSERT INTO livres (isbn, titre, auteur, annee) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (isbn, titre, auteur, annee))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout du livre dans la base de données : {e}")
        return False

def supprimer_livre(isbn):
    try:
        conn = sqlite3.connect('librairie.db')
        cursor = conn.cursor()
        query = "DELETE FROM livres WHERE isbn = ?"
        cursor.execute(query, (isbn,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression du livre dans la base de données : {e}")
        return False

def chatbot_reponse(message, conversation_history=None):
    # Gérer l'historique de la conversation
    if conversation_history is None:
        conversation_history = []

    conversation_history.append({"role": "user", "content": message})

    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",  # Remplacez par l'URL correcte de l'API Mistral
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json; charset=utf-8"
            },
            json={
                "model": "mistral-small",  # Remplacez par le modèle Mistral souhaité
                "messages": [{"role": "system", "content": "Tu es un chatbot amical qui aide à gérer une bibliothèque. Tu réponds en français. Tu peux rechercher, ajouter et supprimer des livres de la base de données. Tu utilises les fonctions rechercher_livre, ajouter_livre et supprimer_livre.  Tu gères la conversation de manière naturelle et tu poses des questions pour mieux comprendre leurs besoins. Tu ne dois pas retourner ta réponse brute. Si l'utilisateur veut faire une recherche tu dois demander le critère (isbn, titre, auteur, annee) et la valeur. "},
                             *conversation_history],
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        response.encoding = 'utf-8'
        reponse_json = response.json()
        reponse_ia = reponse_json["choices"][0]["message"]["content"]

        conversation_history.append({"role": "assistant", "content": reponse_ia})

        return reponse_ia, conversation_history

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API Mistral : {e}")
        return "Je suis désolé, je rencontre un problème pour répondre à votre question. Veuillez réessayer plus tard.", conversation_history
    except (KeyError, IndexError) as e:
        print(f"Erreur lors de l'analyse de la réponse de l'API Mistral : {e}")
        return "Je suis désolé, il y a eu un problème avec la réponse de l'IA. Veuillez réessayer plus tard.", conversation_history

def menu_recherche_chatbot():
    print("Bienvenue dans le système de gestion de bibliothèque avec chatbot.")
    print("Je suis maintenant alimenté par l'IA Mistral et je gère les dialogues!")
    print("Je peux rechercher, ajouter et supprimer des livres.")
    print("Vous pouvez aussi discuter avec moi ou demander de l'aide.")

    conversation_history = []

    while True:
        message = input("\nQue puis-je faire pour vous? : ").strip().lower()

        if message == 'quitter':
            reponse, conversation_history = chatbot_reponse("au revoir", conversation_history)
            print(reponse)
            break

        reponse, conversation_history = chatbot_reponse(message, conversation_history)
        print(f"Chatbot: {reponse}")

        # Actions de gestion de bibliothèque basées sur la conversation
        if "ajouter" in message or "nouveau" in message:
            # Extraire les informations du livre à ajouter
            reponse_ia, conversation_history = chatbot_reponse(
                f"Extrait l'isbn, le titre, l'auteur et l'année du livre du message suivant et retourne les sous forme de dictionnaire python: {message}. Si une information n'est pas présente, retourne None.",
                conversation_history
            )

            try:
                extracted_data = eval(reponse_ia)

                isbn = extracted_data.get("isbn")
                titre = extracted_data.get("titre")
                auteur = extracted_data.get("auteur")
                annee = extracted_data.get("annee")

                if isbn and titre and auteur and annee:
                    if ajouter_livre(isbn, titre, auteur, annee):
                        print(f"Livre ajouté avec succès : ISBN {isbn}, Titre {titre}, Auteur {auteur}, Année {annee}")
                        reponse_ajout_succes, conversation_history = chatbot_reponse(f"Le livre a été ajouté avec succès.", conversation_history)
                        print(reponse_ajout_succes)
                    else:
                        print("Erreur lors de l'ajout du livre.")
                        reponse_ajout_echec, conversation_history = chatbot_reponse(f"Il y a eu une erreur lors de l'ajout du livre. Veuillez vérifier les informations.", conversation_history)
                        print(reponse_ajout_echec)
                else:
                    print("Informations incomplètes pour ajouter le livre. Veuillez fournir toutes les informations (ISBN, Titre, Auteur, Année).")
                    reponse_info_incomplete, conversation_history = chatbot_reponse(f"Les informations fournies sont incomplètes. Veuillez fournir toutes les informations (ISBN, Titre, Auteur, Année).", conversation_history)
                    print(reponse_info_incomplete)

            except (SyntaxError, NameError) as e:
                print(f"Erreur lors de l'évaluation de la réponse de l'IA : {e}")
                print(f"Réponse brute de l'IA : {reponse_ia}")
                reponse_probleme_ia, conversation_history = chatbot_reponse(f"Je n'ai pas réussi à interpréter ma réponse. Pouvez-vous reformuler?", conversation_history)
                print(reponse_probleme_ia)

        elif "supprimer" in message or "enlever" in message:
            # Extraire l'ISBN du livre à supprimer
            reponse_ia, conversation_history = chatbot_reponse(
                f"Extrait l'isbn du livre du message suivant et retourne le sous forme de dictionnaire python: {message}. Si l'isbn n'est pas présent, retourne None.",
                conversation_history
            )

            try:
                extracted_data = eval(reponse_ia)
                isbn = extracted_data.get("isbn")

                if isbn:
                    if supprimer_livre(isbn):
                        print(f"Livre avec ISBN {isbn} supprimé avec succès.")
                        reponse_suppression_succes, conversation_history = chatbot_reponse(f"Le livre a été supprimé avec succès.", conversation_history)
                        print(reponse_suppression_succes)
                    else:
                        print("Erreur lors de la suppression du livre.")
                        reponse_suppression_echec, conversation_history = chatbot_reponse(f"Il y a eu une erreur lors de la suppression du livre.", conversation_history)
                        print(reponse_suppression_echec)
                else:
                    print("ISBN manquant pour supprimer le livre. Veuillez fournir l'ISBN du livre à supprimer.")
                    reponse_isbn_manquant, conversation_history = chatbot_reponse(f"L'ISBN du livre à supprimer est manquant. Veuillez le fournir.", conversation_history)
                    print(reponse_isbn_manquant)

            except (SyntaxError, NameError) as e:
                print(f"Erreur lors de l'évaluation de la réponse de l'IA : {e}")
                print(f"Réponse brute de l'IA : {reponse_ia}")
                reponse_probleme_ia, conversation_history = chatbot_reponse(f"Je n'ai pas réussi à interpréter ma réponse. Pouvez-vous reformuler?", conversation_history)
                print(reponse_probleme_ia)
        elif "recherche" in message or "cherche" in message or "livre" in message:
             reponse_ia, conversation_history = chatbot_reponse(
                f"Quel est le critère de recherche (isbn, titre, auteur, annee) et la valeur?",
                conversation_history
             )

        elif "isbn" in message or "titre" in message or "auteur" in message or "annee" in message:
            critere = input("Entrez le critère de recherche (isbn, titre, auteur, annee) : ").strip().lower()
            if critere not in ['isbn', 'titre', 'auteur', 'annee']:
                print("Critère invalide. Veuillez réessayer.")
                continue

            valeur = input(f"Entrez la valeur à rechercher pour le critère '{critere}' : ").strip()
            livres_trouves = rechercher_livre(critere, valeur)

            if livres_trouves:
                print(f"\nLivres trouvés pour {critere} contenant '{valeur}' :")
                for livre in livres_trouves:
                    print(f"ISBN: {livre[0]}, Titre: {livre[1]}, Auteur: {livre[2]}, Année: {livre[3]}")
            else:
                print(f"\nAucun livre trouvé pour {critere} contenant '{valeur}'.")

if __name__ == "__main__":
    menu_recherche_chatbot()
