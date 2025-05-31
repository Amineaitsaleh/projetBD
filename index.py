import streamlit as st
from datetime import date,timedelta
import pandas as pd
import sqlite3
import re


st.title("Gestion des Hôtels")

with st.sidebar:
    st.header(" MENU")
    choix = st.radio("", ["Accueil", "Liste des Clients", "Liste des Réservations","Les chambres dispinible", "Ajouter Client","Ajouter Réservation"])

data = sqlite3.connect("GrHotel.db")
cur = data.cursor()
cur.execute("PRAGMA foreign_keys = ON")

if choix == "Accueil":
    st.header(" Bienvenue à l'application de gestion")
    st.write("Choisissez une section à gauche pour commencer.")

elif choix == "Liste des Clients":
    st.header(" Liste des Clients")
    df = pd.read_sql_query("SELECT * FROM Client", data)
    st.dataframe(df)
elif choix == "Les chambres dispinible" :
    date_debut = st.date_input("Date d'arrivée", min_value=date.today())
    date_fin = st.date_input("Date de départ", min_value=date_debut)
    
    requet = """
        SELECT * FROM Chambre
        WHERE nChambre NOT IN (
            SELECT CH.nChambre
            FROM Chambre CH
            JOIN Concerner C ON C.Id_Chambre = CH.Id_Chambre
            JOIN Reservation R ON R.Id_Reservation = C.Id_Reservation
            WHERE NOT (
                R.Date_depart <= ? OR R.Date_arrivee >= ?
            )
        )
    """
    df = pd.read_sql_query(requet, data, params=(date_debut, date_fin))
    st.header(" Les chambres dispinible ")
    st.dataframe(df)

elif choix== "Ajouter Client":
    st.title("Ajouter un nouveau client")

    with st.form("ajout_client_form"):
        nom = st.text_input("Nom complet")
        cin = st.text_input("CIN")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        cp = st.text_input("Code postal")
        email = st.text_input("Email")
        tel = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter")

        if submitted:
            erreurs = []
            if not nom:
                erreurs.append("Le nom est requis.")

            if cin and not re.match(r"^[A-Z]{2}[0-9]{5}$", cin):
                erreurs.append(" CIN invalide.")

            if not ville:
                erreurs.append("La ville est requise.")

            if not adresse:
                erreurs.append("L'adresse est requise.")

            if not cp.isdigit() or len(cp) != 5:
                erreurs.append("Code postal invalide.")

            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                erreurs.append("email invalide.")
                
            if not re.match(r"^\d{10}$", tel):
                erreurs.append("Téléphone invalide (10 chiffres).")
            
            if erreurs:
                for i in erreurs:
                    st.error(i)
            else:
                cur.execute(
                    "INSERT INTO Client (CIN, Adresse, Ville, CodePostal, E_mail, Numero_tele, Nom_complet) VALUES ( ?, ?, ?, ?, ?, ?, ?)",
                    (cin, adresse, ville, cp, email, tel, nom)
                )
                data.commit()
                st.success("Client ajouté avec succès!")
elif choix== "Liste des Réservations": 
    st.header("La liste des Reservations :") 
    reservation=pd.read_sql_query("SELECT * FROM Reservation",data)
    st.dataframe(reservation)

elif choix== "Ajouter Réservation":   
    st.title('Ajouter Réservation')

    cur.execute("SELECT DISTINCT Ville FROM Hotel")
    villes = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT  Type FROM TypeChambre")
    types_chambres = [row[0] for row in cur.fetchall()]

    with st.form('Ajouter_Reser_form'):
            cin=st.text_input('CIN :')
            ville = st.selectbox("Choisir une ville :", villes)
            typeChambre=st.selectbox('Type de Chambre :',types_chambres)
            fumeurs=st.selectbox('Fumeurs :',["NON","OUI"])
            nb_chambre=st.number_input("Nombre des chambres :", min_value=1, value=1)
            date_debut=st.date_input('date debut :',min_value=date.today())
            nb_jours = st.number_input("Nombre de jours :", min_value=1, value=1)
            date_fin=date_debut + timedelta(days=int(nb_jours))
            submitted = st.form_submit_button("Ajouter")

            if submitted:
                erreurs = []
                if cin and not re.match(r"^[A-Z]{2}[0-9]{5}$", cin):
                    erreurs.append(" CIN invalide.")
                else:
                    cur.execute("SELECT 1 FROM Client WHERE CIN = ?", (cin,))
                    existe = cur.fetchone()
                    if not existe:
                        erreurs.append("Ce CIN n'existe pas dans la base des clients. Veuillez d'abord ajouter le client.")
                if erreurs:
                    for i in erreurs:
                        st.error(i)
                else:
                    fumeurs=1 if fumeurs=='OUI' else 0
                    cur.execute("""
                       SELECT C.Id_Chambre
                        FROM Typechambre TC
                        JOIN Chambre C ON TC.Id_type = C.Id_type
                        JOIN Hotel H ON C.Id_Hotel = H.Id_Hotel
                        WHERE TC.Type = ?
                        AND C.fumeurs = ?
                        AND H.Ville = ?
                        AND C.Id_Chambre NOT IN (
                            SELECT Co.Id_Chambre
                            FROM Concerner Co
                            JOIN Reservation R ON Co.Id_Reservation = R.Id_Reservation
                            WHERE NOT (
                                R.Date_depart <= ? OR R.Date_arrivee >= ?
                            )
                        )
                        LIMIT ?
                    """, (typeChambre, fumeurs, ville, date_debut, date_fin,nb_chambre))
                    result = [row[0] for row in cur.fetchall()]

                    if len(result) < nb_chambre:
                        if nb_chambre == 1:
                            st.error("Aucune chambre du type sélectionné, avec l'option fumeurs choisie, n'est disponible pour les dates demandées.")
                        else:
                            st.error("Le nombre de chambres disponibles est insuffisant.")
                    else:
                        cur.execute(
                        "INSERT INTO Reservation(Date_arrivee,Date_depart,CIN)  VALUES (?, ?, ?)",
                        (date_debut, date_fin,cin))
                        data.commit()
                        id_reservation = cur.lastrowid

                        for i in range(nb_chambre):
                            cur.execute("""
                                INSERT INTO Concerner (Id_Reservation, Id_Chambre)
                                VALUES (?, ?)
                            """, (id_reservation, result[i]))
                        data.commit() 
                        st.success("Réservation ajoutée avec succès !")
data.close()
