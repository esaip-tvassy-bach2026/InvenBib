#include <iostream>
#include <sqlite3.h>
#include <string>

class Librairie {
private:
    sqlite3* db; // Pointeur vers la base de données SQLite

public:
    // Constructeur : ouvre la connexion à la base de données
    Librairie() {
        int rc = sqlite3_open("librairie.db", &db); // Ouvre ou crée la base de données
        if (rc) {
            std::cerr << "Erreur d'ouverture de la base de données : " << sqlite3_errmsg(db) << std::endl;
            return;
        }
    }

    // Destructeur : ferme la connexion à la base de données
    ~Librairie() {
        sqlite3_close(db);
    }

    // Méthode pour retirer un livre par son ID
    void retirerLivre(int id) {
        // Requête SQL paramétrée pour supprimer un livre par son ID
        std::string sql = "DELETE FROM livres WHERE id = ?;";
        sqlite3_stmt* stmt;

        // Prépare la requête SQL
        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) == SQLITE_OK) {
            // Lie l'ID du livre à supprimer
            sqlite3_bind_int(stmt, 1, id);

            // Exécute la requête et vérifie le succès
            if (sqlite3_step(stmt) != SQLITE_DONE) {
                std::cerr << "Erreur lors du retrait du livre : " << sqlite3_errmsg(db) << std::endl;
            } else {
                std::cout << "Livre retiré avec succès." << std::endl;
            }
        } else {
            std::cerr << "Erreur de préparation de la requête : " << sqlite3_errmsg(db) << std::endl;
        }

        // Libère les ressources associées à la requête
        sqlite3_finalize(stmt);
    }
};

int main() {
    Librairie lib;

    // Supprime le livre avec l'ID 1 (exemple)
    lib.retirerLivre(1);

    return 0;
}
