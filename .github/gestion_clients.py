class Client:
    def __init__(self, nom, prenom, adresse, age):
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.age = age

    def __str__(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Adresse: {self.adresse}, Âge: {self.age}"


class GestionClients:
    def __init__(self):
        self.clients = []

    def ajouter_client(self, nom, prenom, adresse, age):
        client = Client(nom, prenom, adresse, age)
        self.clients.append(client)
        print(f"Client ajouté : {client}")

    def supprimer_client(self, nom, prenom):
        for client in self.clients:
            if client.nom == nom and client.prenom == prenom:
                self.clients.remove(client)
                print(f"Client {nom} {prenom} supprimé.")
                return
        print("Client non trouvé.")

    def modifier_client(self, nom, prenom, nouvelle_adresse=None, nouvel_age=None):
        for client in self.clients:
            if client.nom == nom and client.prenom == prenom:
                if nouvelle_adresse:
                    client.adresse = nouvelle_adresse
                if nouvel_age:
                    client.age = nouvel_age
                print(f"Client {nom} {prenom} modifié : {client}")
                return
        print("Client non trouvé.")

    def afficher_clients(self):
        if not self.clients:
            print("Aucun client enregistré.")
        else:
            print("Liste des clients :")
            for client in self.clients:
                print(client)
