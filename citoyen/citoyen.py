from datetime import  date, datetime
import sqlite3
import os



CHEMIN = os.path.join(os.path.dirname( os.path.dirname( __file__ )), "interf", "enquete.db")


class Citoyen :
    def __init__(self, nom, prenom, nationalite, date_naissance: date, date_mort = "vivant",adresse = ""):
        self.nom = nom
        self.prenom = prenom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.date_mort = date_mort
        self.adresse = adresse


        self.antedecent = []
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
        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()
            age = self.definir_age() #faire la conversion avant enregistrement
            self.date_naissance = datetime.strptime(self.date_naissance, "%Y-%m-%d")

            cursor.execute(
                """
                INSERT INTO citoyen(nom, prenom, nationalite,  date_naissance, date_mort,adresse, age)
                VALUES (?, ?, ?, ?, ?, ?,?)
                """, (self.nom, self.prenom,self.nationalite, self.date_naissance, self.date_mort, self.adresse, age )
            )
            connexion.commit()
            connexion.close()
            print(f"Le citoyen {self.nom_complet()} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)


    @staticmethod
    def recupere_liste_citoyen():
        connexion = sqlite3.connect(CHEMIN)
        cursor = connexion.cursor()
        cursor.execute("""SELECT * FROM citoyen""")
        tuples = cursor.fetchall()
        connexion.close()
        citoyens = []
        for c in tuples:
            print(c)
            citoyens.append(
                Citoyen(
                    nom=c[1],prenom=c[2], nationalite=c[3],
                    date_naissance=c[4], date_mort=c[5],adresse=c[6]
                ))



        return citoyens

    def afficher_antecedents(self):
        """afficher les antécédents du citoyen depuis db criminel_enquete"""
        try:
            connexion = sqlite3.connect(CHEMIN)
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

            cursor.close()
            connexion.close()

            print(f"Le criminel {self.nom_complet()} à été enregistré")
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(f"Erreur d'intégrité : {e}")

    @staticmethod
    def recupere_liste_criminels():
        connexion = sqlite3.connect(CHEMIN)
        cursor = connexion.cursor()
        cursor.execute("""SELECT citoyen.nom, citoyen.prenom, citoyen.age, criminel.statut
                    FROM criminel
                    JOIN citoyen ON criminel.cId = citoyen.cId;""")
        tuples = cursor.fetchall()
        connexion.close()
        criminels = []
        for c in tuples:
            print(c)
            Criminel(
                nom=c[0],
                prenom=c[1],
                date_naissance=c[2],
                statut=c[3]
            )


        return criminels

    def modifier_criminel(self,cId, statut):
        """Modifier le statut du criminel"""

        try:
            connexion = sqlite3.connect(CHEMIN)
            cursor = connexion.cursor()

            query = """UPDATE criminel SET statut = ? WHERE cId = ?"""
            cursor.execute(query, (statut, cId))

            connexion.commit()
            cursor.close()
            connexion.close()

            self.statut = statut
            print(f"Le statut de {self.nom_complet()} a été modifier")
        except sqlite3.OperationalError as e:
            print(e)



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

            print(f"La victime {self.nom_complet()} à été enregistré")

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

            print(f"Le statut de {self.nom_complet()} a été modifier")
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



