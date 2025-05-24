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

data.close()
