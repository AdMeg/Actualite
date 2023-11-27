from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@10.19.2.1:5432/projet_S7_fil_actu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Simuler une base de données avec une liste en mémoire
news_db = [
    {"id": 1, "title": "Nouvelle importante", "content": "Contenu de la nouvelle importante"}
]

@app.route('/news', methods=['GET'])
def get_news():
    """Endpoint pour récupérer les actualités."""
    return Flask(news_db)

@app.route('/news', methods=['POST'])
def post_news():
    """Endpoint pour publier une nouvelle actualité."""
    news_data = Flask.json
    news_data['id'] = len(news_db) + 1  # Assigner un ID simple
    news_db.append(news_data)
    return Flask(news_data), 201

if __name__ == '__main__':
    app.run(debug=True)
