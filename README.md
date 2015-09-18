# DeMo: A De-motivational Demo

 DeMo is an app to keep your ego in check. It's also a simple Flask-SQL demo app that's styled with [Materialize](http://materializecss.com/).

 If you'd like to use this demo application to **learn how to use uWSGI and NGINX** start at the **"How to Deploy Flask on NGINX with uWSGI"** section.

### Install DeMo App
*****


1. Clone this repo

 ```
 $ git clone https://github.com/karishay/de_mo.git
 ```

2. Install dependancies in a virturalenv

 ```
 $ cd de_mo/
 $ virtualenv de_mo_env
 $ source de_mo_env/bin/activate
 $ pip install -r /<path>/<to>/requirements.txt
 ```

3. Set your credentials and tell your computer where to find them
 * Create a config file in your project directory
   ```
   $ cd /<path_to_project>/de_mo
   $ vi de_mo_config.cfg
   ```
  * Add your secrets to *de_mo_config.cfg*

     ```
     DATABASE='/tmp/de_mo.db'
     SECRET_KEY='something_super_secret'
     DEBUG=True
     USERNAME='a_name_for_a_user'
     PASSWORD='don't_make_it_password'
     ```

 * In your terminal, tell your computer where to find your secrets.

    ```
    $ export DE_MO_SETTINGS=/<path_to_project>/de_mo_config.cfg
    ```

4. Set up your database

    * Install sqlite3 (don't judge me...)

     ```
     $ sudo apt-get install sqlite3
     ```

   * Then pipe the schema file into the sqlite3 database
     (make sure you have the path correct!)

     ```
     $ sqlite3 /tmp/de_mo.db < schema.sql
     ```

5. Run the script from the project directory

   ```
   $ python de_mo.py
   ```


### How to Deploy Flask on NGINX with uWSGI
*******

1. Set up a server. (I'm using DigitalOcean)

    Then ssh access as root user and make a 'uwsgi' user with sudo privalleges.
    ```
    $ ssh root@<ip.address.of.server>
    $ adduser uwsgi
    $ gpasswd -a uwsgi sudo
    ```

    Log out of root user and ssh in as uwsgi user.
    ```
    $ exit
    $ ssh uwsgi@<ip.address.of.server>
    ```

    Download ALL THE THINGS (you need for your application, uwsgi and nginx servers)
    ```
    $ sudo apt-get update
    $ sudo apt-get install python-pip python-dev
    $ sudo apt-get install git
    $ sudo apt-get install nginx
    ```

2. Create a Virtual Environment
  (NOTE: make sure to install virtualenv outside of your project directory)
  ```
  $ sudo pip install virtualenv
  ```

3. Get your project code

  Follow the installation instructions at the **Install DeMo App** section (or your own app install procedure)

    If you haven't already, create a virtualenv inside your project directory, then activate it and install dependencies.
    ```
    $ cd <project_dir>
    $ virtualenv project_env
    $ source project_env/bin/activate
    $ pip install -r requirements.txt
    ```


4. Install uWSGI and create a WSGI entry point
  (NOTE: You must be inside your project directory and have your virtualenv active)

  ```
  $ pip install uwsgi
  ```

  Create a `wsgi.py` file and include the following:
  `$ vi ~/<project_dir>/wsgi.py`

  ```
  from <project_name> import application

  if __name__ == "__main__":
      application.run()
  ```

  Check to see if uWSGI is serving your app:
  ```
  $ uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi
  ```

  You should see the index page of your application when you navigate your browser to <ip.address.of.server>:8000

  After admiring your glory, close your uWSGI server and **deactivate your virtualenv**.

6. Configuring uWSGI

  Create a `project.ini` file in your project directory
  ```
  $ vi ~/de_mo/de_mo.ini
  ```
  Add the following to your ini script:
  ```
  [uwsgi]
  module = wsgi

  master = true
  processes = 5

  socket = project.sock
  chmod-socket = 660
  vacuum = true

  die-on-term = true
  ```

7. Create Upstart script

  This script runs the launch of your application server and uwsgi (?)
  ```
  $ sudo vi /etc/init/project.conf
  ```

  Add the following to your upstart script:
  ```
  description "uWSGI server instance configured to serve project"

  start on runlevel [2345]
  stop on runlevel [!2345]

  setuid user
  setgid www-data

  env PATH=/home/user/project/projectenv/bin
  chdir /home/user/project
  exec uwsgi --ini project.ini
  ```

  Start the upstart script
  `$ sudo start project`

8. Configuring NGINX
  Add a new configuration file to the */etc/nginx/conf.d/* directory
  `$ vi /etc/nginx/conf.d/<project>.conf`

  Add a server block directive to your shiny new nginx configuration file
  ```
  server {
    listen 80;
    server_name <your_ip_address>;

    location / {
      include uwsgi_params;
      uwsgi_pass unix:/home/<user>/<project>/<project>.sock;
    }
  }
  ```

  restart NGINX with `service nginx restart`

### Debugging Hints
*****

Trying to run it locally and getting s 500 error?
  - Double check that you've activated the virtualenv and installed all the dependancies using
    `$ pip install -r requirements.txt`
  - Double check that you've told your computer where to find your secrets
    `$ export DE_MO_SETTINGS=/<path_to>/<file_you_just_made>/de_mo_config.cfg`
  - Double check your database schema has been loaded
    `$ sqlite3 /tmp/de_mo.db < schema.sql`

Trying to test uWSGI is working but getting an error saying no application found?
  - Does your main flask application have this anywhere: ` app = Flask(__name__) `
    uWSGI's naming convention is different from Flask, but close enough to be irritating. If you opt to call your application anything other than `application` you need to let uWSGI know what the *callable* name of the application is. You can either:
      * change all instances of `app` in your project files to `application` OR
      * pass a *callable* parameter (probably `app`) to uWSGI in this call:
        `$ uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi:<callable_name>`
        And let your upstart script know the *callable* name by adding this line to the `<project>.ini` script
        `callable = app`


Trying to run it with Upstart + uWSGI + NGINX configured and getting a 500 error?
  - Everything you do to set up your application manually in your local environment needs to happen in your upstart script.
    - Is your server aware of the virtualenv you've set up? Make sure your /etc/init/<project>.conf script has added the path to your virtual env:

    in `/etc/init/de_mo.conf` check these lines are correct:
    ```
    env PATH=$PATH:/home/<user>/<project>/<project_env>/bin
    env DE_MO_SETTINGS=/home/<user>/<project>/<project>_config.cfg
    ```

Got local deploy working but running into issues with uWSGI and NGINX?
  - What user are you on your server? Did you log in as root and put your project folder + files under the root user directory?

  The root directory has specific permissions and when uWSGI or Upstart tries to access it to set up the server it will run into permissions issues. This is for your protection.
    - Set up a user for your uWSGI server to use and give it sudo permissions.
    - Make sure all your project files are in place where this user can access them with correct permissions.
    - Make sure all your paths have been set correctly in your Upstart script (and everywhere else too)
