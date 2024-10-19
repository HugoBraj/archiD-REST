from flask import Flask, render_template, request, jsonify, make_response
import requests

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

import os
import json

# Obtenir le chemin du répertoire du script en cours
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin du fichier JSON en fonction du répertoire du script
json_file_path = os.path.join(script_dir, 'databases', 'bookings.json')

# Vérifier si le fichier existe
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"Le fichier {json_file_path} est introuvable.")

# Charger la base de données JSON
with open(json_file_path, "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return '<body style="background-color: #2c2c2c; color: #e0e0e0; font-family: Arial, sans-serif; display: flex;flex-direction: column;justify-content: center;align-items: center;height: 100vh;margin: 0;"><h1 style="font-size: 2em;color: #f0f0f0;">Bienvenue sur le composant <span style="color: #1e90ff">Booking</span><span style="margin-left: 10px;">🎉</span></h1></body>'


@app.route("/bookings", methods=['GET'])
def get_bookings():
    return make_response(jsonify(bookings), 200)


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking(userid):
    for booking in bookings:
        if booking["userid"] == str(userid):
            return make_response(jsonify(booking), 200)
    return make_response(jsonify({"error": "Booking not found for user id '" + userid + "'"}), 400)


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking(userid):
    req = request.get_json()
    showtime = requests.get('http://127.0.0.1:3202/showtimes/' + req["date"])

    if showtime.status_code != 200:
        return make_response(jsonify({"error": "No date existing for this booking"}), 400)
    elif len(showtime.json()["movies"]) == 0:
        return make_response(jsonify({"error": "No movies existing for this date of booking"}), 400)
    else:
        movies_on_this_date = showtime.json()["movies"]
        for movie in req.get("movies"):
            if not movies_on_this_date.__contains__(movie):
                return make_response(
                    jsonify({"error": "One or many of the movies to book are not available for this date"}), 400)
        bookings_of_user = get_booking(userid).get_json()

        if 'dates' in bookings_of_user:
            for booking in bookings_of_user.get("dates"):
                if booking.get("date") == req["date"]:
                    return make_response(jsonify({"error": "Booking already exists for this date"}), 400)
            for booking in bookings:
                if str(booking["userid"]) == str(userid):
                    booking["dates"].append(req)
                    res = make_response(jsonify({"message": "booking added for bookings of user '" + userid + "'"}),
                                        200)
                    return res
        else:
            bookings.append({
                "userid": userid,
                "dates": [
                    req
                ]
            })
            write(bookings)
            res = make_response(jsonify({"message": "a first booking has been added for user '" + userid + "'"}), 200)
            return res


def write(bookings):
    with open(json_file_path, "w") as f:
        json.dump({"bookings": bookings}, f)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
