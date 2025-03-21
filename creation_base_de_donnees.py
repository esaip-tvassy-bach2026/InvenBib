import sqlite3

# Connexion à la base de données (cela crée la base si elle n'existe pas)
conn = sqlite3.connect('librairie.db')
cursor = conn.cursor()

# Création de la table (si elle n'existe pas déjà)
cursor.execute('''
CREATE TABLE IF NOT EXISTS livres (
    isbn INTEGER PRIMARY KEY,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    annee INTEGER
);
''')

# Liste de livres réels, avec des titres, auteurs et années de publication
livres_reels = [
    (9780451524935, '1984', 'George Orwell', 1949),
    (9780316769174, 'The Catcher in the Rye', 'J.D. Salinger', 1951),
    (9780446310789, 'To Kill a Mockingbird', 'Harper Lee', 1960),
    (9781451673319, 'Fahrenheit 451', 'Ray Bradbury', 1953),
    (9780743273565, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925),
    (9780060850524, 'Brave New World', 'Aldous Huxley', 1932),
    (9780307474278, 'The Da Vinci Code', 'Dan Brown', 2003),
    (9780547928227, 'The Hobbit', 'J.R.R. Tolkien', 1937),
    (9780141439518, 'Pride and Prejudice', 'Jane Austen', 1813),
    (9780385490818, 'The Handmaid\'s Tale', 'Margaret Atwood', 1985),
    (9780307743657, 'The Shining', 'Stephen King', 1977),
    (9780307387899, 'The Road', 'Cormac McCarthy', 2006),
    (9780198800538, 'Anna Karenina', 'Leo Tolstoy', 1877),
    (9780142437247, 'Moby-Dick', 'Herman Melville', 1851),
    (9781400079988, 'War and Peace', 'Leo Tolstoy', 1869),
    (9780141441146, 'Jane Eyre', 'Charlotte Brontë', 1847),
    (9780141439570, 'The Picture of Dorian Gray', 'Oscar Wilde', 1890),
    (9780140177398, 'The Grapes of Wrath', 'John Steinbeck', 1939),
    (9780141439846, 'Dracula', 'Bram Stoker', 1897),
    (9780374528379, 'The Brothers Karamazov', 'Fyodor Dostoevsky', 1880),
]

# 21 livres supplémentaires
livres_supplementaires = [
    (9780062315007, 'The Alchemist', 'Paulo Coelho', 1988),
    (9780439023481, 'The Hunger Games', 'Suzanne Collins', 2008),
    (9781594634024, 'The Girl on the Train', 'Paula Hawkins', 2015),
    (9780307588371, 'Gone Girl', 'Gillian Flynn', 2012),
    (9780425232200, 'The Help', 'Kathryn Stockett', 2009),
    (9780142424179, 'The Fault in Our Stars', 'John Green', 2012),
    (9781594631931, 'The Kite Runner', 'Khaled Hosseini', 2003),
    (9781565125605, 'Water for Elephants', 'Sara Gruen', 2006),
    (9780399167065, 'Big Little Lies', 'Liane Moriarty', 2014),
    (9780307744432, 'The Night Circus', 'Erin Morgenstern', 2011),
    (9780399590504, 'Educated', 'Tara Westover', 2018),
    (9780735219090, 'Where the Crawdads Sing', 'Delia Owens', 2018),
    (9780316556347, 'Circe', 'Madeline Miller', 2018),
    (9780064401883, 'The Secret Garden', 'Frances Hodgson Burnett', 1911),
    (9780140444308, 'Les Misérables', 'Victor Hugo', 1862),
    (9780062316110, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 2011),
    (9780375842207, 'The Book Thief', 'Markus Zusak', 2005),
    (9780316044400, 'The Lovely Bones', 'Alice Sebold', 2002),
    (9780062797155, 'The Tattooist of Auschwitz', 'Heather Morris', 2018),
    (9780735212756, 'The Light We Lost', 'Jill Santopolo', 2017),
    (9781476738024, 'A Man Called Ove', 'Fredrik Backman', 2012),
]

# Combinaison des livres réels et des livres supplémentaires
livres_data = livres_reels + livres_supplementaires

# Récupérer tous les ISBN déjà présents dans la base de données
cursor.execute('SELECT isbn FROM livres')
existing_isbns = cursor.fetchall()
existing_isbns = {isbn[0] for isbn in existing_isbns}  # Utiliser un set pour la recherche rapide

# Filtrer les livres pour ne garder que ceux avec des ISBN non présents dans la base
livres_data_unique = [livre for livre in livres_data if livre[0] not in existing_isbns]

# Insertion des livres non-doublons dans la base
cursor.executemany('''
INSERT INTO livres (isbn, titre, auteur, annee)
VALUES (?, ?, ?, ?)
''', livres_data_unique)

# Sauvegarde des modifications
conn.commit()

# Exemple de requête : sélectionner tous les livres
cursor.execute('SELECT * FROM livres')
livres = cursor.fetchall()

# Affichage des livres (affichage limité aux 10 premiers pour ne pas surcharger la sortie)
for livre in livres[:10]:  # Affiche seulement les 10 premiers livres
    print(f'ISBN: {livre[0]}, Titre: {livre[1]}, Auteur: {livre[2]}, Année: {livre[3]}')

# Fermeture de la connexion
conn.close()
