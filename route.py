import materiel
import connection
import rapportNiveau
import degradation
from degradation import Degradation
from map import get_degraded_road_coordonnee
from util import *

class Route:
# Constructeur
    def __init__(self, id_route, start_km, end_km, longueur, largeur, materiel):
        self._id_route = id_route
        self._largeur = largeur
        self._longueur = longueur
        self._start_km = start_km
        self._end_km = end_km
        self._materiel = materiel
        self._degradations = None

# Encapsulation
    def get_id_route(self):
        return self._id_route
    
    def set_id_route(self, id_route):
        self._id_route = id_route

    def get_largeur(self):
        return self._largeur
    
    def set_largeur(self, largeur):
        return self._largeur
    
    def get_longueur(self):
        return self._longueur
    
    def set_longueur(self, longueur):
        return self._longueur
    
    def get_start_km(self):
        return self._start_km
    
    def set_start_km(self, start_km):
        return self._start_km
    
    def get_end_km(self):
        return self._end_km
    
    def set_end_km(self, end_km):
        return self._end_km
    
    def get_materiel(self):
        return self._materiel
    
    def set_materiel(self, materiel):
        return self._materiel
    
    def get_degradations(self):
        return self._degradations
    
    def set_degradations(self, degradations):
        self._degradations = degradations
    
# Fonctions de classe

    # centre du point a tracer
    def get_center_degraded_point(self):
        listes = self.get_all_degraded_point()
        resultat = []
        for element in listes:
            latitude = (element[0][0] + element[1][0]) / 2
            longitude = (element[0][1] + element[1][1]) / 2
            resultat.append([latitude, longitude, element[2]])
        return resultat

    # fontion qui retourne tous les routes detruit en point geometrique
    def get_all_degraded_point(self):
        degraded_listes = self.get_degradations()
        resultat = []
        for degraded in degraded_listes:
            resultat.append(degraded.get_degradation_Area())
        return resultat

    def get_route_coordinate(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude, geojson FROM roadCoordinate WHERE roadno = '" + self.get_id_route() + "'")
        coord = cursor.fetchone()
        cursor.close()
        conn.close()
        return coord

    def get_reparation_price(self):
        rapport = rapportNiveau.RapportNiveau.get_rapportNiveau()
        degradations = self.get_degradations()
        somme = 0
        for deg in degradations:
            somme += deg.get_reparation_price(rapport)
        return somme
    
    def display_reparation_price(self):
        return format_argent(self.get_reparation_price())
    
    def get_reparation_duration(self):
        rapport = rapportNiveau.RapportNiveau.get_rapportNiveau()
        degradations = self.get_degradations()
        somme = 0       # en heure
        for deg in degradations:
            somme += deg.get_reparation_duration(rapport)
        return somme

    def display_reparation_duration(self):
        return format_temps(self.get_reparation_duration())
    
    def load_degradations(self):
        # charge tous les degradations d'une route
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM degradation WHERE idroute = '" + self.get_id_route() + "'")
        listes = cursor.fetchall()
        degradations = []
        for element in listes:
            degr = degradation.Degradation(element[0], element[1], element[2], element[3])
            degr.set_route(self)
            degradations.append(degr)
        self.set_degradations(degradations)
        conn.close()

    def adjust_degradations(self, b_debut, b_fin, listes):
        for element in listes:
            if element.get_pk_debut() < b_debut:
                element.set_pk_debut(b_debut)
            if element.get_pk_fin() > b_fin:
                element.set_pk_fin(b_fin)

    def get_inclue_degradations(self, b_debut, b_fin):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM Degradation WHERE " \
            "((" + str(b_debut) + " <= pkdebut and " + str(b_fin) + " > pkdebut) or " \
            "(" + str(b_debut) + " < pkfin and " + str(b_fin) + " >= pkfin) or " \
            "(" + str(b_debut) + " > pkdebut and " + str(b_fin) + " < pkfin)) and idroute = '" + self.get_id_route() + "'"
        cursor.execute(sql)
        listes = cursor.fetchall()
        degradations = []
        for element in listes:
            degr = degradation.Degradation(element[0], element[1], element[2], element[3])
            degr.set_route(self)
            degradations.append(degr)
        conn.close()
        self.adjust_degradations(b_debut, b_fin, degradations)
        return degradations

    @staticmethod
    def get_route(id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        # prendre le materiaux de ce route
        cursor.execute("SELECT idmateriel FROM RouteDetail WHERE idroute = '" + id + "'")

        id_materiel = cursor.fetchone()[0]
        mat = materiel.Materiel.get_materiel(id_materiel)

        # creation de l'objet route
        cursor.execute("SELECT * FROM route WHERE roadno = '" + id + "'")
        element = cursor.fetchone()
        route = Route(element[0], element[1], element[2], element[3], element[4], mat)
        route.load_degradations()
        conn.close()
        return route
    
    @staticmethod
    def get_all_route():
        conn = connection.get_connection()
        cursor = conn.cursor()
        # prendre le materiaux de ce route
        cursor.execute("SELECT idroute FROM routedetail")

        routes = cursor.fetchall()
        listes = []
        for route in routes:
            listes.append(route[0])
        return listes

    @staticmethod
    def get_degraded_route():
        conn = connection.get_connection()
        cursor = conn.cursor()
        # prendre le materiaux de ce route
        cursor.execute("SELECT idroute FROM routedetail")

        routes = cursor.fetchall()
        listes = []
        for route in routes:
            listes.append(Route.get_route(route[0]))
        return listes

    @staticmethod
    def add_new_degradation(id_route, pk_debut, pk_fin, niveau):
        if pk_debut > pk_fin:
            print("Le debut doit etre inferieur a la fin")
            return "Le debut doit etre inferieur a la fin"
        lalana = Route.get_route(id_route)
        if pk_fin > lalana.get_end_km():
            print("Le PK fin doit etre a l'interieur de la route")
            return "Le PK fin doit etre a l'interieur de la route"
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO Degradation VALUES (DEFAULT, {}, {}, {}, '{}')".format(pk_debut, pk_fin, niveau, id_route)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
