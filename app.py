from flask import Flask, request, redirect, url_for, render_template, session, flash
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'fred1234'
db = SQLAlchemy(app)

# Model pour la table "user"
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    prenom = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, name, prenom, email, password):
        self.name = name
        self.prenom = prenom
        self.email = email
        self.password = password

# Model pour la table "rencontre"
class Rencontre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    prenom = db.Column(db.String(255))
    titre = db.Column(db.String(50))
    ville = db.Column(db.String(100))
    image = db.Column(db.String(255))  # Chemin vers l'image dans le système de fichiers

    def __init__(self, nom, prenom, titre, ville, image):
        self.nom = nom
        self.prenom = prenom
        self.titre = titre
        self.ville = ville
        self.image = image


# Vérifier si la table "user" existe, sinon la créer
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Erreur lors de la création de la table : {e}")

# Charger la page d'accueil
@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html')

# Charger la page d'inscription
@app.route('/showregister', methods=['GET', 'POST'])
def showregister():
    return render_template('register.html')

# Charger la page de connexion
@app.route('/showlogin', methods=['GET', 'POST'])
def showlogin():
    return render_template('login.html')

@app.route('/showlist', methods=['GET', 'POST'])
def showlist():
    return render_template('voir.html')

# Inscription
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']

        try:
            new_user = User(name=name, prenom=prenom, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash("Inscription réussie. Vous pouvez maintenant vous connecter.", "success")
            return redirect(url_for('showlogin'))
        except Exception as e:
            flash(f"Erreur lors de l'inscription : {e}", "error")
            return redirect(url_for('showregister'))

    return render_template('login.html')


#connexion
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            # Vérifier si les données du formulaire sont correctement soumises
            print(f"Email soumis : {email}")
            print(f"Mot de passe soumis : {password}")

            # Vérifier si l'utilisateur existe dans la base de données
            user = User.query.filter_by(email=email, password=password).first()

            if user:
                # Utilisateur trouvé, connecté avec succès
                session['user_name'] = user.name  # Stocker le nom de l'utilisateur en session
                flash("Vous êtes maintenant connecté.", "success")
                return redirect(url_for('index'))
            else:
                # Utilisateur non trouvé ou mot de passe incorrect
                flash("Échec de la connexion. Vérifiez vos informations d'identification.", "error")
                return redirect(url_for('showlogin'))
        except KeyError as e:
            flash(f"Erreur : Champ manquant dans le formulaire. Clé manquante : {e}", "error")
            return redirect(url_for('showlogin'))
        except Exception as e:
            flash(f"Erreur inattendue : {e}", "error")
            return redirect(url_for('showlogin'))

# Afficher la page de rencontre
@app.route('/rencontres')
def rencontres():
    # Vérifier si l'utilisateur est connecté (par exemple, si son nom est stocké dans la session)
    user_name = session.get('user_name')
    
    if user_name:
        # Utilisateur connecté, redirigez-le vers la page rencontres.html
        return render_template('rencontres.html')
    else:
        # Utilisateur non connecté, redirigez-le vers la page de connexion
        return redirect(url_for('showlogin'))
    

#Afficher la liste des rencontres
@app.route('/list_rencontres')
def list_rencontres():
    # Vérifier si l'utilisateur est connecté (par exemple, si son nom est stocké dans la session)
    user_name = session.get('user_name')
    
    if user_name:
        # Utilisateur connecté, redirigez-le vers la page rencontres.html
        return render_template('voir.html')
    else:
        # Utilisateur non connecté, redirigez-le vers la page de connexion
        return redirect(url_for('rencontres'))
    

#Recupérer les données du formulaire du formulaire de rencontre
@app.route('/rencontrer', methods=['POST'])
def rencontrer():
    if request.method == 'POST':
        # Récupérer les informations de l'utilisateur connecté depuis la session
        user_name = session['user_name'] if 'user_name' in session else ""
        user_prenom = session['user_prenom'] if 'user_prenom' in session else ""

        nom = request.form['nom']
        prenom = request.form['prenom']
        titre = request.form['titre']
        ville = request.form['ville']

        # Utilisez les informations de l'utilisateur connecté pour remplir les champs du formulaire par défaut
        nom = nom if nom else user_name
        prenom = prenom if prenom else user_prenom

        # Traitement de l'image si elle a été uploadée
        image = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Enregistrez l'image dans le dossier "images" à la racine du projet
                image_path = os.path.join('images', image_file.filename)
                image_file.save(image_path)
                image = image_path

        try:
            # Créez un nouvel objet Rencontre avec les données du formulaire
            nouvelle_rencontre = Rencontre(nom=nom, prenom=prenom, titre=titre, ville=ville, image=image)
            db.session.add(nouvelle_rencontre)
            db.session.commit()

            flash("Données ajoutée avec succès à la base de données.", "success")
            return redirect(url_for('showlist'))
        except Exception as e:
            flash(f"Erreur lors de l'ajout des données : {e}", "error")
            return redirect(url_for('rencontres'))






# Déconnexion
@app.route('/logout')
def logout():
    session.pop('user_name', None)  # Supprimer le nom de l'utilisateur de la session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
