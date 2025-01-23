from modele import ReservationModel
from vue import ReservationView

class ReservationController:
    def __init__(self):
        self.model = ReservationModel()
        self.view = ReservationView(self)
        #self.model.inserer_donnees_initiales()
    def rechercher_reservation_par_utilisateur(self, nom_utilisateur):
        return self.model.rechercher_reservation_par_utilisateur(nom_utilisateur)

    def rechercher_reservation_par_date(self, date_reservation):
        return self.model.rechercher_reservation_par_date(date_reservation)    
    def reserver(self, data):
        result=self.model.reserver_salle1(data)
        return result
    def valider_champs_reservation(self, terrain, salle, nom_utilisateur, date_reservation, heure_reservation):
        """Valide les champs nécessaires pour une réservation."""
        erreurs = []
        if not terrain:
            erreurs.append("Terrain")
        if not salle:
            erreurs.append("Salle")
        if not nom_utilisateur:
            erreurs.append("Nom d'utilisateur")
        if not date_reservation:
            erreurs.append("Date de réservation")
        if not heure_reservation:
            erreurs.append("Heure de réservation")
        return erreurs



    def modifier_reservation(self, reservation_id, etat):
        self.model.modifier_reservation(reservation_id, etat)

    def get_salles_disponibles(self, date, heure):
        return self.model.get_salles_disponibles1(date, heure)

    def run(self):
        self.view.afficher_interface()
    def get_all_reservations(self):
        # Appelle la méthode du modèle pour récupérer toutes les réservations
        return self.model.get_all_reservations()
    def get_salles_disponibles(self, date, heure):
        return self.model.get_salles_disponibles(date, heure)
if __name__ == "__main__":
    controller = ReservationController()
    controller.run()
