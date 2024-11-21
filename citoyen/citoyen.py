from datetime import datetime, date

class Citoyen :
    def __init__(self, nom, prenom, nationalite, adresse,  date_naissance, date_mort = "vivant"):
        self.nom = nom
        self.prenom = prenom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.date_mort = date_mort
        self.adresse = adresse

    def definir_age(self):
        """
        Calcule l'age d'une personne en fonction de son age et de la date du jour


        """
        today = date.today()
        age = today.year - self.date_naissance.year
        if today < date(today.year, self.date_naissance.month, self.date_naissance.day):
            age -= 1
        return age

    def nom_complet(self):
        complet = 'f{self.nom} {self.prenom}'

        return complet



class Criminel(Citoyen) :
    def __init__(self,num_nat, nom, prenom, adresse, date_naissance, antecedents, statut):
        super().__init__(num_nat, nom, prenom, adresse, date_naissance)
        self.antecedents = antecedents
        self.statut = statut

