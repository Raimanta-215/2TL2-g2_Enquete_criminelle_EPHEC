from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
#from kivy.uix.listview import ListView, ListItemButton
from kivy.properties import ObjectProperty
from  enquete.enquete import Enquete


class EnqueteApp(BoxLayout):
    # Définition des propriétés liées aux widgets
    enquete_list = ObjectProperty()
    nom_input = ObjectProperty()
    lieu_input = ObjectProperty()
    type_crime_input = ObjectProperty()
    description_input = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enquetes = []

    def ajouter_enquete(self):
        """
        Ajoute une enquête à la liste.
        """
        nom = self.nom_input.text
        lieu = self.lieu_input.text
        type_crime = self.type_crime_input.text
        description = self.description_input.text

        if not nom or not lieu or not type_crime or not description:
            return  # Ne rien faire si un champ est vide

        nouvelle_enquete = Enquete(nom, lieu, type_crime, description)
        self.enquetes.append(nouvelle_enquete)

        # Mettre à jour la liste des enquêtes
        self.enquete_list.adapter.data.append(str(nouvelle_enquete))
        self.enquete_list._trigger_reset_populate()

        # Réinitialiser les champs
        self.nom_input.text = ""
        self.lieu_input.text = ""
        self.type_crime_input.text = ""
        self.description_input.text = ""

    def afficher_details(self):
        """
        Affiche les détails de l'enquête sélectionnée.
        """
        selection = self.enquete_list.adapter.selection
        if selection:
            enquete_str = selection[0].text
            enquete = next((e for e in self.enquetes if str(e) == enquete_str), None)
            if enquete:
                details = (
                    f"Nom: {enquete.nom}\n"
                    f"Lieu: {enquete.lieu}\n"
                    f"Type de crime: {enquete.type_crime}\n"
                    f"Description: {enquete.description}"
                )
                # Afficher les détails dans un popup ou un label
                self.ids.details_label.text = details


class EnqueteManagerApp(App):
    def build(self):
        return EnqueteApp()