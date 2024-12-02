from datetime import  date, datetime
import sqlite3
from db.db import tout_creer





class Citoyen :
    def __init__(self, nom, prenom, nationalite, adresse,  date_naissance: date, date_mort = "vivant"):
        self.nom = nom
        self.prenom = prenom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.date_mort = date_mort
        self.adresse = adresse

    def nom_complet(self):
        """Retourne le nom complet de la personne."""
        return f"{self.nom} {self.prenom}"

    def definir_age(self):
        """
        Calcule l'age d'une personne en fonction de son age et de la date du jour


        """
        if not isinstance(self.date_naissance, str):
            raise TypeError("format doit etre str YYYY-MM-DD")

        date_naissance = datetime.strptime(self.date_naissance, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - date_naissance.year
        if today < date(today.year, date_naissance.month, date_naissance.day):
            age -= 1
        return age



    def ajouter_citoyen(self):
        "sauvegarder un citoyen dans la db"
        try:
            connexion = sqlite3.connect("db/enquete.db")
            cursor = connexion.cursor()
            age = self.definir_age() #faire la conversion avant enregistrement
            date_naiss_str = self.date_naissance.strftime("%Y-/%m-/%d")

            cursor.execute(
                """
                INSERT INTO citoyen(nom, prenom, nationalite, adresse, date_naissance, date_mort, age)
                VALUES (?, ?, ?, ?, ?, ?,?)
                """, (self.nom, self.prenom,self.nationalite, self.adresse, self.date_naissance, self.date_mort, age )
            )
            connexion.commit()
            connexion.close()
            print(f"Le citoyen {self.nom_complet()} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)


    @staticmethod
    def recupere_liste_citoyen():
        connexion = sqlite3.connect("db/enquete.db")
        cursor = connexion.cursor()
        cursor.execute("SELECT * FROM citoyen")
        tuples = cursor.fetchall()
        connexion.close()

        citoyens = [
            Citoyen(
                nom=row[0],prenom=[1], nationalite=[2],adresse=[3],
                date_naissance=[4], date_mort=[5]

            )
            for row in tuples
        ]
        return citoyens


class Criminel(Citoyen) :
    def __init__(self, cId, nom, prenom, nationalite, adresse, date_naissance, antecedents, statut):
        super().__init__( nom, prenom, nationalite, adresse, date_naissance)
        self.cId = cId #clé étrangère qui lie au citoyen
        self.antecedents = antecedents
        self.statut = statut

    def creer_criminel(self):
        """sauvegarder le criminel dans la db """
        try:
            connexion = sqlite3.connect("db/enquete.db")
            cursor = connexion.cursor()

            cursor.execute(
                """
                INSERT INTO criminel(cId, statut)
                VALUES (?, ?)
                """, (self.cId, self.statut)
            )
            connexion.commit()
            connexion.close()
            print(f"Le criminel {self.nom_complet()} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)

    def afficher_antecedents(self):
        """afficher les antécédents du criminel depuis db criminel_enquete"""
        try:
            connexion = sqlite3.connect("db/enquete.db")
            cursor = connexion.cursor()

            cursor.execute("SELECT * FROM criminel_enquete WHERE cId = ?", (self.cId,))
            result = cursor.fetchall()
            connexion.close()

            if result:
                antecedents = result[0]
                print(f"Antécédents de {self.nom_complet()} : {antecedents}")
            else:
                print(f"Aucun antécédent trouvé pour {self.nom_complet()}")
        except sqlite3.OperationalError as e:
            print(e)
        


    def ajouter_crime(self, enquete):
        """
        Associe un criminel à un crime dans une enquête

        PRE:
        POST:

        """


    def modifier_criminel(self):







class Victime(Citoyen):
    pass

class Temoin(Citoyen):
    pass

class Suspect(Citoyen):
    pass

class Expert(Citoyen):
    pass

class Inspecteur(Citoyen):
    pass
