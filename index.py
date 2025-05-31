import streamlit as st
from datetime import date
import pandas as pd
import sqlite3
import re


st.title("Gestion des Hôtels")

with st.sidebar:
    st.header(" MENU")
    choix = st.radio("", ["Accueil", "Liste des Clients", "Liste des Réservations","Les chambres dispinible", "Ajouter Client","Ajouter Réservation"])

data = sqlite3.connect("GrHotel.db")
sqlite3.connect("PARGMA foreign_keys =ON ")

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
                cur = data.cursor()
                cur.execute(
                    "INSERT INTO Client ( Adresse, Ville, CodePostal, E_mail, Numero_tele, Nom_complet) VALUES ( ?, ?, ?, ?, ?, ?)",
                    ( adresse, ville, cp, email, tel, nom)
                )
                data.commit()
                st.success("Client ajouté avec succès!")
elif choix== "Liste des Réservations": 
    st.header("La liste des Reservations :") 
    reservation=pd.read_sql_query("SELECT * FROM Reservation",data)
    st.dataframe(reservation)

elif choix== "Ajouter Réservation":   
    st.title('Ajouter Réservation')  

    with st.form('Ajouter_Reser_form'):
            Nomhotel=st.selectbox('Nom De hotel',["-- Veuillez choisir une Hotel --","Mariaf","Monalissa","Mogador"])
            typeChambre=st.selectbox('Type de Chambre',["-- Veuillez choisir une Type de Chambre --","Simple","Double"])
            fumeurs=st.selectbox('Fumeurs',["NON","OUI"])
            date_debut=st.date_input('date debut')
            date_fin=st.date_input('date fin')
            Id_client=st.text_input('CNE')
            submitted = st.form_submit_button("Ajouter")

            if submitted:
                erreurs = []
                if Nomhotel=='-- Veuillez choisir une Hotel --':
                  erreurs.append("Vous devez sélectionner un Nom de Hotel valide")
                if typeChambre=='-- Veuillez choisir une Type de Chambre --':
                   erreurs.append("Vous devez sélectionner un Type de Chambre valide")
                if not date_debut:
                     erreurs.append("L'adresse est requise.")
                if not date_fin:
                        erreurs.append("L'adresse est requise.")
                if not Id_client:
                       erreurs.append("CNE est requise.")
                if erreurs:
                    for i in erreurs:
                        st.error(i)
                else:
                    cur = data.cursor()
                    fumeurs=1 if fumeurs=='OUI' else 0
                    cur.execute("""
                         SELECT C.Id_Chambre
                         FROM Typechambre TC
                         JOIN Chambre C ON TC.Id_type = C.Id_type
                         WHERE TC.Type = ? AND C.fumeurs = ?
                        """, (typeChambre, fumeurs))
                    result = cur.fetchone()
                    if result is None:
                         st.error("")
                    else:
                      IdCh=result[0]
                      cur.execute(
                      "INSERT INTO Reservation(NomHotel,Date_arrivee,Date_depart,Id_client,Id_Chambre,fumeurs)  VALUES ( ?, ?, ?, ?, ?,?)",
                      (Nomhotel, date_debut, date_fin, Id_client, IdCh, fumeurs))
                      data.commit()
                      st.success("Client ajouté avec succès!")
data.close()
