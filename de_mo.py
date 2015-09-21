import sqlite3
import random
from flask import Flask, request, redirect, url_for
from flask import render_template, flash, g
from contextlib import closing

application = Flask(__name__)

application.config.from_envvar('DE_MO_SETTINGS', silent=True)


#========# Database #==========#

def connect_db():
    return sqlite3.connect(application.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with application.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def populate_db():
    default_insults = ["... that's a useless as a box of hair.",
                        "... at least your parents will love you.",
                        "... well.. that's not your best idea."]
    for insult in default_insults:
        g.db.execute('insert into De_mos (words) values (?)',
                    [insult])
        g.db.commit()

@application.before_request
def before_request():
    g.db = connect_db()

@application.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


#==========# Routes #==========#

@application.route('/', methods=['GET'])
def index():
    populate_db()
    return render_template('index.html')

@application.route('/', methods=['POST'])
def de_motivate():
    name = request.form['name']
    query_results = g.db.execute('SELECT words from De_mos')
    insults = [dict(words=row[0]) for row in query_results.fetchall()]
    random_insult= random.choice(insults)['words']
    return render_template('de_motivation.html', name=name, insult=random_insult)


@application.route('/add_insults', methods=['GET'])
def add_insults_view():
    return render_template('add_insults.html')

@application.route('/add_insults', methods=['POST'])
def add_insults():
    g.db.execute('insert into De_mos (words) values (?)',
                [request.form['insult']])
    g.db.commit()
    flash("New insult added. Mwhahah!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    application.run(host='0.0.0.0')
    init_db()
