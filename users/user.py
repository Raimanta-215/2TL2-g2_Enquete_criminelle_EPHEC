import re

class User:
    liste_users = []

    def __init__(self, nom, prenom, email, mot_de_passe, role, droits_acces=None):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = role
        self.droits_acces = droits_acces if droits_acces else[]


    @classmethod
    def creer_user(cls, admin, nom, prenom, email, mot_de_passe, role, droits_acces=None):
        """
        Créer un nouvel utilisateur grace à son adresse mail professionnelle vérifiée par un mdp

        PRE : - pour créer un utilisateur il faut être administrateur

        POST : - un nouvel utilisateur est ajouté à la liste et une confirmation est retorunée

        RAISE : -  PermissionError si l'utilisateur n'est pas administrateur.
                 - ValueError si l'email existe déjà ou si des champs sont manquants.

        """
        if admin.role != "administrateur":
            raise PermissionError("Vous n'etes pas admin")

        if not nom or not prenom or not email or not mot_de_passe:
            raise ValueError("tout les champs doivent être remplis")

        if any(u.email == email for u in cls.liste_users):
            raise ValueError(f"Un utilisateur avec l'email {email} existe déjà.")

        new_user = cls(nom, prenom, email, mot_de_passe, role, droits_acces)
        cls.liste_users.append(new_user)

        return new_user

    @staticmethod
    def valider_mdp( mot_de_passe):
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

    def modifier_mdp(self, ancien_mdp, nouv_mdp):
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


        if ancien_mdp != self.mot_de_passe:
            raise ValueError("ancien mdp est incorrect")

        if ancien_mdp == nouv_mdp:
            raise ValueError("nouveau mdp doit être différent de l'ancien")

        if not User.valider_mdp(nouv_mdp):
            raise ValueError('critères pas respectées')

        self.mot_de_passe = nouv_mdp
        return "modification enregistrée"


    def double_authentification(self, code):
        """
        Fait une double authentification grâce à un code d'accès.

        PRE : - email : adresse mail de l'user pour l'identification
             - code : user doit exister pour posseder un code

        POST : - return une validation

        RAISES: - si le code est erroné , ValueError

        """
        key = 123
        if code != key:
            raise ValueError("Echec de la double authentification")
        return "Connecté"

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
        return action in self.droits_acces


class Inspecteur(User):
    def __init__(self, nom, prenom, email, mot_de_passe, droits_acces=None):
        super().__init__(nom, prenom, email, mot_de_passe, role="inspecteur", droits_acces=droits_acces)