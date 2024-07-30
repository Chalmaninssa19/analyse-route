import connection

def get_degraded_road_coordonnee(degradation):    
    #renvoie les routes detruits
    conn = connection.get_connection()
    cursor = conn.cursor()

    # Prends le tracée du route
    debut = degradation.get_pk_debut() / degradation.get_route().get_longueur()
    fin = degradation.get_pk_fin() / degradation.get_route().get_longueur()
    sql= "SELECT ST_AsGeoJson(ST_LineSubstring(geom, {}, {})) FROM Route WHERE roadno = '{}'".format(debut, fin, degradation.get_route().get_id_route())
    cursor.execute(sql)
    line = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return line

