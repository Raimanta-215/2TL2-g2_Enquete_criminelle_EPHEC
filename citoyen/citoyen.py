from datetime import  date, datetime
import sqlite3
import os
from dataclasses import dataclass


CHEMIN = os.path.join(os.path.dirname( os.path.dirname( __file__ )), "interf", "enquete.db")

@dataclass
class Citoyen :
    '''def __init__(self, nom, prenom, nationalite, date_naissance, date_mort = "vivant",adresse = ""):
        self.nom = nom
        self.prenom = prenom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.date_mort = date_mort
        self.adresse = adresse
        '''

    nom: str
    prenom: str
    nationalite: str
    date_naissance: date
    date_mort: str = "vivant"
    adresse: str = None
    antedecent = []

    @property
    def nom_complet(self):
        """Retourne le nom complet de la personne."""
        return f"{self.nom} {self.prenom}"
    @property
    def definir_age(self):
        """
        Calcule l'age d'une personne en fonction de son âge et de la date du jour


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
        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()
            age = self.definir_age  #faire la conversion avant enregistrement
            self.date_naissance = datetime.strptime(self.date_naissance, "%Y-%m-%d")

            cursor.execute(
                """
                INSERT INTO citoyen(nom, prenom, nationalite,  date_naissance, date_mort,adresse, age)
                VALUES (?, ?, ?, ?, ?, ?,?)
                """, (self.nom, self.prenom,self.nationalite, self.date_naissance, self.date_mort, self.adresse.upper(), age )
            )
            connexion.commit()
            connexion.close()
            print(f"Le citoyen {self.nom_complet} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)


    @staticmethod
    def recupere_liste_citoyen():
        connexion = sqlite3.connect(CHEMIN)
        cursor = connexion.cursor()
        cursor.execute("""SELECT * FROM citoyen""")


        for c in cursor:
            print(c)
            yield Citoyen(
                    nom=c[1],prenom=c[2], nationalite=c[3],
                    date_naissance=c[4], date_mort=c[5],adresse=c[6]
                )

        connexion.close()

    def afficher_antecedents(self, cid):
        """afficher les antécédents du citoyen depuis db criminel_enquete"""
        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()
            cursor.execute('''
                           SELECT citoyen.nom, citoyen.prenom, citoyen.nationalite, criminel.idCriminel
                           FROM criminel_enquete
                                JOIN criminel on criminel.idCriminel = criminel_enquete.idCriminel
                                JOIN citoyen on citoyen.cId = criminel.cId
                           WHERE criminel.cId = ?
                           '''
                           , cid)
            result = cursor.fetchall()
            connexion.close()

            if result:
                antecedents = result[0]
                print(f"Antécédents de {self.nom_complet} : {antecedents}")
            else:
                print(f"Aucun antécédent trouvé pour {self.nom_complet}")
        except sqlite3.OperationalError as e:
            print(e)


class Criminel(Citoyen) :
    def __init__(self, nom, prenom, nationalite, adresse, date_naissance, date_mort, statut=None):
        super().__init__( nom, prenom, nationalite, date_naissance, date_mort, adresse)
        self.statut = statut


    @staticmethod
    def charger_criminel_depuis_db(cid):

        connexion = sqlite3.connect(CHEMIN)
        cursor = connexion.cursor()
        cursor.execute("SELECT * FROM citoyen WHERE cId = ?", (cid,))
        data = cursor.fetchone()
        cursor.close()
        connexion.close()
        if data is None:
            raise ValueError(f"Aucun criminel trouvé avec l'ID {cid}")
        return Criminel(
            nom=data[1],
            prenom=data[2],
            nationalite=data[3],
            date_naissance=data[4],
            date_mort=data[5],
            adresse=data[6],
        )



    def ajouter_criminel(self, cid):
        """sauvegarder le criminel dans la db """

        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()

            cursor.execute(
                """
                INSERT INTO criminel(cId, statut)
                VALUES (?, ?)
                """, (cid, self.statut)
            )
            connexion.commit()

            cursor.close()
            connexion.close()

            print(f"Le criminel {self.nom_complet} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(f"Erreur d'intégrité : {e}")

    @staticmethod
    def recupere_liste_criminels():

        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()
            cursor.execute("""
                        SELECT citoyen.nom, citoyen.prenom, citoyen.nationalite, citoyen.adresse,
                               citoyen.date_naissance, citoyen.date_mort, criminel.statut
                        FROM criminel
                        JOIN citoyen ON criminel.cId = citoyen.cId;
                        """)

            for c in cursor:
                print(c)
                yield Criminel(
                        nom=c[0],
                        prenom=c[1],
                        nationalite=c[2],
                        adresse=c[3],
                        date_naissance=c[4],
                        date_mort=c[5],
                        statut=c[6]
                )
            connexion.close()

        except sqlite3.OperationalError as e:
            print(e)
            return []

    def modifier_criminel(self,cid, statut):
        """Modifier le statut du criminel"""

        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()

            query = """UPDATE criminel SET statut = ? WHERE cId = ?"""
            cursor.execute(query, (statut, cid))

            connexion.commit()
            cursor.close()
            connexion.close()

            self.statut = statut
            print(f"Le statut de {self.nom_complet} a été modifier")
        except sqlite3.OperationalError as e:
            print(e)



