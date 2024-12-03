#kiwi lib
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView

#self classes
from citoyen.citoyen import Citoyen, Criminel


Window.clearcolor = (182/255,208/255,226/255,1)

class AccueilScreen(Screen):
    pass

class ListeCitoyensScreen(Screen):

    def affiche_citoyens(self):
        # Récupérer la liste des citoyens
        liste = Citoyen.recupere_liste_citoyen()
        print(liste)
        # Formater les citoyens pour l'affichage
        citoyens_form = [
            {"text": f"{c.nom} {c.prenom} - {c.nationalite}"} for c in liste
        ]

        # Mettre à jour les données de la RecyclerView
        self.ids.rv_citoyens.data = citoyens_form

    def on_pre_enter(self):
        self.affiche_citoyens()

class EnqueteForm(Screen):
    pass

class PoliceApp(App):
    def build(self):
        Builder.load_file("pages.raisa")
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(AccueilScreen(name='accueil'))
        sm.add_widget(ListeCitoyensScreen(name='liste_citoyens'))
        sm.add_widget(EnqueteForm(name='form'))

        return sm

if __name__ == '__main__':

    PoliceApp().run()