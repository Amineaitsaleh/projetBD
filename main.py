import sqlite3 as sql

data = sql.connect("GrHotel.db")
cursor = data.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Hotel(
    Id_Hotel TEXT PRIMARY KEY,  
    Ville TEXT,
    Pays TEXT,
    NomHotel TEXT,
    CodePostal INTEGER
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS TypeChambre(
    Id_Type TEXT PRIMARY KEY,
    Type TEXT,
    tarif REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Chambre(
    Id_Chambre TEXT PRIMARY KEY,
    nChambre INTEGER,
    Étage INTEGER,
    fumeurs INTEGER CHECK (fumeurs IN (0, 1)),
    Id_Hotel TEXT,
    Id_Type TEXT,
    CONSTRAINT fk_idHotel FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    CONSTRAINT fk_idType FOREIGN KEY (Id_Type) REFERENCES TypeChambre(Id_Type)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Client(
    Id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    Adresse TEXT,
    Ville TEXT,
    Codepostal TEXT,
    E_mail TEXT,
    Numero_tele TEXT,
    Nom_complet TEXT
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS Reservation(
    Id_Reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    NomHotel Text,
    Date_arrivee DATE,
    Date_depart DATE,
    Id_client TEXT,
    Id_Chambre TEXT,
    fumeurs INTEGER,
    CONSTRAINT fk_Idclient FOREIGN KEY (Id_client) REFERENCES Client(Id_client),
    CONSTRAINT fk_NomHotel FOREIGN KEY (NomHotel) REFERENCES Hotel( NomHotel) ,
    CONSTRAINT fk_IdChambre FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre)  ,
    CONSTRAINT fk_fumeurs FOREIGN KEY (fumeurs) REFERENCES Chambre(fumeurs)             
);  
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Concerner(
    Id_Chambre TEXT,
    Id_Reservation TEXT,
    PRIMARY KEY (Id_Reservation, Id_Chambre),
    FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre),
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Evaluation(
    Id_Evaluation TEXT PRIMARY KEY,
    Date_arrivée DATE,
    LaNote INTEGER,
    Text_Descrp TEXT,
    Id_client TEXT,
    Id_Hotel TEXT,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_client) REFERENCES Client(Id_client)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Préstation(
    Id_Préstation TEXT PRIMARY KEY,
    Prix REAL,
    Nom_Préstation TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Offre(
    Id_Préstation TEXT,
    Id_Hotel TEXT,
    PRIMARY KEY (Id_Préstation, Id_Hotel),
    FOREIGN KEY (Id_Préstation) REFERENCES Préstation(Id_Préstation),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel)
);
""")

#Insertion
Hotel=[
    ( 1,'Paris', 'France',"SANFRANCISSCO", 75001) ,
    (2,'Lyon', 'France',"MONALISA",69002),
    (3,'Lyon', 'France',"THE PLAZA",69002),
    ]
#cursor.executemany("INSERT INTO Hotel VALUES(?,?,?,?,?)",Hotel)
Client=[
    (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', 
      '0612345678', 'Jean Dupont'),
    (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', 
     '0623456789', 'Marie Leroy') ,
    (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 
    'paul.moreau@email.fr', '0634567890', 'Paul Moreau'), 
    (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', 
'0645678901', 'Lucie Martin') ,
    (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', 
    '0656789012', 'Emma Giraud') 
]
#cursor.executemany("INSERT INTO Client Values(?,?,?,?,?,?,?)",Client)
Prestation=[
    (1, 15, 'Petit-déjeuner') ,
    (2, 30, 'Navette aéroport'), 
    (3, 0, 'Wi-Fi gratuit') ,
    (4, 50, 'Spa et bien-être'), 
    (5, 20, 'Parking sécurisé') 
]
#cursor.executemany("INSERT INTO Préstation Values(?,?,?)",Prestation)
TypeChambre=[
   (1, 'Simple', 80),
   (2, 'Double', 120)
]
#cursor.executemany("INSERT INTO TypeChambre Values(?,?,?)",TypeChambre)
Chambre=[
    (1, 201, 2, 0, 1, 1) ,
    (2, 502, 5, 1, 1, 2) ,
    (3, 305, 3, 0, 2, 1) ,
    (4, 410, 4, 0, 2, 2) ,
    (5, 104, 1, 1, 2, 2) ,
    (6, 202, 2, 0, 1, 1) ,
    (7, 307, 3, 1, 1, 2) ,
    (8, 101, 1, 0, 1, 1) 
]
#cursor.executemany("INSERT INTO Chambre Values(?,?,?,?,?,?)",Chambre)
Reservation=[
    # Client 1 (Jean Dupont) 
("SANFRANCISSCO", '2025-06-15', '2025-06-18',1,2,1) ,
# Client 2 (Marie Leroy) 
("MONALISA",'2025-07-01', '2025-07-05', 2,2,1) ,
("THE PLAZA", '2025-11-12', '2025-11-14', 2,8,1) ,
("MONALISA",'2026-02-01', '2026-02-05', 2,7,0) ,
# Client 3 (Paul Moreau) 
("SANFRANCISSCO", '2025-08-10', '2025-08-14', 3,4,1) ,
# Client 4 (Lucie Martin) 
("THE PLAZA", '2025-09-05', '2025-09-07', 4,7,1) ,
("MONALISA", '2026-01-15', '2026-01-18', 4,8,0) ,
# Client 5 (Emma Giraud) 
("SANFRANCISSCO",'2025-09-20', '2025-09-25', 5,1,0),
]
#cursor.executemany("INSERT INTO Reservation (NomHotel,Date_arrivee,Date_depart,Id_client,Id_Chambre,fumeurs) VALUES (?, ?, ?, ?, ?, ?);",Reservation)

Evaluation=[
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1, 2),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2, 1),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3, 1),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4, 2),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5, 1)
]
#cursor.executemany("INSERT INTO Evaluation Values(?,?,?,?,?,?)",Evaluation)

Concerner=[
    (1,1),
    (2, 2),
    (3, 7),
    (4, 10),
    (5, 3),
    (6, 4),
    (7,9),
    (8,5)
]
#cursor.executemany("INSERT INTO Concerner Values(?,?)",Concerner)




data.commit()
data.close()

