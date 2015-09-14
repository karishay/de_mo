import sqlite3
from flask import Flask, request, redirect, url_for
from flask import render_template, flash, g
from contextlib import closing

app = Flask(__name__)

app.config.from_envvar('DE_MO_SETTINGS', silent=True)


#========# Database #==========#

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#==========# Routes #==========#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/de_mo')
def de_motivate():
    #query the database for a random insult
    
    #return template with name from form in index passed to insult from db

if __name__ == '__main__':
    app.run()
