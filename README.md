# DeMo: A De-motivational Demo

 DeMo is an app to keep your ego in check. It's also a simple Flask-SQL demo app that's styled with [Materialize](http://materializecss.com/).

#### Install DeMo App
*****


* Clone this repo

  ```
  $ git clone https://github.com/karishay/de_mo.git
  ```

* Create a virturalenv

  ```
  $ pip install virturalenv
  $ virtualenv de_mo
  $ source de_mo/bin/activate
  $ pip install -r /<path>/<to>/requirements.txt
  ```

* In the project directory, create a config file (in which we hide our secrets!)

  ```
  $ cd /<path>/<to>/de_mo
  $ touch de_mo_config.cfg
  ```

* Add your secrets to *de_mo_config.cfg*

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

* Install sqlite3 (don't judge me...)

  ```
  $ apt-get install sqlite3
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
********

1. Set up a server that will serve your web app (I am using DigitalOcean) and ssh into it
  - `$ ssh root@<ip.address.of.server>`

2. Prep your shiny new server
  - `$ sudo apt-get update`
  - install the base dependencies you'll need for your application (in my case it's:)
    - `$ sudo apt-get install python-pip python-dev `
    - `$ sudo apt-get install git`
  - install nginx TODO: Add directions for installing latest mainline version
    - `$ sudo apt-get install nginx`

3. Clone your app code and install any dependencies
  - make sure to change into /home directory to avoid root permissions issues
  - I use virtualenv to keep track of dependencies
    - `$ sudo pip install virtualenv`

  - get your [application](#install) installed
    - make sure your virtualenv is activated

  - install uWSGI and create a WSGI entry point
    - `$ pip install uwsgi`
    - in your project directory create a *wsgi.py* file
        ```
        $ cd /<path>/<to>/de_mo
        $ vi wsgi.py
        ```
    - add the following to *wsgi.py*
      ```
      from de_mo import app

      if __name__ == "__main__":
        app.run(host='0.0.0.0')
      ```

4. Configure uWSGI server
  - make sure your virtualenv is activated

    `$ source bin/activate`

  - check that uWSGI is running

    `$ uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi:app`

    open a browser with your ip address and port 8000 and you should see your app's index page

  - deactivate your virtualenv with `$ deactivate`

  - create a uWSGI configuration file called *de_mo.ini* in your app directory

    `$ vi ~/de_mo/de_mo.ini`

    add the following settings to your uWSGI configuration
    ```
    [uwsgi]
    module = wsgi

    master = true
    process = 5

    socket = de_mo.sock
    chmod-socket = 666
    vaccum = true

    die-on-term = true
    ```

5. Create an Upstart Script
  - `$ vi /etc/init/de_mo.conf`

  add the following to your Upstart script

    ```
    # a description of your Upstart Script
    description "uWSGI server configured to serve de_mo"

    #TODO: explain
    start on runlevel [2345]
    stop on runlevel [!2345]

    #TODO: explain
    setuid root
    setgid www-data

    # add the location of your env variables to your path  
    #env PATH=$PATH:/root/de_mo/bin
    chdir /<path_to_project>/de_mo
    exec uwsgi --ini de_mo.ini
    ```
  save and close file then run it with
  `start de_mo`

6. Configure NGINX
  - Add a new configuration file to the */etc/nginx/conf.d/* directory
  `$ vi /etc/nginx/conf.d/de_mo.conf`
    - Add a server block directive to your shiny new nginx configuration file
    ```
    server {
      listen 80;
      server_name <your_ip_address>;

      location / {
        include uwsgi_params;
        uwsgi_pass unix:/root/de_mo/de_mo.sock;
      }
    }
    ```
    - restart NGINX with `service nginx restart`



#### Get DeMo on NGINX with Docker Images
*****

1. Set up a digital ocean droplet (or whatever equivalent you prefer) and ssh into it
  - `ssh user@<ip.address.of.droplet>`
  - NOTE: do not use root user. make a new [user](https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04). 

2. Install [Docker](https://docs.docker.com/installation/ubuntulinux/)

3. Clone the official [docker image](https://blog.docker.com/2015/04/tips-for-deploying-nginx-official-image-with-docker/)
    - create an instance of the nginx docker image
    ```
    $ docker run --name de_mo_nginx -P -d nginx
    ```
    you should see output that ends with something like:
    `
    5323c06b75dc9378b702e54059485cdedefb92c9511a05b9e4cac4462f20b863
    `

     You can check to see that nginx is running by navigating in a browser to the ip address of your droplet with the port number randomly picked by the docker image (which you can find by running `docker ps`)

* Unleash onto the internet
