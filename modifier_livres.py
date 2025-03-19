#include <iostream>
#include <sqlite3.h>
#include <string>

class Librairie {
private:
    sqlite3* db; // Pointeur vers la base de données SQLite

public:
    // Constructeur : ouvre la connexion à SQLite
    Librairie() {
        int rc = sqlite3_open("librairie.db", &db); 
        if (rc) {
            std::cerr << "Erreur d'ouverture de la base de données : " << sqlite3_errmsg(db) << std::endl;
            return;
        }
    }

    // Destructeur : ferme proprement SQLite
    ~Librairie() {
        sqlite3_close(db);
    }

    // Méthode pour modifier un livre existant par son ID
    void modifierLivre(int id, const std::string& nouveauTitre, const std::string& nouvelAuteur, int nouvelleAnnee) {
        // Requête SQL paramétrée pour mettre à jour les informations d'un livre par ID
        std::string sql = "UPDATE livres SET titre = ?, auteur = ?, annee = ? WHERE id = ?;";
        sqlite3_stmt* stmt;

        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) == SQLITE_OK) {
            // Lie les nouveaux paramètres au livre correspondant à l'ID donné
            sqlite3_bind_text(stmt, 1, nouveauTitre.c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_text(stmt, 2, nouvelAuteur.c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_int(stmt, 3, nouvelleAnnee);
            sqlite3_bind_int(stmt, 4, id);

            if (sqlite3_step(stmt) != SQLITE_DONE) {
                std::cerr << "Erreur lors de la modification du livre : " << sqlite3_errmsg(db) << std::endl;
            } else {
                std::cout << "Livre modifié avec succès." << std::endl;
            }
        } else {
            std::cerr << "Erreur lors de préparation de la requête : " << sqlite3_errmsg(db) << std::endl;
        }

        // Libère les ressources associées à cette requête SQL
        sqlite3_finalize(stmt);
    }
};

int main() {
    Librairie lib;

    // Modifie le livre ayant l'ID 1 avec un nouveau titre et auteur
    lib.modifierLivre(1, "Animal Farm", "George Orwell", 1945);

    return 0;
}
