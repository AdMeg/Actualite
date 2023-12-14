from flask import Flask, jsonify
from flask import request
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime
from datetime import datetime

app = Flask(__name__)


def listify(vals):
    return [elem for val in vals for elem in val]

def get_db_connection():
    connex = psycopg2.connect(host="10.19.2.1", port="5432", database="projet_actu", user="actu_user", password="ValMaxMatAma")
    return connex

def execute_select(query):
    connex = psycopg2.connect(host="10.19.2.1", port="5432", database="projet_actu", user="actu_user", password="ValMaxMatAma")
    cursor = connex.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query)
    vals = cursor.fetchall()
    cursor.close()
    connex.close()
    return vals

def execute_insert(query) : 
    connex = psycopg2.connect(host="10.19.2.1", port="5432", database="projet_actu", user="actu_user", password="ValMaxMatAma")
    cursor = connex.cursor()
    try:
        cursor.execute(query)
        connex.commit()
        return 1
    except Exception as e:
        print("Une erreur est survenue:", e)
        connex.rollback()
        return 0
    finally:
        cursor.close()
        connex.close()

def execute_insert(query, mytuple) : 
    connex = psycopg2.connect(host="10.19.2.1", port="5432", database="projet_actu", user="actu_user", password="ValMaxMatAma")
    cursor = connex.cursor()
    try:
        cursor.execute(query, (mytuple,))
        connex.commit()
        return [1, "ok"]
    except Exception as e:
        print("Une erreur est survenue:", e)
        connex.rollback()
        return [0, e]
    finally:
        cursor.close()
        connex.close()

#
#   Partie Messages
#

# Récupération des 10 derniers messages  
@app.route('/get_messages', methods=['GET'])
def get_messages():

    result = execute_select('SELECT * FROM "actu", "thematique" WHERE actu.thematique_id = thematique.id ORDER BY date DESC LIMIT 10;')
    return jsonify(result)


# Récupération de tous les messages en fonction d'une date
@app.route('/get_messages_from_date', methods=['POST'])
def get_messages_from_date():

    # Verification du body du message (il doit être en JSON)
    if not request.is_json :
        return jsonify({"error": "Format du post non-JSON"}), 400

    # Exemple de JSON valide :
    # {"date" : "2023-12-04"}
    
    # Récupération du body
    data = request.json 

    # Création de la query avec les paramètres présents dans le JSON
    query = f"SELECT * FROM actu, thematique WHERE actu.thematique_id = thematique.id AND date_trunc('day', date) = '{data['date']}' ORDER BY date DESC"
    
    # Execution de la query et récupération des résultats
    result = execute_select(query)
    return jsonify(result)

@app.route('/create_message', methods=['POST'])
def create_message() : 
    # Verification du body du message (il doit être en JSON)
    if not request.is_json :
        return jsonify({"error": "Format du post non-JSON"}), 400
    else:
        data = request.json
    
    # Exemple de JSON valide :
    # {"actu" : "texte de l'actu", "thematique":"valeur_thematique"}

    thematique_id = verif_thematique_in_table(data['thematique'])
    if thematique_id != 0:
        date_time = get_timestamp()
        mytuple = (data['actu'], thematique_id, date_time)
        query = "INSERT INTO actu(contenu, thematique_id, date) VALUES %s;"
        rep = execute_insert(query, mytuple)
        if rep[0] == 1:
            return jsonify({"message": f"Actu créée avec succès: {data['actu']}, {thematique_id}, {date_time}"}), 201
        else:
            return jsonify({"message": f"Impossible de créer l'actu, requete d'insertion dans la table non correcte, {rep[1]}"}), 400
    else:
        return jsonify({"message": "Impossible de créer l'actu, thematique non reconnue"}), 400

def verif_thematique_in_table(thematique_a_verifier):
    # Verification que la thematique est bien présente dans la table thematique
    thematiques = get_thematiques_tab()
    for thematique in thematiques:
        if thematique[1] == thematique_a_verifier :
            return thematique[0]
        else:
            return 0

def get_thematiques_tab():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "thematique"')
    thematiques = cur.fetchall()
    cur.close()
    conn.close()
    return thematiques

def get_groupes_tab():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "groupe"')
    groupes = cur.fetchall()
    cur.close()
    conn.close()
    return groupes  

def get_timestamp():
    current_time = datetime.now()
    time_stamp = current_time.timestamp()
    date_time = datetime.fromtimestamp(time_stamp)
    return date_time

#
#   Partie Groupes
#

# Récupération de tous les groupes
@app.route('/get_groupes', methods=['GET'])
def get_groupes():

    result = execute_select('SELECT * FROM "groupe";')
    return jsonify(result)

# Création d'un groupe, avec le nom du groupe en JSON
@app.route('/create_groupe', methods=['POST'])
def create_groupe():

    # Verification du body du message (il doit être en JSON)
    if not request.is_json :
        return jsonify({"error": "Format du post non-JSON"}), 400
    else:
        # Récupération du body
        data = request.json
    # Exemple de JSON valide :
    # {"nom" : "NomDuGroupe"}

    # Création de la query avec les paramètres présents dans le JSON
    query = f"INSERT INTO groupe(nom) VALUES ('{data['nom']}');"
    execute_insert(query)
    return jsonify({"message": "Groupe créé avec succès"}), 201

#
#   Partie groupe_actu (table de diffusion des messages)
#

# Récupération de tous les groupe_actu
@app.route('/get_groupe_actu', methods=['GET'])
def get_groupe_actu():
    result = execute_select('SELECT * FROM "groupe_actu";')
    return jsonify(result)

# Création d'entrée dans la table groupe_actu, c'est-à-dire enregistrement d'une diffusion de message
# avec l'id du groupe et l'id du message (actu) en JSON
@app.route('/create_groupe_actu', methods=['POST'])
def create_groupe_actu():
    # Verification du body du message (il doit être en JSON)
    if not request.is_json :
        return jsonify({"error": "Format du post non-JSON"}), 400
    else:
        # Récupération du body
        data = request.json
    # Exemple de JSON valide :
    # {"actu_id" : 2, "groupes_id" : [1, 3]}
    # diffusion du message dont l'id est 2 dans la table actu
    # aux groupes dont les id sont 1 et 2 dans la table groupe
    # attention la valeur associée au champs groupes_id doit être un tableau d'entiers

    message_id = data['actu_id']
    groupes_id = data['groupes_id']
    
    nb_insert_ok = 0
    for groupe_id in groupes_id:
        # Création de la query avec les paramètres présents dans le JSON
        mytuple = (groupe_id, message_id)
        query = "INSERT INTO groupe_actu(groupe_id, actu_id) VALUES %s;"
        rep = execute_insert(query, mytuple)
        if rep[0] == 1:
            nb_insert_ok += 1
        else:
            return jsonify({"message": f"Impossible de créer la diffusion, requete d'insertion dans la table non correcte, {rep[1]}"}), 400 
    if nb_insert_ok == len(groupes_id):
        return jsonify({"message": "Les entrées dans la table groupe_actu ont été créées avec succès"}), 201
    else:
        return jsonify({"message": "Problème d'insertion des données dans la table groupe_actu"}), 400


if __name__ == '__main__':
    app.run()
