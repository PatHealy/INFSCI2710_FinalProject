# INFSCI2710_FinalProject

## What you need to do to get this thing running

Assuming you want to run this as a developer and don't care about being secure right now, you need to start up a PostgreSQL server with the following parameters:

- POSTGRES_URL = "127.0.0.1:5432"
- POSTGRES_USER = "postgres"
- POSTGRES_PW = "pw"
- POSTGRES_DB = "final_project"

Next, you need to create the database and populate it. Run the following sql files (found in the /sql folder):

- Final Project Database.sql
- indexes.sql
- triggers.sql
- views.sql
- inserts.sql

Next, get the flask server up and running! It's recommended you do this in a virtual environment. Run these two lines (in Mac or Linux):

- export FLASK_APP=app.py
- flask run

Now the flask server is running, so you can access it in a web browser, at the url it gives you. 