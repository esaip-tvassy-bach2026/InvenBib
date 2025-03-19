#include <iostream>
#include <sqlite3.h>
#include <string>

class Librairie {
private:
    sqlite3* db; // Pointeur vers la base de données SQLite

public:
    // Constructeur : ouvre la connexion à la base de données et crée la table si elle n'existe pas
    Librairie() {
        int rc = sqlite3_open("librairie.db", &db); // Ouvre ou crée la base de données
        if (rc) {
            std::cerr << "Erreur d'ouverture de la base de données : " << sqlite3_errmsg(db) << std::endl;
            return;
        }

        // Crée une table "livres" si elle n'existe pas déjà
        const char* sql = "CREATE TABLE IF NOT EXISTS livres ("
                          "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "titre TEXT NOT NULL,"
                          "auteur TEXT NOT NULL,"
                          "annee INTEGER);";
        
        char* errMsg = nullptr;
        rc = sqlite3_exec(db, sql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::cerr << "Erreur SQL : " << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
    }

    // Destructeur : ferme la connexion à la base de données
    ~Librairie() {
        sqlite3_close(db);
    }

    // Méthode pour ajouter un livre dans la base de données
    void ajouterLivre(const std::string& titre, const std::string& auteur, int annee) {
        // Requête SQL paramétrée pour insérer un nouveau livre
        std::string sql = "INSERT INTO livres (titre, auteur, annee) VALUES (?, ?, ?);";
        sqlite3_stmt* stmt;

        // Prépare la requête SQL
        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) == SQLITE_OK) {
            // Lie les valeurs des paramètres à la requête SQL
            sqlite3_bind_text(stmt, 1, titre.c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_text(stmt, 2, auteur.c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_int(stmt, 3, annee);

            // Exécute la requête et vérifie le succès
            if (sqlite3_step(stmt) != SQLITE_DONE) {
                std::cerr << "Erreur lors de l'ajout du livre : " << sqlite3_errmsg(db) << std::endl;
            } else {
                std::cout << "Livre ajouté avec succès." << std::endl;
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

    // Ajoute deux livres à la base de données
    lib.ajouterLivre("1984", "George Orwell", 1949);
    lib.ajouterLivre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943);

    return 0;
}
