
import json
import MySQLdb

# Connexion à la base de données
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="12345",  # change selon ton mot de passe
    db="digit_school_store",
    charset="utf8mb4"
)

cursor = db.cursor()

# Liste de produits à ajouter
produits = [
    {
        "nom": "Sac scolaire",
        "description": "Sac à dos résistant pour élèves avec plusieurs compartiments.",
        "prix": 10000,
        "categorie": "accessoire",
        "stock": 15,
        "images": json.dumps(["sac1.jpg", "sac2.jpg", "sac3.jpg"])
    },
    {
        "nom": "Chaussures Mode1",
        "description": "Chaussures tendance pour l’école ou les sorties.",
        "prix": 12000,
        "categorie": "mode",
        "stock": 10,
        "images": json.dumps(["mode1_1.jpg", "mode1_2.jpg", "mode1_3.jpg"])
    },
    {
        "nom": "Store1 Scolaire",
        "description": "Rideaux store pour salle d’étude ou chambre d’enfant.",
        "prix": 8000,
        "categorie": "accessoire",
        "stock": 20,
        "images": json.dumps(["store1_1.jpg", "store1_2.jpg", "store1_3.jpg"])
    },
    {
        "nom": "EDUCA Pack 1",
        "description": "Pack éducatif complet avec cahiers, stylos, règles.",
        "prix": 5000,
        "categorie": "educatif",
        "stock": 30,
        "images": json.dumps(["educa1.jpg", "educa2.jpg", "educa3.jpg"])
    },
    {
        "nom": "EDUCA Pack 3",
        "description": "Set pour les élèves de niveau avancé avec matériel scientifique.",
        "prix": 15000,
        "categorie": "educatif",
        "stock": 25,
        "images": json.dumps(["educa3_1.jpg", "educa3_2.jpg", "educa3_3.jpg"])
    },
    {
        "nom": "Ordinateur scolaire",
        "description": "Ordinateur portable adapté pour les élèves et étudiants.",
        "prix": 250000,
        "categorie": "technologie",
        "stock": 5,
        "images": json.dumps(["ordi1.jpg", "ordi2.jpg", "ordi3.jpg"])
    }
]

try:
    for produit in produits:
        cursor.execute("""
            INSERT INTO produits (nom, description, prix, categorie, stock, images)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            produit["nom"],
            produit["description"],
            produit["prix"],
            produit["categorie"],
            produit["stock"],
            produit["images"]
        ))
    
    db.commit()
    print("✅ Tous les produits ont été ajoutés avec succès !")

except Exception as e:
    print("❌ Erreur :", e)
    db.rollback()

finally:
    cursor.close()
    db.close()
