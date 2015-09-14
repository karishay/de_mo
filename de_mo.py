import sqlite3
import random
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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def de_motivate():
    name = request.form['name']
    print name
    query_results = g.db.execute('SELECT words, too_mean from De_mos')
    insults = [dict(words=row[0], too_mean=row[1]) for row in query_results.fetchall()]
    random_insult= random.choice(insults)['words']
    print "something"
    return render_template('de_motivation.html', name=name, insult=random_insult)


@app.route('/add_insults', methods=['GET'])
def add_insults_view():
    return render_template('add_insults.html')

@app.route('/add_insults', methods=['POST'])
def add_insults():
    g.db.execute('insert into De_mos (words) values (?)',
                [request.form['insult']])
    g.db.commit()
    flash("New insult added. Mwhahah!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
