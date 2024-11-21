from datetime import datetime, date
from citoyen.citoyen import Criminel

class Enquete:

    liste_enquetes = []

    def __init__(self, id_enquete: int, nom_enquete: str, lieu: str, date_o: datetime = None,
                 type_crime: str = "", statut: str = "ouvert", description: str = ""):
        self.id_enquete = id_enquete
        self.nom_enquete = nom_enquete
        self.lieu = lieu
        self.date_o = date_o if date_o else date.today()
        self.date_f = None
        self.type_crime = type_crime
        self.statut = statut
        self.description = description


        self.liste_preuves = []
        self.liste_temoins = []
        self.liste_victimes = []
        self.liste_criminels = []
        self.liste_suspects = []

    @classmethod
    def creer_enquete(cls, id_enquete: int, nom_enquete: str, lieu: str,type_crime: str, description: str):
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

        RAISES :-ValueError si l'ID existe déjà, indique que l'enquete existe et redemande un nouvel ID

        """
        for e in cls.liste_enquetes:
            if e.id_enquete == id_enquete:
                raise ValueError(f"L'ID {id_enquete} correspond à l'enquête {e.nom_enquete}. Insérez un nouveaux.")

        nouvelle_enquete = cls(
            id_enquete=id_enquete,
            nom_enquete=nom_enquete,
            lieu=lieu,
            type_crime=type_crime,
            description=description,
        )
        cls.liste_enquetes.append(nouvelle_enquete)

        return nouvelle_enquete

    def ajouter_coupable(self, criminel: Criminel):
        """
        Ajouter un criminel à la liste des criminels de l'enquete associée

        PRE : - criminel : Objet de la classe Criminel

        POST : - rajoute un criminel à la liste des criminels de l'enquete

        RAISES : - ValueError si le criminel existe deja, on indique qu'il y est

        """

        for c in self.liste_criminels:
            if c.num_nati == criminel.num_nat:
                raise ValueError(f"Le criminel {criminel.nom_complet} est deja associé")

        self.liste_criminels.append(criminel)

