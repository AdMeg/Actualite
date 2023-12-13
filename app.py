from flask import Flask, jsonify
from flask import request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def listify(vals):
    return [elem for val in vals for elem in val]


def execute_query(query):
    connex = psycopg2.connect(host="10.19.2.1", port="5432", database="projet_actu", user="actu_user", password="ValMaxMatAma")
    cursor = connex.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query)
    vals = cursor.fetchall()
    cursor.close()
    connex.close()
    return vals


def execute_insert(query, params):
    connex = psycopg2.connect(host="10.19.2.1", port="5432", database="projet_actu", user="actu_user", password="ValMaxMatAma")
    cursor = connex.cursor()
    try:
        cursor.execute(query, params)
        connex.commit()
    except Exception as e:
        print("Une erreur est survenue:", e)
        connex.rollback()
    finally:
        cursor.close()
        connex.close()


@app.route('/groupe', methods=['GET'])
def get_groupe():
    result = execute_query('SELECT * FROM "groupe";')
    return jsonify(result)


@app.route('/actu', methods=['GET'])
def get_actu():
    result = execute_query('SELECT * FROM "actu", "thematique" WHERE actu.thematique_id = thematique.id ORDER BY date DESC LIMIT 10;')
    return jsonify(result)

@app.route('/actu/<date>', methods=['GET'])
def get_actu_date(date):
    query = f"SELECT * FROM actu, thematique WHERE actu.thematique_id = thematique.id AND date_trunc('day', date) = '{date}' ORDER BY date DESC"
    result = execute_query(query)
    return jsonify(result)



@app.route('/news', methods=['POST'])
def create_groupe():
    data = request.json  # Supposons que les données sont envoyées au format JSON
    # Vous devez valider et structurer 'data' en fonction du format de votre table

    query = "INSERT INTO groupe(nom) VALUES (%s);"

    execute_insert(query, (data['nom'],))

    return jsonify({"message": "Groupe créé avec succès"}), 201


if __name__ == '__main__':
    app.run()
