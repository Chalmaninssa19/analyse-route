CREATE TABLE Materiel (
    idMateriel SERIAL PRIMARY KEY,
    nom VARCHAR(20),
    prixUnitaire FLOAT,
    duree FLOAT
);

CREATE TABLE RouteDetail (
    idRoute VARCHAR(10),
    idMateriel SERIAL,
    FOREIGN KEY(idMateriel) REFERENCES Materiel,
    FOREIGN KEY(idRoute) REFERENCES Route
);

CREATE TABLE Degradation (
    idDegradation SERIAL PRIMARY KEY,
    pkDebut INTEGER,
    pkFin INTEGER,
    niveau INTEGER,
    idRoute VARCHAR(10),
    FOREIGN KEY(idRoute) REFERENCES Route
);

CREATE TABLE RapportNiveau (
    niveau INTEGER,
    profondeur FLOAT
);

CREATE TABLE Route (
    roadno  VARCHAR(10) PRIMARY KEY,
    start_km FLOAT,
    end_km FLOAT,
    longueur FLOAT,
    largeur FLOAT,
    geom geometry
);

CREATE VIEW RoadCoordinate AS
SELECT roadno, ST_X(ST_StartPoint(geom)) as latitude, ST_Y(ST_StartPoint(geom)) as longitude, ST_AsGeoJSON(geom) as geoJSON 
FROM route;

CREATE VIEW Route AS 
SELECT roadno, min(start_km) as start_km, max(end_km) as end_km, sum(lengthkm) as longueur, avg(width) as largeur, ST_Union(collect.geom) as geom
FROM (SELECT * FROM madagascar_roads_version4 order by roadno, start_km asc) as collect GROUP BY roadno;


-- Insertion des donnees de test
INSERT INTO Materiel VALUES (DEFAULT, 'Goudron', 100, 5);
INSERT INTO Materiel VALUES (DEFAULT, 'Pave', 30, 3);

INSERT INTO RapportNiveau VALUES (100, 50);

-- Je vais travailler avec les routes de RN2 : 2  RNP_2_06_1 | 79 RNP_2_09_2_a | 199 RNP_2_06_3
INSERT INTO Degradation VALUES (DEFAULT, 104, 118, 8, 'RNP 2');
INSERT INTO Degradation VALUES (DEFAULT, 200, 235, 5, 'RNP 2');

INSERT INTO Degradation VALUES (DEFAULT, 321, 350, 12, 'RNP 7');

INSERT INTO Degradation VALUES (DEFAULT, 75, 110, 7, 'RNP 4');

INSERT INTO RouteDetail VALUES ('RNP 2', 1);
INSERT INTO RouteDetail VALUES ('RNP 7', 1);
INSERT INTO RouteDetail VALUES ('RNP 4', 2);
INSERT INTO RouteDetail VALUES ('RNS 1', 1);

-- Requete de recherche entre borne
SELECT * FROM Degradation WHERE 
((90<= pkdebut and 330 > pkdebut) or
(90< pkfin and 330 >= pkfin) or
(90> pkdebut and 330 < pkfin)) and idroute = 'RNP 7';