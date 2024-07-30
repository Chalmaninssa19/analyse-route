import connection

class RapportNiveau:
# Constructeur
    def __init__(self, niveau, profondeur):
        self._niveau = niveau
        self._profondeur = profondeur

# Encapsulation
    def get_niveau(self):
        return self._niveau
    
    def set_niveau(self, niveau):
        self._niveau = niveau

    def get_profondeur(self):
        return self._profondeur
    
    def set_profondeur(self, profondeur):
        self._profondeur = profondeur
 
# Fonctions de classe
    @staticmethod
    def get_rapportNiveau():
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rapportNiveau")
        listes = cursor.fetchone()
        conn.close()
        return RapportNiveau(listes[0], listes[1])