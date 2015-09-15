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

* Hide your secrets from github:

  ```
  $ vi .gitignore
  ```
  add *de_mo_config.cfg* to your *.gitignore*

  ```
  de_mo_config.cfg
  ~
  ~
  -- INSERT --
  :wq!
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
********

1. Set up a server that will serve your web app (I am using DigitalOcean) and ssh into it
  - `$ ssh root@<ip.address.of.server>`

2. Prep your shiny new server
  - `$ sudo apt-get update`
  - install the base dependencies you'll need for your application (in my case it's:)
    - `$ sudo apt-get install python-pip python-dev `
    - `$ sudo apt-get install git`
  - install nginx
    - `$ sudo apt-get install nginx`

3. Clone your app code and install any dependencies
  - I use virtualenv to keep track of dependencies
    - `$ sudo pip install virtualenv`
  - get your [application](#install) installed
  - install uWSGI and create a WSGI entry point
    - `$ pip install uwsgi`
    - create a *de_mo/wsgi.py* file
      - `$ vi de_mo/wsgi.py`
      - add the following to *wsgi.py*
      - ```
        from de_mo import de_mo

        if __name__ == "__main__":
        application.run()
      ```
      - save and close *wsgi.py*

4. Configure uWSGI server
  - check that uWSGI is running (stuff gets weird here watch out)


#### Get DeMo on NGINX with Docker Images
*****

1. Set up a digital ocean droplet (or whatever equivalent you prefer) and ssh into it
  - `ssh root@<ip.address.of.droplet>`

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
