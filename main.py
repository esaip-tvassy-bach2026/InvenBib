from gestion_clients import GestionClients

def afficher_menu():
    print("\n=== Menu de Gestion des Clients ===")
    print("1. Ajouter un client")
    print("2. Supprimer un client")
    print("3. Modifier un client")
    print("4. Afficher tous les clients")
    print("5. Quitter\n")

def main():
    gestion_clients = GestionClients()

    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == '1':
            nom = input("Nom du client : ")
            prenom = input("Prénom du client : ")
            adresse = input("Adresse du client : ")
            age = int(input("Âge du client : "))
            gestion_clients.ajouter_client(nom, prenom, adresse, age)

        elif choix == '2':
            nom = input("Nom du client à supprimer : ")
            prenom = input("Prénom du client à supprimer : ")
            gestion_clients.supprimer_client(nom, prenom)

        elif choix == '3':
            nom = input("Nom du client à modifier : ")
            prenom = input("Prénom du client à modifier : ")
            nouvelle_adresse = input("Nouvelle adresse (laisser vide pour ne pas modifier) : ")
            nouvel_age = input("Nouvel âge (laisser vide pour ne pas modifier) : ")
            nouvel_age = int(nouvel_age) if nouvel_age else None
            gestion_clients.modifier_client(nom, prenom, nouvelle_adresse, nouvel_age)

        elif choix == '4':
            gestion_clients.afficher_clients()

        elif choix == '5':
            print("Au revoir !")
            break

        else:
            print("Choix non valide, veuillez réessayer.")

if __name__ == "__main__":
    main()
