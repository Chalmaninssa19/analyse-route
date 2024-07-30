]import materiel
import route
import degradation
from degradation import Degradation
import rapportNiveau
import json
import re
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from route import Route

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    listes = Route.get_degraded_route()
    routes = Route.get_all_route()
    road = None
    if request.method == 'POST':
        road = Route.get_route(request.form['idRoute'])
        coord = road.get_route_coordinate()
        rapport = rapportNiveau.RapportNiveau.get_rapportNiveau()
        return render_template("index.html", round = round, int = int, listes = listes, routes = routes, road = road, latitude = coord[0], longitude = coord[1], geoJSON = coord[2], degats = road.get_degradations(), rapport = rapport)
    else:
        return render_template("index.html", listes = listes, road = road, routes = routes)
 
@app.route("/insertion", methods=['POST', 'GET'])
def insert():
    print("Voila " + request.form['route'])
    print("Voila debut " + request.form['pk_debut'])
    print("Voila fin " + request.form['pk_fin'])
    Route.add_new_degradation(request.form['route'], int(request.form['pk_debut']), int(request.form['pk_fin']), int(request.form['niveau']))
    return redirect("/") 

@app.route("/delete", methods=['GET'])
def delete():
    Degradation.remove_degradation(request.args.get('indice'))
    return redirect("/") 
