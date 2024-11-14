from datetime import datetime, date
from multiprocessing.sharedctypes import Value
from typing import re


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

liste_enquetes = []


class Enquete :
    def __init__(self,id_enquete : int, nom_enquete, lieu, date_o : datetime, type_crime, statut, description):
        self.id_enquete = id_enquete
        self.nom_enquete = nom_enquete
        self.lieu = lieu
        self.date_o = date_o
        self.date_f = None
        self.type_crime = type_crime
        self.statut = statut
        self.description = description
        self.liste_preuves = []
        self.liste_temoins = []
        self.liste_victimes = []
        self.liste_criminels = []
        self.liste_suspects = []

    def creer_enquete(self, id_enquete : int, nom_enquete: str, lieu: str, type_crime: str, description: str):

        """
        Créer une enquete dont l'id est unique à chaque enquête avec
            un statut initié "ouvert" à l'ouverture et la date du jour

        PRE : - id_enquete  : un entier positif qui ne peut pas égale à zero
              - nom_enquete : une chaine de caractères
              - lieu : une chaine de caratcères
              - type de crime : chaine de caratcère
              - description : chaine de caratère

        POST : - la nouvelle enquête est crée avec un ID, le statut ouvert , la date
                    le nom, le lieu et la description

        RAISES :- si l'ID existe déjà, indique que l'enquete existe et redemande un nouvel ID
        
        """
        for e in liste_enquetes:
            if e.id_enquete == id_enquete:
                raise ValueError(f"L'ID {id_enquete} correspond à l'enquête {e.nom_enquete}. Insérez un nouveaux.")

        nouvelle_enquete = Enquete(id_enquete, nom_enquete, lieu, description, type_crime)
        liste_enquetes.append(nouvelle_enquete)

        return nouvelle_enquete



    def ajouter_coupable(self, criminel : Criminel):
        """
        Ajouter un criminel à la liste des criminels de l'enquete associée

        PRE : - criminel : Objet de la classe Criminel

        POST : - rajoute un criminel à la liste des criminels de l'enquete

        RAISES : - si le criminel existe deja, on indique qu'il y est

        """

        for c in self.liste_criminels:
                if c.num_nati == criminel.num_nat:
                    raise ValueError(f"Le criminel {criminel.nom_complet} est deja associé")

        self.liste_criminels.append(criminel)

liste_users = []

class User:
    def __init__(self, nom, prenom, email, mot_de_passe, role, droits_acces):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = role
        self.droits_acces = droits_acces



    def creer_user(self, nom, prenom, email, mot_de_passe, role, droits_acces):
        """
        Créer un nouvel utilisateur grace à son adresse mail professionnelle vérifiée par un mdp

        PRE : - pour créer un utilisateur il faut être administrateur

        POST : - un nouvel utilisateur est ajouté à la liste et une confirmation est retorunée

        RAISE : - si le membre du commisariat qui tente de créer un utilisateur
                    n'est pas admin, aucun rajout à la liste users

                - si des valeurs manquent dans les champs, impossible de créer le user

        """
        if self.role != "administrateur":
            raise PermissionError("Vous n'etes pas admin")

        if not nom or not prenom or not email or not mot_de_passe:
            raise ValueError("tout les champs doivent être remplis")

        user = User(nom, prenom, email, mot_de_passe, role, droits_acces)
        liste_users.append(user)

        return user


    def valider_mdp(self, mot_de_passe):
        """
        Verifier et valider que le mot de passe respecte bien la longueur de 12 char, majuscules, chiffres et char speciaux

        PRE : - mot_de_passe : la longueur de 12 char minimum, maj, int, et char spcéciaux

        POST : - return True si tout les critères sont remplis
               - return False dans le cas contraire

        """
        if len(mot_de_passe) < 12:
            return False
        if not re.search("[A-Z]", mot_de_passe):
            return False
        if not re.search("[0-9]", mot_de_passe):
            return False
        if not re.search('[!@#$%^&*(),.?":{}|<>]', mot_de_passe):
            return False
        return True

    def modifier_mdp(self, email, ancien_mdp, nouv_mdp):
        """
        Modifier le mdp d'un user.

        PRE : - ancien_mdp : l'ancien mdp valide
             - nouv_mdp : nouveau mdp qui respecte les critères de validation
             - email : adresse mail de l'user pour l'identification

        POST : - return message de validation et met à jour le mdp en cas de succès

        RAISES : - si l'ancien mdp est erroné , ValueError
                 - si le nouveau mdp est le même que l'ancien , ValueError
                 - si le nouveau mdp ne respecte pas les critères de validation, ValueError

        """
        for u in liste_users:
            if u.email == email:
                if ancien_mdp != self.mot_de_passe:
                    raise ValueError("ancien mdp est incorrect")

                if ancien_mdp == self.mot_de_passe:
                    raise ValueError("nouveau mdp doit être différent de l'ancien")

                if not self.valider_mdp(ancien_mdp):
                    raise ValueError('critères pas respectées')

                self.mot_de_passe = nouv_mdp
                return "modification enregistrée"


    def double_authentification(self, email, code):
        """
        Fait une double authentification grâce à un code d'accès.

        PRE : - email : adresse mail de l'user pour l'identification
             - code : user doit exister pour posseder un code

        POST : - return une validation

        RAISES: - si le code est erroné , ValueError

        """
        for u in liste_users:
            if u.email == email:
                if code != 123:
                    raise ValueError("echec de la double authentification")

                return "double authentification réussie "

    def recevoir_notif(self, enquete):
        """
        Envoyer des notifications des mises à jour des enqêtes aux users en fonction de leur droits

        PRE : - message : contient une alerte de mise à jour d'une des enquêtes
              - enquete :   user doit avoir le droit à l'enquete

        POST : -si le user à les droits sur l'enquete , il recevra les notifications
               - si il a pas les droit , n'envoie rien

        """

        if enquete in self.droits_acces:
            return f"mise a jour de {enquete}"


    def verifier_droit(self, action):
        """verifier si le user à le droit de faire l'action"""
        if action in self.droits_acces:
            return True
        return False


class Inspecteur(User):
    def __init__(self, nom, prenom, email, mot_de_passe,  droits_acces):
        super().__init__(nom, prenom, email, mot_de_passe)