
import mysql.connector

# Connexion MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',  # remplace par ton mot de passe
    database='digit_school_store'  # remplace par le nom de ta base de données
)

cursor = conn.cursor()

# Liste des produits avec stock
produits = [
    ("Calculatrice scolaire", 3000, "Calculatrice simple et robuste pour les cours", "sac.jpg", 20),
    ("Sac à dos éducatif", 12000, "Sac solide avec compartiments pour matériel scolaire", "ordi.jpg", 15),
    ("Kit géométrie", 1500, "Contient règle, compas, équerre et rapporteur", "store.jpg", 30),
    ("Cahier intelligent", 2500, "Cahier connecté pour la prise de notes numérique", "store2.jpg", 25),
    ("Tablette éducative", 45000, "Parfaite pour les apprentissages numériques", "tablette.jpg", 10),
    ("Stylo intelligent", 1500, "Stylo connecté pour élèves", "mont.jpg", 50)
]

# Requête SQL avec le champ stock
sql = "INSERT INTO produits (nom, prix, description, image, stock) VALUES (%s, %s, %s, %s, %s)"

try:
    cursor.executemany(sql, produits)
    conn.commit()
    print(f"{cursor.rowcount} produit(s) ajouté(s) avec succès.")
except Exception as e:
    print("Erreur lors de l'insertion :", e)
    conn.rollback()

# Fermeture
cursor.close()
conn.close()
