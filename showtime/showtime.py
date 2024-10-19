from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

import os
import json

# Obtenir le chemin du répertoire du script en cours
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin du fichier JSON en fonction du répertoire du script
json_file_path = os.path.join(script_dir, 'databases', 'times.json')

# Vérifier si le fichier existe
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"Le fichier {json_file_path} est introuvable.")

# Charger la base de données JSON
with open(json_file_path, "r") as jsf:
    schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return '<body style="background-color: #2c2c2c; color: #e0e0e0; font-family: Arial, sans-serif; display: flex;flex-direction: column;justify-content: center;align-items: center;height: 100vh;margin: 0;"><h1 style="font-size: 2em;color: #f0f0f0;">Bienvenue sur le composant <span style="color: #1e90ff">Showtime (Times)</span><span style="margin-left: 10px;">🎉</span></h1></body>'


@app.route("/showtimes", methods=['GET'])
def get_json():
    res = make_response(jsonify(schedule), 200)
    return res

@app.route("/showtimes/<date>", methods=['GET'])
def get_showtimes(date):
   for day in schedule:
      if str(day["date"]) == str(date):
         res = make_response(jsonify(day), 200)
         return res
   return make_response(jsonify({"error": "Date not found for date "+date}), 400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
