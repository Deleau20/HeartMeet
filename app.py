from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'fred1234'
db = SQLAlchemy(app)

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

            return redirect(url_for('index'))
        except Exception as e:
            return 'Error: {}'.format(e)

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
                return redirect(url_for('index'))
            else:
                # Utilisateur non trouvé ou mot de passe incorrect
                return "Échec de la connexion. Vérifiez vos informations d'identification."
        except KeyError as e:
            return f"Erreur : Champ manquant dans le formulaire. Clé manquante : {e}"
        except Exception as e:
            return f"Erreur inattendue : {e}"

    return redirect(url_for('showlogin'))



# Déconnexion
@app.route('/logout')
def logout():
    session.pop('user_name', None)  # Supprimer le nom de l'utilisateur de la session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
