import streamlit as st
import pandas as pd 
from streamlit_option_menu import option_menu
class ReservationView:
    def __init__(self, controller):
        self.controller = controller

    def afficher_interface(self):
       
        with st.sidebar:
        #menu = st.sidebar.radio("Navigation", ["Accueil", "Réserver", "Rechercher", "Modifier", "Salles Disponibles"])
            menu= option_menu(
                "Menu Principal",
                ["Accueil", "Réserver", "Rechercher", "Modifier","Salles Disponibles"],
                icons=['house', 'calendar-plus', 'search', 'gear', 'door-open'],
                menu_icon="cast",
                default_index=0,
                styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "25px"}, 
                "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#D2B48C"},
                }
            )
        if menu == "Accueil":
            self.afficher_accueil()
        elif menu == "Réserver":
            self.afficher_formulaire_reservation1()
        elif menu == "Rechercher":
            self.afficher_recherche()
        elif menu == "Modifier":
            self.afficher_modification()
        elif menu == "Salles Disponibles":
            self.afficher_salles_disponibles1()

    def afficher_accueil(self):
        st.title("Gestion des Réservations de Salles")
        st.write("Bienvenue dans l'application de gestion des réservations.")
       # Ajouter l'image en arrière-plan
        # Ajouter l'image en arrière-plan
        image_path = 'image1.png'  # Remplacez par le chemin de votre image
        st.image(image_path, use_container_width=True,width=400)
    def afficher_formulaire_reservation(self):
        st.header("Formulaire de Réservation")
        terrain = st.text_input("Terrain", autocomplete="off")
        salle = st.text_input("Salle", autocomplete="off")
        capacite = st.number_input("Capacité", min_value=1, step=1)
        nom_utilisateur = st.text_input("Nom de l'utilisateur", autocomplete="off")
        date_reservation = st.date_input("Date de Réservation")
        heure_reservation = st.time_input("Heure de Réservation")
        date_reservation_str = date_reservation.strftime("%Y/%m/%d")
        heure_reservation_str = heure_reservation.strftime("%H:%M")
        if st.button("Réserver"):
            erreurs = self.controller.valider_champs_reservation(
            terrain, salle, nom_utilisateur, date_reservation_str, heure_reservation_str
             )
    
            if erreurs:
            # Afficher les champs manquants
                st.error(f"Les champs suivants doivent être remplis : {', '.join(erreurs)}")
            else:
                if terrain and salle and nom_utilisateur:
                    data = (terrain, salle, capacite, nom_utilisateur, date_reservation_str, heure_reservation_str)
                    result=self.controller.reserver(data)
                    #st.success("Réservation effectuée avec succès.")
                    # Afficher le message en fonction du résultat
                    if "Réservation réussie" in result:
                        #st.success(result)
                        reservation_id = result.split(":")[-1].strip()  # Extraire l'ID de la réservation
                        st.success(f"Réservation réussie ! L'ID de la réservation est : {reservation_id}")
                    else:
                        st.error(result)
            
        # Affichage des réservations actuelles
        st.subheader("Toutes les Réservations")
        if st.button("Actualiser"):
            reservations = self.controller.get_all_reservations()
            if reservations:
                st.dataframe(
                    [{"ID": r[0], "Terrain": r[1], "Salle": r[2], "Capacité": r[3], "Utilisateur": r[4],
                      "Date": r[5], "Heure": r[6], "État": r[7]} for r in reservations]
                )
            else:
                st.warning("Aucune réservation enregistrée.")
    def afficher_recherche(self):
        st.header("Rechercher une Réservation")
        # Permettre à l'utilisateur de choisir le type de recherche
        critere = st.selectbox("Rechercher par :", ["Utilisateur", "Date"])
        if critere == "Utilisateur":
            nom_utilisateur = st.text_input("Nom de l'utilisateur à rechercher")
            if st.button("Rechercher"):
                reservations = self.controller.rechercher_reservation_par_utilisateur(nom_utilisateur)
                if reservations:
                    df = self.formatter_reservations(reservations)
                    st.dataframe(df)
                else:
                    st.warning("Aucune réservation trouvée.")
        elif critere == "Date":
            date_recherche = st.date_input("Entrez la date de réservation")
            if st.button("Rechercher par Date"):
                reservations = self.controller.rechercher_reservation_par_date(date_recherche.strftime("%Y/%m/%d"))
                if reservations:
                    df = self.formatter_reservations(reservations)
                    st.dataframe(df)
                else:
                    st.warning("Aucune réservation trouvée pour cette date.")
    def afficher_modification(self):
        reservations = self.controller.get_all_reservations()  # Assurez-vous que cette fonction renvoie toutes les réservations
        if reservations:
            st.subheader("Réservations Actuelles")
            st.dataframe(
                [{"ID": r[0], "Terrain": r[1], "Salle": r[2], "Capacité": r[3], "Utilisateur": r[4],
                "Date": r[5], "Heure": r[6], "État": r[7]} for r in reservations]
            )
        else:
            st.warning("Aucune réservation enregistrée.")
            
        reservation_id = st.number_input("ID de la réservation", min_value=1, step=1)
        etat = st.selectbox("Nouvel État", ["réservé", "disponible", "annulé"])
        if st.button("Modifier"):
            # Appeler la méthode et récupérer le message
            self.controller.modifier_reservation(reservation_id, etat)
            reservations = self.controller.get_all_reservations()
            st.success("Réservation modifiée avec succès.")
            
            

    def afficher_salles_disponibles(self):

        st.header("Salles Disponibles")
        reservations = self.controller.get_all_reservations()  # Assurez-vous que cette fonction renvoie toutes les réservations
        if reservations:
            st.subheader("Réservations Actuelles")
            st.dataframe(
                [{"ID": r[0], "Terrain": r[1], "Salle": r[2], "Capacité": r[3], "Utilisateur": r[4],
                "Date": r[5], "Heure": r[6], "État": r[7]} for r in reservations]
                )
        else:
            st.warning("Aucune réservation enregistrée.")
        date = st.date_input("Date")
        heure = st.time_input("Heure")
        date1 = date.strftime("%Y/%m/%d")
        heure1 = heure.strftime("%H:%M")
        if st.button("Afficher"):
            salles = self.controller.get_salles_disponibles(date1, heure1)
            if salles:
                df = self.formatter_reservations(salles)
                st.dataframe(df)
            else:
                st.warning("Aucune salle disponible.")

    def formatter_reservations(self, reservations):
        # Convertir les données brutes en DataFrame pour un affichage clair
        return pd.DataFrame(
            reservations,
            columns=["ID", "Terrain", "Salle", "Capacité", "Utilisateur", "Date", "Heure", "État"]
        )
    def afficher_salles_disponibles1(self):
        st.header("Salles Disponibles")
        
        reservations = self.controller.get_all_reservations()  # Obtenez toutes les réservations
        if reservations:
            st.subheader("Réservations Actuelles")
            # Créez un DataFrame à partir des réservations et permettez la sélection
            reservations_df = [{"ID": r[0], "Terrain": r[1], "Salle": r[2], "Capacité": r[3], "Utilisateur": r[4], 
                                "Date": r[5], "Heure": r[6], "État": r[7]} for r in reservations]
            df = pd.DataFrame(reservations_df)
            
            # Affichage du DataFrame
            selected_row = st.selectbox("Sélectionner une réservation", df.index, format_func=lambda x: f"{df.at[x, 'Date']} {df.at[x, 'Heure']}")
            
            # Récupérer les valeurs de la ligne sélectionnée
            selected_data = df.iloc[selected_row]
            
            # Pré-remplir les champs avec les données de la ligne sélectionnée
            st.write(f"Sélectionné :  {selected_data['Date']}       {selected_data['Heure']}")
            
            # Champs de saisie pour l'utilisateur
            date = st.date_input("Date", value=pd.to_datetime(selected_data['Date']))
            heure = st.time_input("Heure", value=pd.to_datetime(selected_data['Heure']).time())
          
            
        else:
            st.warning("Aucune réservation enregistrée.")
            
        # Afficher les salles disponibles si l'utilisateur clique sur "Afficher"
        date1 = date.strftime("%Y/%m/%d")
        heure1 = heure.strftime("%H:%M")
        if st.button("Afficher"):
            salles = self.controller.get_salles_disponibles(date1, heure1)
            if salles:
                df_salles = self.formatter_reservations(salles)
                st.dataframe(df_salles)
            else:
                st.warning("Aucune salle disponible.")
    def afficher_formulaire_reservation1(self):
        st.header("Formulaire de Réservation")
        
        # Charger toutes les réservations existantes
        reservations = self.controller.get_all_reservations()
        
        if reservations:
            # Créer un DataFrame avec les réservations
            df_reservations = pd.DataFrame(
                [{"ID": r[0], "Terrain": r[1], "Salle": r[2], "Capacité": r[3], "Utilisateur": r[4],
                "Date": r[5], "Heure": r[6], "État": r[7]} for r in reservations]
            )

            # Afficher un selectbox pour choisir une réservation à modifier, avec toutes les informations
            selected_reservation_id = st.selectbox(
                "Sélectionner une réservation",
                df_reservations.apply(lambda row: f"ID {row['ID']} - {row['Terrain']} - {row['Salle']} - {row['Utilisateur']} - {row['Date']} - {row['Heure']} - {row['État']}", axis=1)
            )
            
            # Extraire l'ID de la réservation sélectionnée à partir de la chaîne
            selected_reservation_id = selected_reservation_id.split(" ")[1]  # ID se trouve après "ID"
            
            # Récupérer la ligne de la réservation sélectionnée
            selected_reservation = df_reservations[df_reservations['ID'] == int(selected_reservation_id)].iloc[0]

            # Remplir les champs du formulaire avec les données de la réservation sélectionnée
            terrain = selected_reservation['Terrain']
            salle = selected_reservation['Salle']
            capacite = selected_reservation['Capacité']
            nom_utilisateur = selected_reservation['Utilisateur']
            date_reservation = pd.to_datetime(selected_reservation['Date']).date()  # Convertir en type date
            heure_reservation = pd.to_datetime(selected_reservation['Heure']).time()  # Convertir en type time
            
            # Affichage des champs du formulaire pré-remplis
            terrain_input = st.text_input("Terrain", value=terrain, autocomplete="off")
            salle_input = st.text_input("Salle", value=salle, autocomplete="off")
            capacite_input = st.number_input("Capacité", value=capacite, min_value=1, step=1)
            nom_utilisateur_input = st.text_input("Nom de l'utilisateur", value=nom_utilisateur, autocomplete="off")
            date_reservation_input = st.date_input("Date de Réservation", value=date_reservation)
            heure_reservation_input = st.time_input("Heure de Réservation", value=heure_reservation)

            if st.button("Réserver"):
                erreurs = self.controller.valider_champs_reservation(
                    terrain_input, salle_input, nom_utilisateur_input, date_reservation_input.strftime("%Y/%m/%d"), heure_reservation_input.strftime("%H:%M")
                )
                
                if erreurs:
                    st.error(f"Les champs suivants doivent être remplis : {', '.join(erreurs)}")
                else:
                    data = (terrain_input, salle_input, capacite_input, nom_utilisateur_input, date_reservation_input.strftime("%Y/%m/%d"), heure_reservation_input.strftime("%H:%M"))
                    result = self.controller.reserver(data)
                    
                    if "Réservation réussie" in result:
                        reservation_id = result.split(":")[-1].strip()
                        st.success(f"Réservation réussie ! L'ID de la réservation est : {reservation_id}")
                    else:
                        st.error(result)
        else:
            st.warning("Aucune réservation enregistrée.")
