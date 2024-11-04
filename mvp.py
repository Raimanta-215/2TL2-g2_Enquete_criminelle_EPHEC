import flask

from flask  import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
#ca marche pas apparemment 
# Stockage temporaire pour les enquêtes
enquetes = []

# Page d'accueil : liste des enquêtes
@app.route('/')
def index():
    return render_template('index.html', enquetes=enquetes)

# Page de formulaire pour créer une nouvelle enquête
@app.route('/create_enquete', methods=['GET', 'POST'])
def create_enquete():
    if request.method == 'POST':
        # Récupérer les informations du formulaire
        num_enquete = request.form['numEnquete']
        titre = request.form['titreEnquete']
        description = request.form['description']
        date_debut = request.form['dateDebut']
        statut = request.form['statut']

        # Créer un dictionnaire pour représenter l'enquête
        enquete = {
            'numEnquete': num_enquete,
            'titreEnquete': titre,
            'description': description,
            'dateDebut': date_debut,
            'statut': statut,
        }

        # Ajouter l'enquête à la liste
        enquetes.append(enquete)
        return redirect(url_for('index'))

    return render_template('create_enquete.html')

if __name__ == '__main__':
    app.run(debug=True)
