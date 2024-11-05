from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Liste fictive des enquêtes pour simuler une base de données
enquetes = [
    {
        'numEnquete': '001',
        'titreEnquete': 'Enquête A',
        'description': 'Description de l\'enquête A',
        'dateDebut': '2024-01-01',
        'victime': 'Victime A',
        'suspect': 'Suspect A',
        'temoin': 'Témoin A',
        'preuve': 'Preuve A',
        'inspecteur': 'Inspecteur A',
        'statut': 'En cours'
    },
    # Ajouter plus d'enquêtes si nécessaire
]

@app.route('/')
def index():
    return render_template('index.html', enquetes=enquetes)

@app.route('/create_enquete', methods=['GET', 'POST'])
def create_enquete():
    if request.method == 'POST':
<<<<<<< Updated upstream
        # Récupérer les informations du formulaire
        num_enquete = request.form['numEnquete']
        titre = request.form['titreEnquete']
        description = request.form['description']
        date_debut = request.form['dateDebut']
        statut = request.form['statut']
        victime = request.form['victime']
        suspect = request.form['suspect']
        temoin = request.form['temoin']
        preuve = request.form['preuve']
        inspecteur = request.form['inspecteur']

        # Créer un dictionnaire pour représenter l'enquête
        enquete = {
            'numEnquete': num_enquete,
            'titreEnquete': titre,
            'description': description,
            'dateDebut': date_debut,
            'statut': statut,
            'victime': victime,
            'suspect': suspect,
            'temoin': temoin,
            'preuve': preuve,
            'inspecteur': inspecteur,
=======
        new_enquete = {
            'numEnquete': request.form['numEnquete'],
            'titreEnquete': request.form['titreEnquete'],
            'description': request.form['idDescription'],
            'dateDebut': request.form['dateDebut'],
            'victime': request.form['victime'],
            'suspect': request.form['suspect'],
            'temoin': request.form['temoin'],
            'preuve': request.form['preuve'],
            'inspecteur': request.form['inspecteur'],
            'statut': request.form['statut']
>>>>>>> Stashed changes
        }
        enquetes.append(new_enquete)
        return redirect(url_for('index'))
    return render_template('create_enquete.html')

@app.route('/edit_enquete/<int:enquete_id>', methods=['GET', 'POST'])
def edit_enquete(enquete_id):
    enquete = enquetes[enquete_id]

    if request.method == 'POST':
        enquete['numEnquete'] = request.form['numEnquete']
        enquete['titreEnquete'] = request.form['titreEnquete']
        enquete['description'] = request.form['idDescription']
        enquete['dateDebut'] = request.form['dateDebut']
        enquete['victime'] = request.form['victime']
        enquete['suspect'] = request.form['suspect']
        enquete['temoin'] = request.form['temoin']
        enquete['preuve'] = request.form['preuve']
        enquete['inspecteur'] = request.form['inspecteur']
        enquete['statut'] = request.form['statut']
        return redirect(url_for('index'))

    return render_template('edit_enquete.html', enquete=enquete, enquete_id=enquete_id)

if __name__ == '__main__':
    app.run(debug=True)
