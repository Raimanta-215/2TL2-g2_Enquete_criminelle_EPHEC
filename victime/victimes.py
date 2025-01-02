import sqlite3

from citoyen.citoyen import Citoyen, CHEMIN


class Victime(Citoyen):
    def __init__(self, nom, prenom, nationalite, date_naissance, date_mort, adresse, incident, statut, relation_enquete, date_incident):
        super().__init__( nom, prenom, nationalite, date_naissance, date_mort, adresse)
        self.incident = incident
        self.statut = statut
        self.relation_enquete = relation_enquete
        self.date_incident = date_incident

    def creer_victim(self, cId, eId, cause, idVictime):
        """ creer la victime dans la db"""
        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()
            cursor.execute(
                """
                INSERT INTO victime(cId, statut, incident, date_incident)
                VALUES(?, ?, ?, ?)
                """, (cId, self.statut, self.incident, self.date_incident))

            cursor.execute(
                """
                INSERT INTO victime_enquete(idVictime, eId, cause)
                VALUES(?, ?, ?)
                """, (idVictime, eId, cause)
            )

            cursor.close()
            connexion.commit()
            connexion.close()

            print(f"La victime {self.nom_complet} à été enregistré")

        except sqlite3.OperationalError as e:
            print(e)

        except sqlite3.IntegrityError as e:
            print(f"Erreur d'intégrité : {e}")

    def modifier_statut(self, statut, idVictime):
        """Modifier le statut de la victime"""
        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()

            query = """ UPDATE victime SET statut = ? WHERE idVictime = ?"""
            cursor.execute(query, (query, (statut, idVictime)))

            cursor.close()
            connexion.close()
            connexion.commit()
            self.statut = statut

            print(f"Le statut de {self.nom_complet} a été modifier")
        except sqlite3.OperationalError as e:
            print(e)



    def modifier_incident(self):
        pass


class Temoin(Citoyen):
    pass

class Suspect(Citoyen):
    pass

class Expert(Citoyen):
    pass

class Inspecteur(Citoyen):
    pass



