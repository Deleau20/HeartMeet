# Application Web de Rencontre Amoureuse et Amicale

## À propos

Cette application web de rencontre amoureuse et amicale a été développée en utilisant Python avec le framework Flask, SQLAlchemy pour la gestion de la base de données et SQLite3 comme système de gestion de base de données. Elle permet aux utilisateurs de créer des profils, de rechercher des correspondances potentielles en fonction de leurs préférences et de communiquer avec d'autres utilisateurs.

## Prérequis

- Python 3.x installé localement
- Flask et SQLAlchemy installés dans votre environnement Python
- Un navigateur web moderne

## Installation

1. Clonez ou téléchargez ce dépôt.

   ```
   git clone https://github.com/votre-utilisateur/rencontre-amoureuse-web-app.git
   ```

2. Accédez au répertoire du projet.

   ```
   cd rencontre-amoureuse-web-app
   ```

3. Créez un environnement virtuel.

   ```
   python -m venv env
   ```

4. Activez l'environnement virtuel.

   - Sur Windows :

     ```
     env\Scripts\activate
     ```

   - Sur macOS/Linux :

     ```
     source env/bin/activate
     ```

5. Installez les dépendances du projet.

   ```
   pip install -r requirements.txt
   ```

6. Initialisez la base de données SQLite3.

   ```
   python manage.py init_db
   ```

## Utilisation

### Mode de développement

1. Lancez l'application en exécutant la commande suivante :

   ```
   flask run
   ```

2. Accédez à l'application dans votre navigateur à l'adresse `http://localhost:5000`.

3. Créez un compte utilisateur en fournissant les informations requises.

4. Connectez-vous avec vos identifiants.

5. Explorez les fonctionnalités de recherche de correspondances, de messagerie et de gestion de profil.

## Contribution

Les contributions à ce projet sont les bienvenues. Voici comment vous pouvez contribuer :

1. Fork ce dépôt.

2. Créez une branche pour votre fonctionnalité ou correction de bug.

   ```
   git checkout -b fonctionnalite-incroyable
   ```

3. Faites vos modifications et commit.

   ```
   git commit -m "Ajouter une fonctionnalité incroyable"
   ```

4. Push vers votre dépôt forké.

   ```
   git push origin fonctionnalite-incroyable
   ```

5. Créez une Pull Request vers ce dépôt.

## Construit avec

### Langages & Frameworks

- Python - [Site officiel](https://www.python.org)
- Flask - [Documentation](https://flask.palletsprojects.com)
- SQLAlchemy - [Documentation](https://docs.sqlalchemy.org)

### Outils

#### CI

- GitHub Actions - [Documentation](https://docs.github.com/actions)

#### Déploiement

- Pythonanywhere 