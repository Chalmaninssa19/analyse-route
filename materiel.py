import connection

class Materiel:
# Constructeur
    def __init__(self, id_materiel, nom, prix_unitaire, duree):
        self._id_materiel = id_materiel
        self._nom = nom
        self._prix_unitaire = prix_unitaire     # par metre cube
        self._duree = duree     # en heure

# Encapsulation
    def get_id_materiel(self):
        return self._id_materiel
    
    def set_id_materiel(self, id_materiel):
        self._id_materiel = id_materiel
        
    def get_nom(self):
        return self._nom
    
    def set_nom(self, nom):
        self._nom = nom

    def get_prix_unitaire(self):
        return self._prix_unitaire
    
    def set_prix_unitaire(self, prix_unitaire):
        self._prix_unitaire = prix_unitaire

    def get_duree(self):
        return self._duree
    
    def set_duree(self, duree):
        self._duree = duree
        
# Fonction de classe
    @staticmethod
    def get_all_materiel():
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materiel")
        listes = cursor.fetchall()
        materiels = []
        for element in listes:
            materiels.append(Materiel(element[0], element[1], element[2], element[3]))
        conn.close()
        return materiels

    @staticmethod
    def get_materiel(id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materiel WHERE idmateriel = " + str(id))
        listes = cursor.fetchone()
        conn.close()
        return Materiel(listes[0], listes[1], listes[2], listes[3])
