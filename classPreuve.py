from datetime import datetime


class Preuve:
    def __init__(self, id_preuve, type_preuve, categorie, description, emplacement, image, date_decouverte):
        """
        Initialise une nouvelle instance de la classe Preuve.

        :param id_preuve: int, Identifiant unique de la preuve.
        :param type_preuve: str, Type de la preuve.
        :param categorie: str, Catégorie de la preuve.
        :param description: str, Description de la preuve.
        :param emplacement: str, Lieu où la preuve a été trouvée.
        :param image: str, Chemin ou URL de l'image de la preuve.
        :param date_decouverte: str, Date de découverte de la preuve au format 'DD-MM-YYYY'.

        PRE: - 'id_preuve' est entier positif
             - 'date_decouverte' est chaine au format 'DD-MM-YYYY'
        POST: - preuve initialisée avec valeurs fournies
        """

        if not isinstance(id_preuve, int) or id_preuve <= 0:
            raise ValueError("id_preuve doit être un entier positif.")

        # Conversion de la date
        try:
            date_decouverte_str = datetime.strptime(date_decouverte, "%d-%m-%Y")
        except ValueError:
            raise ValueError("La date doit être au format 'DD-MM-YYYY'.")

        self.id_preuve = id_preuve
        self.type_preuve = type_preuve
        self.categorie = categorie
        self.description = description
        self.emplacement = emplacement
        self.image = image
        self.date_decouverte = date_decouverte_str
        self.analyses = []  # Liste pour stocker les analyses associées
        self.suspects = []  # Liste pour stocker les suspects associés

    def ajouter_preuve(self, type_preuve, description, emplacement, image, date_decouverte):
        """
        ajout nouvelle preuve

        PRE: - arguments sont des chaine non vide et 'date_decouverte' doit être sous format "DD-MM-YYYY"
        POST: - preuve ajouter avec les valeurs fournies
        """
        if not all(isinstance(arg, str) and arg for arg in [type_preuve, description, emplacement, image]):
            raise ValueError("type_preuve, description, emplacement, et image doivent être des chaînes non vides.")

        try:
            date_obj = datetime.strptime(date_decouverte, "%d-%m-%Y")
        except ValueError:
            raise ValueError("La date doit être au format 'DD-MM-YYYY'.")

        self.type_preuve = type_preuve
        self.description = description
        self.emplacement = emplacement
        self.image = image
        self.date_decouverte = date_obj
        print("Preuve ajoutée avec succès.")

    def modifier_preuve(self, type_preuve=None, categorie=None, description=None, emplacement=None, image=None, date_decouverte=None):
        """
        Modifier les info d'une preuve

        PRE: - arguments fournis sont des chaines et 'date_decouverte' est au format DD-MM-YYYY
        POST: - attributs de preuve mis à jour avec nouvelles valeurs fournies
        """
        if type_preuve is not None:
            self.type_preuve = type_preuve
        if categorie is not None:
            self.categorie = categorie
        if description is not None:
            self.description = description
        if emplacement is not None:
            self.emplacement = emplacement
        if image is not None:
            self.image = image
        if date_decouverte is not None:
            try:
                self.date_decouverte = datetime.strptime(date_decouverte, "%d-%m-%Y")
            except ValueError:
                raise ValueError("La date doit être au format 'DD-MM-YYYY'.")
        print("Preuve modifiée avec succès.")

    def ajouter_analyse(self, analyse):
        """
        ajouter analyse à la liste

        PRE: -analyse est un dictionnaire contenant clé 'type' et 'resultat'
        POST: -analyse ajouter a la liste des analyses

        """
        if not isinstance(analyse, dict) or 'type' not in analyse or 'resultat' not in analyse:
            raise ValueError("L'analyse doit être un dictionnaire contenant les clés 'type' et 'resultat'.")
        self.analyses.append(analyse)
        print("Analyse ajoutée:", analyse)

    def change_etat_analyse(self, index, nouvel_etat):
        """
        Changer état d'une analyse spécifique

        PRE: - index est entier valide dans la liste des analyses
             - nouvel_etat est chaine non vide
        POST: - état de l'analyse à l'indice spécifié est modifié
        """
        if not (0 <= index < len(self.analyses)):
            raise IndexError("Index d'analyse invalide.")
        if not isinstance(nouvel_etat, str) or not nouvel_etat:
            raise ValueError("Le nouvel état doit être une chaîne non vide.")

        self.analyses[index]['etat'] = nouvel_etat
        print(f"État de l'analyse {index} changé à {nouvel_etat}.")

    def associer_suspect(self, suspect):
        """
        associer un suspect

        PRE: - argument doit être une chaine non vide
        POST: - suspect ajouté a la liste suspects
        """
        if not isinstance(suspect, str) or not suspect:
            raise ValueError("Le suspect doit être une chaîne non vide.")
        self.suspects.append(suspect)
        print(f"Suspect associé: {suspect}")

    def afficher_preuve(self):
        """
        Affiche tous les détails de la preuve.

        Postconditions:
        - Les informations de la preuve sont affichées.
        """
        print(f"ID Preuve: {self.id_preuve}")
        print(f"Type de Preuve: {self.type_preuve}")
        print(f"Catégorie: {self.categorie}")
        print(f"Description: {self.description}")
        print(f"Emplacement: {self.emplacement}")
        print(f"Image: {self.image}")
        print(f"Date de Découverte: {self.date_decouverte.strftime('%d-%m-%Y')}")
        print("Analyses détaillées :")
        for analyse in self.analyses:
            print(f"  - Type: {analyse.get('type')}, Résultat: {analyse.get('resultat')}")
        print("Suspects associés:", ", ".join(self.suspects))
