CREATE DATABASE IF NOT EXISTS  GrHotel;
    
    USE GrHotel;

CREATE TABLE IF NOT EXISTS Hotel(
	Id_Hotel VARCHAR(6),
	Ville TEXT,
	Pays TEXT,
	CodePostal NUMERIC(5),
	CONSTRAINT fk_Hotel PRIMARY KEY (Id_Hotel) 
);

CREATE TABLE IF NOT EXISTS TypeChambre(
	Id_Type VARCHAR(6),
	Type TEXT,
	tarif NUMERIC(8),
	CONSTRAINT pk_Type PRIMARY KEY (Id_Type)
);

CREATE TABLE IF NOT EXISTS Chambre(
	Id_Chambre VARCHAR(6),
	Étage NUMERIC(2),
    nChambre numeric,
	fumeurs  INT,
	Id_Hotel VARCHAR(6),
	Id_Type VARCHAR(6),
	CONSTRAINT pk_Idchambre PRIMARY KEY (Id_Chambre),
	CONSTRAINT ck_fumeurs CHECK (fumeurs IN (0,1)),
	CONSTRAINT fk_IdHotelC FOREIGN KEY (Id_Hotel)  REFERENCES Hotel(Id_Hotel),
	CONSTRAINT fk_TypeC FOREIGN KEY (Id_Type)  REFERENCES TypeChambre(Id_Type)
);

CREATE TABLE IF NOT EXISTS Client(
	Id_client VARCHAR(6),
	Nom_complet VARCHAR(30),
	Adresse TEXT,
	Ville TEXT,
	Codepostal NUMERIC(5),
	E_mail TEXT,
	Numero_tele NUMERIC,
	CONSTRAINT pk_id_client PRIMARY KEY (Id_client)
);

CREATE TABLE IF NOT EXISTS Reservation (
    Id_Reservation VARCHAR(6),
    Date_arrivee  DATE,
    Date_depart   DATE,
    Id_client VARCHAR(6),
    CONSTRAINT pk_IdReservation PRIMARY KEY (Id_Reservation),
    CONSTRAINT fk_Nom FOREIGN KEY (Id_client) REFERENCES Client(Id_client)
);

CREATE TABLE IF NOT EXISTS Concerner (
    Id_Chambre  VARCHAR(6),
    Id_Reservation VARCHAR(6),
    CONSTRAINT pk_Concerner PRIMARY KEY (Id_Reservation, Id_Chambre),
    CONSTRAINT fk_Id_Chambre FOREIGN KEY (Id_Chambre) REFERENCES chambre(Id_Chambre),
    CONSTRAINT fk_IdReservation FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation)
);



CREATE TABLE IF NOT EXISTS Evaluation(
    Id_Evaluation  VARCHAR(6),
    Date_arrivée  DATE,
    LaNote NUMERIC(2),
    Text_Descrp TEXT,
    Id_Hotel VARCHAR(6),
	Id_client VARCHAR(6),
	CONSTRAINT pk_IdEvaluer PRIMARY KEY (Id_Evaluation) ,
	CONSTRAINT fk_IdhotelE FOREIGN KEY (Id_Hotel)  REFERENCES Hotel(Id_Hotel),
	CONSTRAINT fk_NomE FOREIGN KEY (Id_client) REFERENCES Client(Id_client)
);

CREATE TABLE IF NOT EXISTS Préstation(
	Id_Préstation VARCHAR(6),
	Prix NUMERIC,
    Nom_Préstation varchar(30),
	CONSTRAINT pk_Préstation PRIMARY KEY (Id_Préstation)
);

CREATE TABLE IF NOT EXISTS Offre(
	Id_Préstation VARCHAR(6),
	Id_Hotel VARCHAR(6),
	CONSTRAINT pk_Id PRIMARY KEY (Id_Préstation,Id_Hotel),
	CONSTRAINT fk_IdPrésatO FOREIGN KEY (Id_Préstation) REFERENCES Préstation(Id_Préstation),
	CONSTRAINT fk_IdhotelO FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel)
);
-- SHOW TABLES ;