from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

import os
import json

# Obtenir le chemin du répertoire du script en cours
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin du fichier JSON en fonction du répertoire du script
json_file_path = os.path.join(script_dir, 'databases', 'users.json')

# Vérifier si le fichier existe
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"Le fichier {json_file_path} est introuvable.")

# Charger la base de données JSON
with open(json_file_path, "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# un point d’entrée permettant d’obtenir les réservations à partir du nom ou de l’ID d’un utilisateur ce qui
# demandera à interroger le service Booking pour vérifier que la réservation est bien disponible à la date demandée

@app.route("/users", methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)


@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    for user in users:
        if user['id'] == id:
            return make_response(jsonify(user), 200)
        else:
            return make_response(jsonify({"error": "User not found for id '" + id + "'"}), 400)


@app.route("/users/<id>", methods=['POST'])
def create_user(id):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify({"error": "user ID already exists"}), 409)
    users.append(req)
    write(users)
    res = make_response(jsonify({"message": "user added"}), 200)
    return res


def write(users):
    with open(json_file_path, "w") as f:
        json.dump({"users": users}, f)


@app.route("/users/<id>/bookings", methods=['GET'])
def get_user_bookings(id):
    user = get_user(id)
    if user.status_code != 200:
        return user
    else:
        bookings = requests.get('http://127.0.0.1:3201/bookings/' + id)
        if bookings.status_code != 200:
            return bookings
        else:
            return make_response(jsonify({id: bookings.json().get("dates")}), 200)


@app.route("/users/<id>/detailed_bookings", methods=['GET'])
def get_user_detailed_bookings(id):
    bookings = get_user_bookings(id)
    if bookings.status_code != 200:
        return bookings
    else:
        bookings_temp = bookings.get_json().get(id)
        for booking in bookings_temp:
            movies = []
            for movie in booking.get("movies"):
                print(movie)
                get_movie = requests.get('http://127.0.0.1:3200/movies/' + movie)
                if get_movie.status_code == 200:
                    movies.append(get_movie.json())
            booking.update({"movies": movies})
        return make_response(jsonify({id: bookings_temp}), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
