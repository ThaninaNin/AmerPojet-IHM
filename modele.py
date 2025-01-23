import sqlite3

class ReservationModel:
    def __init__(self, db_name="reservations.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            terrain TEXT,
            salle TEXT,
            capacite INTEGER,
            nom_utilisateur TEXT,
            date_reservation DATE,
            heure_reservation TIME,
            etat TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()
    
    def inserer_donnees_initiales(self):
        data = [
            #("Terrain 1", "Salle A", 20, "Utilisateur 1", "2025/01/20", "10:00", "réservé"),
            # ("Terrain 2", "Salle B", 30, "Utilisateur 2", "2025/01/21", "11:00", "disponible"),
            #("Terrain 3", "Salle C", 25, "Utilisateur 3", "2025/01/22", "14:00", "réservé"),
           
            ("Terrain 4", "Salle A", 20, "Utilisateur 4", "2025/01/22", "10:00", "réservé"),
            ("Terrain 5", "Salle B", 30, "Utilisateur 5", "2025/01/23", "11:00", "disponible"),
            ("Terrain 6", "Salle C", 25, "Utilisateur 6", "2025/01/24", "14:00", "réservé"),
            ("Terrain 7", "Salle A", 20, "Utilisateur 7", "2025/01/25", "10:00", "réservé"),
            ("Terrain 8", "Salle B", 30, "Utilisateur 8", "2025/01/26", "11:00", "disponible"),
            ("Terrain 9", "Salle C", 25, "Utilisateur 9", "2025/01/27", "14:00", "réservé"),
            ("Terrain 10", "Salle A", 20, "Utilisateur 10", "2025/01/28", "10:00", "réservé"),
            ("Terrain 11", "Salle B", 30, "Utilisateur 11", "2025/01/30", "11:00", "disponible"),
            ("Terrain 12", "Salle C", 25, "Utilisateur 12", "2025/01/31", "14:00", "réservé"),
            ("Terrain 13", "Salle A", 20, "Utilisateur 13", "2025/02/01", "10:00", "réservé"),
            ("Terrain 14", "Salle B", 30, "Utilisateur 14", "2025/02/21", "11:00", "disponible"),
            ("Terrain 14", "Salle C", 25, "Utilisateur 15", "2025/02/22", "14:00", "réservé"),
            ("Terrain 15", "Salle A", 20, "Utilisateur 16", "2025/02/20", "10:00", "réservé"),
            ("Terrain 16", "Salle B", 30, "Utilisateur 17", "2025/02/21", "11:00", "disponible"),
            ("Terrain 17", "Salle C", 25, "Utilisateur 18", "2025/02/22", "14:00", "réservé"),
            ("Terrain 18", "Salle A", 20, "Utilisateur 19", "2025/02/20", "10:00", "réservé"),
            ("Terrain 19", "Salle B", 30, "Utilisateur 20", "2025/02/21", "11:00", "disponible"),
            ("Terrain 20", "Salle C", 25, "Utilisateur 21", "2025/02/22", "14:00", "réservé"),
        ]
        query = """
        INSERT INTO reservations (terrain, salle, capacite, nom_utilisateur, date_reservation, heure_reservation, etat)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.executemany(query, data)
        self.conn.commit()

    def reserver_salle(self, data):
        terrain, salle, capacite, nom_utilisateur, date_reservation, heure_reservation = data

        # Vérification de la disponibilité de la salle
        print(f"Vérification de la disponibilité pour: terrain={terrain}, salle={salle}, date={date_reservation}, heure={heure_reservation}")

        query_check_reservation = """
        SELECT * FROM reservations 
        WHERE terrain = ? AND salle = ? AND capacite = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'réservé'
        """
        cursor = self.conn.execute(query_check_reservation, (terrain, salle, capacite, date_reservation, heure_reservation))
        reservation_existante = cursor.fetchone()
        print(f"reservation_existante: {reservation_existante}")
        if reservation_existante:
          print("La salle est déjà réservée")
          return "Salle déjà réservée"

    # Vérifier si la salle est disponible
        query_check_disponible = """
        SELECT * FROM reservations 
        WHERE terrain = ? AND salle = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'disponible'
        """
        cursor = self.conn.execute(query_check_disponible, (terrain, salle, date_reservation, heure_reservation))
        salle_disponible = cursor.fetchone()
        print(f"salle_disponible: {salle_disponible}")

        if not salle_disponible:
          print("La salle n'est pas disponible")
          return "Salle non disponible"
        
        salle_disponible = cursor.fetchone()
    # Si la salle est disponible, effectuer la réservation
        query_update = """
        UPDATE reservations
        SET etat = 'réservé', nom_utilisateur = ?, capacite = ?
        WHERE terrain = ? AND salle = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'disponible'
        RETURNING id; 
        """
        self.conn.execute(query_update, (nom_utilisateur, capacite, terrain, salle, date_reservation, heure_reservation))
        reservation_id = cursor.fetchone()[0]
        self.conn.commit()

        print("Réservation réussie")
        return f"Réservation réussie ! L'ID de la réservation est : {reservation_id}"
    def reserver_salle1(self, data):
        terrain, salle, capacite, nom_utilisateur, date_reservation, heure_reservation = data

        # Vérification de la disponibilité de la salle
        query_check_reservation = """
        SELECT * FROM reservations 
        WHERE terrain = ? AND salle = ? AND capacite = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'réservé'
        """
        cursor = self.conn.execute(query_check_reservation, (terrain, salle, capacite, date_reservation, heure_reservation))
        reservation_existante = cursor.fetchone()
        if reservation_existante:
            return "Salle déjà réservée"

        # Vérifier si la salle est disponible
        query_check_disponible = """
        SELECT * FROM reservations 
        WHERE terrain = ? AND salle = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'disponible'
        """
        cursor = self.conn.execute(query_check_disponible, (terrain, salle, date_reservation, heure_reservation))
        salle_disponible = cursor.fetchone()
        if not salle_disponible:
            return "Salle non disponible"

        # Si la salle est disponible, effectuer la réservation
        query_update = """
        UPDATE reservations
        SET etat = 'réservé', nom_utilisateur = ?, capacite = ?
        WHERE terrain = ? AND salle = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'disponible'
        RETURNING id;
        """
        cursor = self.conn.execute(query_update, (nom_utilisateur, capacite, terrain, salle, date_reservation, heure_reservation))
        reservation_id_row = cursor.fetchone()
        if reservation_id_row is None:
            return "Erreur lors de la réservation"

        self.conn.commit()
        reservation_id = reservation_id_row[0]
        return f"Réservation réussie ! L'ID de la réservation est : {reservation_id}"

    def get_all_reservations(self):
        query = "SELECT * FROM reservations"
        cursor = self.conn.execute(query)
        return cursor.fetchall()
        
    def rechercher_reservation_par_utilisateur(self, nom_utilisateur):
        query = "SELECT * FROM reservations WHERE nom_utilisateur = ?"
        cursor = self.conn.execute(query, (nom_utilisateur,))
        return cursor.fetchall()

    def rechercher_reservation_par_date(self, date_reservation):
        query = "SELECT * FROM reservations WHERE date_reservation = ?"
        cursor = self.conn.execute(query, (date_reservation,))
        return cursor.fetchall()

        
    def modifier_reservation(self, reservation_id, etat):
        query = "UPDATE reservations SET etat = ? WHERE id = ?"
        self.conn.execute(query, (etat, reservation_id))
        self.conn.commit()
    def get_salles_disponibles(self, date, heure):
        query = """
        SELECT * 
        FROM reservations 
        WHERE date_reservation = ? AND heure_reservation = ? AND etat = 'disponible'
        """
        cursor = self.conn.execute(query, (date, heure))
        result = cursor.fetchall()

        # Retourner les résultats sous forme de liste de dictionnaires
        if result:
            return [{"ID": r[0], "Terrain": r[1], "Salle": r[2], "Capacité": r[3], "Utilisateur": r[4],
                "Date": r[5], "Heure": r[6], "État": r[7]} for r in result]
        else:
          return None
     def reserver_salle2(self, data):
        terrain, salle, capacite, nom_utilisateur, date_reservation, heure_reservation = data

        # Vérification de la disponibilité de la salle
        query_check_reservation = """
        SELECT * FROM reservations 
        WHERE terrain = ? AND salle = ? AND capacite = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'réservé'
        """
        cursor = self.conn.execute(query_check_reservation, (terrain, salle, capacite, date_reservation, heure_reservation))
        reservation_existante = cursor.fetchone()
        
        if reservation_existante:  # Si une réservation existe déjà
            return "Salle déjà réservée"

        # Vérifier si la salle est disponible
        query_check_disponible = """
        SELECT * FROM reservations 
        WHERE terrain = ? AND salle = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'disponible'
        """
        cursor = self.conn.execute(query_check_disponible, (terrain, salle, date_reservation, heure_reservation))
        salle_disponible = cursor.fetchone()
        
        if salle_disponible is None:  # Si aucune salle disponible n'est trouvée
            return "Salle non disponible"

        # Si la salle est disponible, effectuer la réservation
        query_update = """
        UPDATE reservations
        SET etat = 'réservé', nom_utilisateur = ?, capacite = ?
        WHERE terrain = ? AND salle = ? AND date_reservation = ? AND heure_reservation = ? AND etat = 'disponible'
        RETURNING id;
        """
        cursor = self.conn.execute(query_update, (nom_utilisateur, capacite, terrain, salle, date_reservation, heure_reservation))
        reservation_id_row = cursor.fetchone()
        
        if reservation_id_row is None:  # Si la mise à jour échoue pour une raison quelconque
            return "Erreur lors de la réservation"

        # Validation et enregistrement
        self.conn.commit()
        reservation_id = reservation_id_row[0]
        return f"Réservation réussie ! L'ID de la réservation est : {reservation_id}"
