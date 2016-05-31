# Bringing Buzzwords Home

## Installation
- (Recommended) Set up a virtual environment for this project. If you use virtualenv, the command would be `echo "layout python3" >> .envrc`. You will need to follow up that command with `direnv allow`.
- Ensure that [PostgreSQL is installed](http://www.postgresql.org/download/) (we use [Postgres.app](http://postgresapp.com/) on OS X). Create the database you wish to use with this project.
- Clone this git repository: `git clone https://github.com/Bringing-Buzzwords-Home/bringing_buzzwords_home.git` (If you use SSH it's `git clone git@github.com:Bringing-Buzzwords-Home/bringing_buzzwords_home.git`)
- Run `pip install -r requirements.txt`
- [Set an environment variable for your database.](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup) Run `export DATABASE_URL=postgres:///DATABASE_NAME` where DATABASE_NAME is the name of your local database. Add that line to your bash profile if you wish the environment variable to be loaded in every session.
- Set an environment variable for django's SECRET_KEY. Run `export SECRET_KEY=<YOUR_SECRET_KEY>` where YOUR_SECRET_KEY is the secret key you devise.
- Run `python manage.py make migrations visualize` and `python manage.py migrate` to tell Django to set up its tables in the database.

## How to Use
- Run `python manage.py runserver` to start the webserver.
- Navigate to [127.0.0.1:8000](http://127.0.0.1:8000) to view the app.
