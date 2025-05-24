--  la liste des réservations avec le nom du client et la ville de l’hôtel réservé.
SELECT 
r.Id_Reservation,c.Nom_complet AS NomClient,h.Ville AS VilleHotel
FROM 
Reservation r JOIN Client c ON r.Id_client = c.Id_client
JOIN Concerner con ON r.Id_Reservation = con.Id_Reservation
JOIN Chambre ch ON con.Id_Chambre = ch.Id_Chambre
JOIN Hotel h ON ch.Id_Hotel = h.Id_Hotel;

-- Calculer le nombre de réservations faites par chaque client.
SELECT Id_client, COUNT(Id_Reservation) AS Nbr_reservation 
FROM reservation 
GROUP BY Id_client;

-- requétes
-- b
SELECT Nom_complet
FROM Gr1Hotel.Client
WHERE Ville='Paris';
-- d
SELECT Type,COUNT(nChambre) AS Nombre_DeChmbre
FROM Typechambre TC,Chambre C
WHERE TC.Id_Type=C.Id_Type
GROUP BY Type;
-- e
SELECT nChambre
FROM gr1hotel.Chambre
WHERE nChambre NOT IN(
  SELECT CH.nChambre
  FROM gr1hotel.Chambre CH 
  JOIN gr1hotel.Concerner C ON C.Id_Chambre = CH.Id_Chambre
  JOIN gr1hotel.Reservation R ON R.Id_Reservation = C.Id_Reservation
  WHERE R.Date_arrivee <= @fiN
    AND R.Date_depart >= @DEBUT
);

