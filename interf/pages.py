from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
#from kivymd.app import MDApp
#from kivymd.uix.pickers import MDDatePicker

#self classes
from citoyen.citoyen import Citoyen, Criminel


class AccueilScreen(Screen):
    pass


class ListeCitoyensScreen(Screen):

    def affiche_citoyens(self):
        # Récupérer la liste des citoyens
        liste = Citoyen.recupere_liste_citoyen()
        print(liste)

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
        nom = self.ids.nom_cit.text
        prenom = self.ids.prenom_cit.text
        nationalite = self.ids.nationalite_cit.text
        adresse = self.ids.adresse_cit.text
        #dateNaiss = self.ids.date_cit.text
        try:
            citoyen = Citoyen(
                nom=nom,
                prenom=prenom,
                nationalite=nationalite,
                adresse=adresse,
                date_naissance="2002-11-21",

            )
            citoyen.ajouter_citoyen()
            self.ids.citValide = "citoyen rajouté"
        except ValueError as e:
            print(e)


class ListeCriminelsScreen(Screen):

    def affiche_criminels(self):
        liste = Criminel.recupere_liste_criminels()
        print(liste)

        criminels_form = [
            {"text": f"{c.nom} {c.prenom} - {c.nationalite} - {c.statut}"} for c in liste
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
        criminel = self.chercher_citoyen()
        num_nat = self.ids.cit_id.text
        criminel.statut = "recherché"
        criminel.ajouter_criminel(num_nat)


class PoliceApp(App):
    def build(self):
        Builder.load_file("pages.raisa")
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(AccueilScreen(name='accueil'))
        sm.add_widget(ListeCitoyensScreen(name='liste_citoyens'))
        sm.add_widget(AjouterCitoyen(name='ajoutCitoyen'))
        sm.add_widget(EnqueteForm(name='form'))
        sm.add_widget(ListeCriminelsScreen(name='liste_criminels'))
        sm.add_widget(AjouterCriminel(name='ajoutCriminel'))


        return sm


if __name__ == '__main__':
    PoliceApp().run()
