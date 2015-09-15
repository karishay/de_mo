# DeMo: A De-motivational Demo

 DeMo is an app to keep your ego in check. It's also a simple Flask-SQL demo app that's styled with [Materialize](http://materializecss.com/).

#### Install DeMo App
*****


* Clone this repo
```
$ git clone https://github.com/karishay/de_mo.git
```

* In the project directory, create a config file (in which we hide our secrets!)
```
$ touch de_mo_config.cfg
```

* Add your secrets to **de_mo_config.cfg**:
```
DATABASE='/<path>/<to>/<database_file>/de_mo.db'
SECRET_KEY='something_super_secret'
DEBUG=True
USERNAME='a_name_for_a_user'
PASSWORD='don't_make_it_password'
```

* In your terminal, tell your computer where to find your secrets.

 ```
 $ export DE_MO_SETTINGS=/<path_to>/<file_you_just_made>/de_mo_config.cfg
 ```

* Then pipe the schema file into the sqlite3 database
  (make sure you have the path correct!)
```
$ sqlite3 /tmp/de_mo.db < schema.sql
```

* Run the script from the project directory
```
$ python de_mo.py
```

#### Get DeMo on NGINX
*****

* Install NGINX

`maybe use some code`

* Unleash onto the internet
