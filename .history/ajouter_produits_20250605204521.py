
from flask import Flask
from flask_mysqldb import MySQL

# --- Configuration Flask & MySQL ---
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'  # 🔁 remplace ici
app.config['MYSQL_DB'] = 'digit_school_store'         # 🔁 remplace ici

mysql = MySQL(app)

# --- Insertion des produits ---
with app.app_context():
    try:
        cursor = mysql.connection.cursor()

        # Liste de produits à insérer
        produits = [
            ("Stylo Bleu", "Stylo à bille bleu de qualité", 1.50, 100, "cas.jpg"),
            ("Cahier A4", "Cahier 100 pages, format A4", 2.00, 50, "mode1.jpg"),
            ("Gomme Blanche", "Gomme blanche douce", 0.75, 200, "mathe.jpg"),
            ("Crayon HB", "Crayon en bois mine HB", 0.60, 120, "mode2.jpg"),
            ("Trousse Scolaire", "Trousse en tissu multicolore", 3.90, 45, "mode3.jpg"),
            ("Règle 30cm", "Règle en plastique transparente", 0.90, 80, "sac.jpg"),
        ]

        # Insertion dans la table
        cursor.executemany("""
            INSERT INTO produits (nom, description, prix, stock, image)
            VALUES (%s, %s, %s, %s, %s)
        """, produits)

        mysql.connection.commit()
        cursor.close()
        print("✅ Produits ajoutés avec succès !")

    except Exception as e:
        print("❌ Erreur lors de l'insertion :", e)
