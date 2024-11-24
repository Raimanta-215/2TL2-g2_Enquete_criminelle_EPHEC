#kiwi lib
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView

#self classes
from citoyen.citoyen import Citoyen


Window.clearcolor = (182/255,208/255,226/255,1)

class AccueilScreen(Screen):
    pass

class ListeCitoyensScreen(Screen):

    def affiche_citoyens(self):
        liste = Citoyen.recupere_liste_citoyen()

        citoyens_form = []
        for c in liste:
            citoyens_form.append([f"{c.nom_complet()} - {c.nationalite}"])

        for citoyen in citoyens_form:
            self.ids.rv_citoyens.data = [citoyen]

    def on_pre_enter(self):
        self.affiche_citoyens()


class PipiApp(App):
    def build(self):
        Builder.load_file("pages.raisa")
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(AccueilScreen(name='accueil'))
        sm.add_widget(ListeCitoyensScreen(name='liste_citoyens'))

        return sm

if __name__ == '__main__':
    Citoyen.creer_table()

    # Ajouter un citoyen
    citoyen1 = Citoyen(
        nom="Dupont",
        prenom="Jean",
        nationalite="Française",
        adresse="123 Rue de Paris",
        date_naissance="1980-01-01"
    )
    citoyen1.ajouter_citoyen()
    print("Citoyen ajouté avec succès.")

    # Ajouter un autre citoyen
    citoyen2 = Citoyen(
        nom="Smith",
        prenom="Anna",
        nationalite="Américaine",
        adresse="456 Avenue des États-Unis",
        date_naissance="1990-05-12"
    )
    citoyen2.ajouter_citoyen()
    print("Citoyen ajouté avec succès.")

    PipiApp().run()