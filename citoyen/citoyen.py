from datetime import  date, datetime
import sqlite3

from docutils.nodes import address


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



    @staticmethod
    def creer_table():
        connexion = sqlite3.connect("citoyen.db")
        cursor = connexion.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS citoyen (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            nationalite TEXT NOT NULL,
            date_naissance DATETIME NOT NULL,
            date_mort DATETIME null,
            adresse TEXT NULL,
            age INTEGER NOT NULL
            )
        """)
        connexion.commit()
        connexion.close()

    def ajouter_citoyen(self):
        "sauvegarder un citoyen dans la db"

        connexion = sqlite3.connect("citoyen.db")
        cursor = connexion.cursor()
        age = self.definir_age() #faire la conversion avant enregistrement
        #date_naiss_str = self.date_naissance.strftime("%Y-/%m-/%d")

        cursor.execute(
            """
            INSERT INTO citoyen(nom, prenom, nationalite, adresse, date_naissance, date_mort, age)
            VALUES (?, ?, ?, ?, ?, ?,?)
            """, (self.nom, self.prenom,self.nationalite, self.adresse, self.date_naissance, self.date_mort, age )
        )
        connexion.commit()
        connexion.close()

    @staticmethod
    def recupere_liste_citoyen():
        connexion = sqlite3.connect("citoyen.db")
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
    def __init__(self,num_nat, nom, prenom, adresse, date_naissance, antecedents, statut):
        super().__init__(num_nat, nom, prenom, adresse, date_naissance)
        self.antecedents = antecedents
        self.statut = statut

