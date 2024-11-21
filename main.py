from enquete.enquete import Enquete
from interf.interf import EnqueteManagerApp
from users.user import User, Inspecteur


enquete1 = Enquete.creer_enquete(
    id_enquete=1,
    nom_enquete="Enquête Mystère",
    lieu="Paris",
    type_crime="Vol",
    description="Enquête sur un vol mystérieux au musée."
)
print(f"Nom : {enquete1.nom_enquete}, Lieu : {enquete1.lieu}, Statut : {enquete1.statut}")


user = User("Dupont", "Jean", "jean.dupont@example.com", "SecurePass123!", "inspecteur")
# Tentative de modification du mot de passe
try:
    print(user.modifier_mdp("SecurePass123!", "NewPass1234!"))  # Succès
except ValueError as e:
    print(f"Erreur : {e}")

# Validation du nouveau mot de passe
print(user.mot_de_passe)

EnqueteManagerApp().run()