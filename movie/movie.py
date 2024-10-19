from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

import os
import json

# Obtenir le chemin du répertoire du script en cours
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin du fichier JSON en fonction du répertoire du script
json_file_path = os.path.join(script_dir, 'databases', 'movies.json')

# Vérifier si le fichier existe
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"Le fichier {json_file_path} est introuvable.")

# Charger la base de données JSON
with open(json_file_path, "r") as jsf:
    movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response('<body style="background-color: #2c2c2c; color: #e0e0e0; font-family: Arial, sans-serif; display: flex;flex-direction: column;justify-content: center;align-items: center;height: 100vh;margin: 0;"><h1 style="font-size: 2em;color: #f0f0f0;">Bienvenue sur le composant <span style="color: #1e90ff">Movie</span><span style="margin-left: 10px;">🎉</span></h1></body>',200)

@app.route("/help", methods=['GET'])
def get_help():
    return make_response(render_template('help.html'),200)
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html'),200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res


@app.route("/movies/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)
    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

def write(movies):
    with open(json_file_path, "w") as f:
        json.dump({"movies": movies}, f)

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res


if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
