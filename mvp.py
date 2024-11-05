from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

enquetes = []

@app.route('/')
def index():
    return render_template('index.html', enquetes=enquetes)

@app.route('/create_enquete', methods=['GET', 'POST'])
def create_enquete():
    if request.method == 'POST':
        new_enquete = {
            'numEnquete': request.form['numEnquete'],
            'titreEnquete': request.form['titreEnquete'],
            'description': request.form['description'],
            'dateDebut': request.form['dateDebut'],
            'victime': request.form['victime'],
            'suspect': request.form['suspect'],
            'temoin': request.form['temoin'],
            'preuve': request.form['preuve'],
            'inspecteur': request.form['inspecteur'],
            'statut': request.form['statut']
        }
        enquetes.append(new_enquete)
        return redirect(url_for('index'))
    return render_template('create_enquete.html')

@app.route('/modifier_enquete/<int:enquete_id>', methods=['GET', 'POST'])
def modifier_enquete(enquete_id):
    enquete = enquetes[enquete_id]

    if request.method == 'POST':
        enquete['numEnquete'] = request.form['numEnquete']
        enquete['titreEnquete'] = request.form['titreEnquete']
        enquete['dateDebut'] = request.form['dateDebut']
        enquete['victime'] = request.form['victime']
        enquete['suspect'] = request.form['suspect']
        enquete['temoin'] = request.form['temoin']
        enquete['preuve'] = request.form['preuve']
        enquete['inspecteur'] = request.form['inspecteur']
        enquete['statut'] = request.form['statut']
        enquete['description'] = request.form['description']
        return redirect(url_for('index'))

    return render_template('modifier_enquete.html', enquete=enquete, enquete_id=enquete_id)

if __name__ == '__main__':
    app.run(debug=True)
