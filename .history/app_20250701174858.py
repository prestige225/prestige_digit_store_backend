



from flask import Flask, request, jsonify, session, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors
import json  # 👈 utile pour encoder les produits en JSON

from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'secret123'  # Clé secrète pour la session
CORS(app, supports_credentials=True)

# Configuration MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'digit_school_store'

mysql = MySQL(app)

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'afanouemile6@gmail.com'      # Remplace par ton email
app.config['MAIL_PASSWORD'] = 'keranowzgsywovcb'         # Remplace par ton mot de passe ou un mot de passe d’application

mail = Mail(app)

# 🌐 Page HTML
@app.route('/')
def index():
    return render_template('index.html')


# Route d'inscription
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'message': 'Cet email est déjà utilisé'}), 409

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )
    mysql.connection.commit()

    return jsonify({'message': 'Inscription réussie !'}), 201



# rout pour supprimer un utilisateur

@app.route('/api/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email requis'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Vérifier si l'utilisateur existe
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

    # Supprimer l'utilisateur
    cursor.execute("DELETE FROM users WHERE email = %s", (email,))
    mysql.connection.commit()

    return jsonify({'message': f"Utilisateur avec l'email {email} supprimé"}), 200



# Route de connexion
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET is_online = TRUE WHERE id = %s", (user['id'],))
        mysql.connection.commit()

        session['user_id'] = user['id']
        session['email'] = user['email']
        session['name'] = user['name']
        return jsonify({'message': 'Connexion réussie', 'user': {'email': user['email'], 'name': user['name']}})
    else:
        return jsonify({'message': 'Email ou mot de passe incorrect'}), 401




@app.route('/api/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return jsonify({'message': 'Non connecté'}), 401

    user_id = session['user_id']

    try:
        cursor = mysql.connection.cursor()

        # Récupérer les commandes de l'utilisateur
        cursor.execute("""
            SELECT id, produits, total, date_commande, statut
            FROM commande
            WHERE user_id = %s
            ORDER BY date_commande DESC
        """, (user_id,))
        commandes = cursor.fetchall()

        commandes_list = []
        for row in commandes:
            commandes_list.append({
                'id': row[0],
                'produits': row[1],  # JSON brut
                'total': float(row[2]),
                'date': row[3].strftime('%Y-%m-%d %H:%M'),
                'statut': row[4]
            })

        return jsonify({
            'user': {
                'email': session.get('email'),
                'name': session.get('name')
            },
            'commandes': commandes_list
        })

    except Exception as e:
        print("Erreur serveur :", e)
        return jsonify({'message': 'Erreur serveur'}), 500

        
# Route déconnexion
@app.route('/api/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET is_online = FALSE WHERE id = %s", (user_id,))
        mysql.connection.commit()

    session.clear()
    return jsonify({'message': 'Déconnexion réussie'}), 200


# Route pour les utilisateurs en ligne
@app.route('/api/online-users', methods=['GET'])
def online_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, name, email FROM users WHERE is_online = TRUE")
    users_online = cursor.fetchall()
    return jsonify({'online_users': users_online})


# Tous les utilisateurs
@app.route('/api/users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, name, email, is_online FROM users")
    users = cursor.fetchall()
    return jsonify({'users': users})


# Utilisateurs connectés
@app.route('/api/users/connected', methods=['GET'])
def get_connected_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, name, email FROM users WHERE is_online = TRUE")
    users_online = cursor.fetchall()
    return jsonify({'connected_users': users_online})


# Import des modules nécessaires

from flask import jsonify, request
import json
import MySQLdb.cursors

# 🛒 Route pour passer une commande





from flask import request, jsonify, session
import json




@app.route('/api/commander', methods=['POST'])
def commander():
    if 'user_id' not in session:
        return jsonify({'message': 'Non autorisé'}), 401

    data = request.get_json()
    print("👉 Données reçues :", data)

    produits = data.get('produits')
    total = float(data.get('total'))  # montant total sans réduction
    reduction_percent = float(data.get('reduction_percent', 0))  # réduction appliquée, ex: 10 pour 10%
    nom = data.get('client_nom')
    email = data.get('client_email')
    telephone = data.get('client_telephone')
    methode_paiement = data.get('methode_paiement')
    adresse = data.get('client_adress_de_livraison')
    user_id = session['user_id']

    if not produits or not nom or total is None:
        return jsonify({'message': 'Données incomplètes'}), 400

    try:
        # 🔄 Reformatage des produits
        produits_formates = []
        for p in produits:
            produits_formates.append({
                "nom": p.get("nom") or p.get("name"),
                "quantite": p.get("quantite") or p.get("quantity"),
                "prix": p.get("prix") or p.get("price")
            })

        # 🧮 Calcul du total avec réduction
        montant_reduction = (reduction_percent / 100) * total
        total_apres_reduction = round(total - montant_reduction, 2)

        # 📥 Insertion dans la base de données
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO commande (
                produits, total, reduction_percent, total_apres_reduction,
                client_nom, client_email, client_telephone, methode_paiement,
                client_adress_de_livraison, user_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            json.dumps(produits_formates), total,
            reduction_percent, total_apres_reduction,
            nom, email, telephone, methode_paiement,
            adresse, user_id
        ))

        mysql.connection.commit()
        print("✅ Commande enregistrée avec réduction :", total_apres_reduction)

        return jsonify({
            'message': 'Commande enregistrée avec succès',
            'total_avant_reduction': total,
            'reduction': f"{reduction_percent}%",
            'total_apres_reduction': total_apres_reduction
        }), 201

    except Exception as e:
        print("❌ Erreur lors de l’enregistrement :", e)
        return jsonify({'message': 'Erreur serveur'}), 500

# 📦 Route admin pour consulter les commandes
@app.route('/api/admin/commandes')
def api_commandes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM commande ORDER BY date_commande DESC")
    commandes = cursor.fetchall()

    commandes_list = []
    for c in commandes:
        commandes_list.append({
            'id': c['id'],
            'produits': json.loads(c['produits']),
            'total': c['total'],
            'client_nom': c.get('client_nom', 'Inconnu'),
            'client_email': c.get('client_email', 'Non renseigné'),
            'client_telephone': c.get('client_telephone', 'Non renseigné'),
            'client_adresse': c.get('client_adress_de_livraison', 'Non renseignée'),  # ✅ clé ajoutée ici
            'methode_paiement': c.get('methode_paiement', 'Non renseignée'),
            'statut': c.get('statut', 'En attente'),
            'date_commande': c['date_commande'].strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(commandes_list)

# 📦 Route admin pour consulter une commande spécifique

@app.route('/api/admin/commande/<int:commande_id>/statut', methods=['PUT'])
def update_statut_commande(commande_id):
    data = request.get_json()
    nouveau_statut = data.get('statut')

    # Liste des statuts possibles
    statuts_valides = ['en attente', 'en préparation', 'en livraison', 'livrée', 'annulée']

    if nouveau_statut not in statuts_valides:
        return jsonify({'message': 'Statut invalide'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE commande SET statut = %s WHERE id = %s", (nouveau_statut, commande_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': f'Statut de la commande {commande_id} mis à jour à "{nouveau_statut}"'})


@app.route('/api/admin/commande/<int:id>', methods=['DELETE'])
def supprimer_commande(id):
    try:
        cursor = mysql.connection.cursor()

        # Vérifie si la commande existe
        cursor.execute("SELECT * FROM commande WHERE id = %s", (id,))
        commande = cursor.fetchone()

        if not commande:
            return jsonify({"message": "Commande non trouvée"}), 404

        # Supprime la commande
        cursor.execute("DELETE FROM commande WHERE id = %s", (id,))
        mysql.connection.commit()

        return jsonify({"message": f"Commande {id} supprimée avec succès"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()


# route pour suivre une commande
# Cette route permet à un utilisateur de suivre l'état de sa commande en fournissant l'ID de la commande.

# ✅ Route pour suivre une commande par ID
@app.route("/api/track/<int:order_id>", methods=["GET"])
def track_order(order_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT id, statut, client_nom, client_email, client_telephone, 
                   client_adress_de_livraison, date_commande 
            FROM commande 
            WHERE id = %s
        """
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            # Convertir date_commande au format lisible
            result['date_commande'] = result['date_commande'].strftime('%Y-%m-%d %H:%M')
            return jsonify(result)
        else:
            return jsonify({"message": "Commande non trouvée"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500






# MESSAGE ENVOYER PAS UTLISATEUR
@app.route('/api/messages', methods=['POST'])
def receive_message():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'message': 'Champs manquants'}), 400

    cursor = mysql.connection.cursor()
    try:
        # Enregistrer dans la BDD
        cursor.execute("""
            INSERT INTO contacts (name, email, message, sender, created_at, status)
            VALUES (%s, %s, %s, 'user', NOW(), 'unread')
        """, (name, email, message))
        mysql.connection.commit()

        # ➤ Envoi de l'email à l'admin
        try:
            msg = Message(
                subject=f"Nouveau message de {name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=['afanouemile6@gmail.com']
            )
            msg.body = f"Nom : {name}\nEmail : {email}\n\nMessage :\n{message}"
            mail.send(msg)
        except Exception as e:
            print("❌ Erreur lors de l'envoi d'email à l'admin :", e)

        return jsonify({'message': 'Message reçu, merci !'}), 201

    except Exception as e:
        print("❌ Erreur insertion message :", e)
        return jsonify({'message': 'Erreur serveur'}), 500

    finally:
        cursor.close()



# message reçu 

@app.route('/api/messages', methods=['GET'])
def get_all_messages():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            SELECT id, name, email, message, sender, created_at, status, response, responded_at 
            FROM contacts
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        messages = [dict(zip(column_names, row)) for row in rows]
        return jsonify(messages), 200
    except Exception as e:
        print("Erreur récupération messages :", e)
        return jsonify({'message': 'Erreur serveur'}), 500
    finally:
        cursor.close()

from flask import request, jsonify
from datetime import datetime



from datetime import datetime
from flask import request, jsonify

@app.route('/api/messages/<int:id>/reply', methods=['POST'])
def reply_to_message(id):
    data = request.get_json()
    reply = data.get('reply')

    if not reply:
        return jsonify({'message': 'Réponse manquante'}), 400

    try:
        cursor = mysql.connection.cursor()

        # Vérifier que le message existe dans 'contacts'
        cursor.execute("SELECT email, name FROM contacts WHERE id = %s", (id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'Message non trouvé'}), 404

        email, name = user

        # Mettre à jour la réponse
        cursor.execute("""
            UPDATE contacts
            SET response = %s, responded_at = %s, status = 'read'
            WHERE id = %s
        """, (reply, datetime.now(), id))
        mysql.connection.commit()

        cursor.close()

        # Facultatif : envoyer un mail ici si besoin

        return jsonify({'message': 'Réponse enregistrée avec succès'}), 200

    except Exception as e:
        print("Erreur lors de la réponse :", e)
        return jsonify({'message': 'Erreur serveur'}), 500


@app.route('/api/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
        mysql.connection.commit()
        return jsonify({'message': 'Message supprimé'}), 200
    except Exception as e:
        print("Erreur suppression message :", e)
        return jsonify({'message': 'Erreur serveur'}), 500
    finally:
        cursor.close()



# route envoyez message par admin




@app.route('/api/messages/send', methods=['POST'])
def send_message():
    data = request.get_json()

    name = data.get('name', 'Admin')  # Valeur par défaut : "Admin"
    email = data.get('email')         # Email du destinataire
    message = data.get('message')     # Contenu du message
    sender = data.get('sender', 'admin')  # Par défaut "admin"

    # Vérification des champs obligatoires
    if not email or not message:
        return jsonify({'success': False, 'message': 'Champs manquants'}), 400

    try:
        cursor = mysql.connection.cursor()

        # ➤ Enregistrement dans la base de données
        cursor.execute("""
            INSERT INTO contacts (name, email, message, sender, created_at, status)
            VALUES (%s, %s, %s, %s, NOW(), 'unread')
        """, (name, email, message, sender))
        mysql.connection.commit()
        cursor.close()

        # ➤ Affiche l'email cible pour vérification
        print("➡️ Envoi de l'email à :", email)

        # ➤ Envoi de l'email avec version texte + HTML
        msg = Message(
            subject="Message de l'équipe Prestige Digit School",
            recipients=[email],
            sender=app.config.get('MAIL_DEFAULT_SENDER') or app.config['MAIL_USERNAME']
        )
        msg.body = f"""Bonjour,

Vous avez reçu un message de l'administration :

{message}

Cordialement,
L'équipe Prestige Digit School
"""

        msg.html = f"""
        <p>Bonjour,</p>
        <p>Vous avez reçu un message de l'administration :</p>
        <blockquote style="color:#333;background:#f9f9f9;padding:10px;border-left:4px solid #007BFF;">
            {message}
        </blockquote>
        <p>Cordialement,<br>L'équipe Prestige Digit School</p>
        """

        # ➤ Envoi du mail
        try:
            mail.send(msg)
            print("✅ Email envoyé avec succès")
        except Exception as e:
            print("❌ Erreur lors de l'envoi de l'email :", e)

        return jsonify({'success': True, 'message': 'Message envoyé avec succès.'}), 200

    except Exception as e:
        print("❌ Erreur lors de l'enregistrement ou de l'envoi :", e)
        return jsonify({'success': False, 'message': 'Erreur interne du serveur'}), 500




# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)
