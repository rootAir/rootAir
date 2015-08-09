#<<<<<<< HEAD

=> Features
Import of bank itau statement file
Groups expenses by cost center
Provision and cost reserves to maintain a steady financial turnover
Get tasks in trello e send to google spreadsheet as a report

Motivation
Do not worry about the expenses and keep costs in order.

## How to Use
Django API with Django Rest Framework and AngularJS-Resource
This sample project is the companion of a blog post on how to get started with Django Rest Framework and AngularJS.

Dependencies

To setup and run the sample code, you're going to need npm from NodeJS available to install the frontend code.

Setup

You're encouraged to setup a virtualenv to work in prior to configuring the dependencies.

Install Python Requirements

pip install -r requirements.txt
python setup.py develop
Install Bower + Grunt

npm install -g grunt-cli bower
Install Assets

npm install
bower install
Compile Assets

grunt
Setup the Database

make create_database; make make_fixtures
Run the Server

./manage.py runserver



python-getting-started
A barebones Python app, which can easily be deployed to Heroku.

This application support the Getting Started with Python on Heroku article - check it out.

Running Locally

Make sure you have Python installed properly. Also, install the Heroku Toolbelt and Postgres.

$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started
$ pip install -r requirements.txt
$ createdb python_getting_started
$ foreman run python manage.py migrate
$ python manage.py collectstatic
$ foreman start web
Your app should now be running on localhost:5000.

Deploying to Heroku

$ heroku create
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku open
Documentation

For more information about using Python on Heroku, see these Dev Center articles:
 ==== 
 
# thinkster-django-angular-boilerplate

## Installation

* `$ git clone git@github.com:brwr/thinkster-django-angular-boilerplate.git`
* `$ mkvirtualenv thinkster-djangular`
* `$ cd thinkster-django-angular-boilerplate/`
* `$ pip install -r requirements.txt`
* `$ npm install`
* `$ bower install`
* `$ python manage.py migrate`
* `$ python manage.py runserver`

## Deployment

*NOTE: Requires [Heroku Toolbelt](https://toolbelt.heroku.com/).*

heroku apps:create;
heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git;
heroku config:set DEBUG=False;
heroku config:set COMPRESS_ENABLED=True;
git push heroku master;

* `$ git push heroku master`
* `$ heroku open`

 ====

To use this project, follow these steps:

1. Create your working environment.
2. Install Django (`$ pip install django`)
3. Create a new project using this template

## Creating Your Project

Using this template to create a new Django app is easy::

    $ django-admin.py startproject --template=https://github.com/heroku/heroku-django-template/archive/master.zip --name=Procfile helloworld

You can replace ``helloworld`` with your desired project name.

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [django-postgrespool](https://warehouse.python.org/project/django-postgrespool/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
=======

#>>>>>>> 6f7a1aa3d0f59fe841d8fff1d953505005d8f007
