from datetime import datetime
from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.lang import Builder
import os
from citoyen.citoyen import Citoyen, Criminel


class AccueilScreen(Screen):
    pass


class ListeCitoyensScreen(Screen):

    def affiche_citoyens(self):
        # Récupérer la liste des citoyens
        liste = Citoyen.recupere_liste_citoyen()

        citoyens_form = [
            {"text": f"{c.nom} {c.prenom} - {c.nationalite}"} for c in liste
        ]

        # Mettre à jour les données de la RecyclerView
        self.ids.rv_citoyens.data = citoyens_form

    def on_pre_enter(self):
        self.affiche_citoyens()



class EnqueteForm(Screen):
    pass


class AjouterCitoyen(Screen):
    def sauvegarder_citoyen(self):
        print(self.ids.nom_cit.text)
        nom = self.ids.nom_cit.text.upper().rstrip()
        prenom = self.ids.prenom_cit.text.upper().rstrip()
        nationalite = self.ids.nationalite_cit.text.upper().rstrip()
        adresse = self.ids.adresse_cit.text.upper().rstrip()
        date_mort = self.ids.date_mort_cit.text.upper().strip()
        dateNaiss = self.ids.date_naissance_cit.text.strip()
        date_good = "1111-11-11"
        try:
            date = datetime.strptime(dateNaiss, "%Y/%m/%d")
            date_good = date.strftime("%Y-%m-%d")

        except ValueError:
            print("format invalide")


        try:
            citoyen = Citoyen(
                nom=nom,
                prenom=prenom,
                nationalite=nationalite,
                adresse=adresse,
                date_naissance=date_good,
                date_mort=date_mort

            )
            citoyen.ajouter_citoyen()
            self.ids.citValide = "citoyen rajouté"
        except ValueError as e:
            print(e)


class ListeCriminelsScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.liste_raw = list(Criminel.recupere_liste_criminels())

    def affiche_criminels(self):
        print(self.liste_raw)
        criminels_form = list(map(
            lambda c: {
                "text": f"{c.nom_complet} - {c.nationalite} - {c.date_mort}" if c.date_mort == "vivant"
                else f"{c.nom_complet} - {c.nationalite} - date de mort : {c.date_mort}"},
            self.liste_raw

        ))
        self.ids.rv_criminels.data = criminels_form

    def filtre_criminels(self):
        liste = filter(lambda c: c.date_mort == "vivant", self.liste_raw)
        criminels_form = [
            {"text": f"{c.nom} {c.prenom} - {c.nationalite} - {c.statut} - {c.date_mort}"} for c in liste
        ]
        self.ids.rv_criminels.data = criminels_form

    def on_pre_enter(self):
        self.affiche_criminels()

class AjouterCriminel(Screen):

    def chercher_citoyen(self):

        num_nat = self.ids.cit_id.text
        print(num_nat)
        try:
            criminel = Criminel.charger_criminel_depuis_db(num_nat)
            self.ids.affiche_cit.text = f"{criminel.nom} {criminel.prenom} - {criminel.nationalite} - {criminel.statut}"
            return criminel
        except ValueError as e:
            print(e)

    def ajouter_criminel(self):
        try:

            criminel = self.chercher_citoyen()

            if not criminel:
                self.ids.affiche_cit.text = "echec de l'ajout, pa de citoyen trouvé"
                return

            num_nat = self.ids.cit_id.text.strip()
            if not num_nat:
                self.ids.affiche_cit.text = "num national requis"

            criminel.statut = "recherché"
            criminel.ajouter_criminel(num_nat)
            self.ids.affiche_cit.text = f"criminel {criminel.nom} {criminel.prenom} - {criminel.nationalite} - {criminel.statut}"

            print(criminel)
        except ValueError as e:
            print(e)
            self.ids.affiche_cit.text = "impossible d'ajouter crimininel"



class PoliceApp(App):
    def build(self):
        Builder.load_file(os.path.join(os.path.dirname( os.path.dirname( __file__ )), "interf", "pages.raisa"))
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(AccueilScreen(name='accueil'))
        sm.add_widget(ListeCitoyensScreen(name='liste_citoyens'))
        sm.add_widget(AjouterCitoyen(name='ajoutCitoyen'))
        sm.add_widget(EnqueteForm(name='form'))
        sm.add_widget(ListeCriminelsScreen(name='liste_criminels'))
        sm.add_widget(AjouterCriminel(name='ajoutCriminel'))
        dropdown = DropDown()


        return sm


if __name__ == '__main__':
    PoliceApp().run()
