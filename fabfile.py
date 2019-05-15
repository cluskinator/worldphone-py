# -*- coding: utf-8 -*-

import os
from fabric.api import task, lcd, env, local, sudo
# import fabric_gunicorn as gunicorn


''' Fabfile commands that work properly (run these from the root of the repo):

    To start the application with newrelic:
        fab -f deploy/fabfile.py newrelic_start
    To stop the running app:
        fab -f deploy/fabfile.py dev stop_app
'''


project = "theworldphone.com"

env.user = ''
env.hosts = ['']

nginx_conf = '''# /etc/nginx/sites-enabled/default
server {
    listen 80 default_server;
    listen [::]:80 default_server ipv6only=on;

    server_name localhost;

    location / {
        proxy_pass         http://localhost:5000;

            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_set_header    X-Originating-IP    $remote_addr;
            proxy_set_header    HTTP_REMOTE_ADDR    $remote_addr;
            proxy_set_header    REMOTE_ADDR         $remote_addr;
    }
}'''


@task
def init():
    """
    Setup virtual env, database and run!
    """
    with(lcd('/root/.virtualenvs')):
        print(os.getcwd())
        local("virtualenv phone")
    local("pip install -r requirements.txt")
    local("mkdir tmp")
    local("mkdir tmp/instance")
    local("python manage.py initdb")

    with open("/etc/nginx/sites-enabled/default", 'w') as nginx_file:
        nginx_file.write(nginx_conf)
    sudo('service nginx restart')
    # start_app()


@task
def dev():
    env.user = 'root'
    env.hosts = ['localhost']
    env.gunicorn_bind = '127.0.0.1:5000'
    env.gunicorn_wsgi_app = 'app_wsgi'
    env.remote_workdir = '/root/theworldphone.com'
    env.virtualenv_dir = '/root/.virtualenvs/phone'
    env.gunicorn_workers = 1
    env.gunicorn_pidpath = env.remote_workdir + '/deploy/gunicorn.pid'


# @task
# def deploy():
#     local('hg pull')
#     local('hg update')
#     restart()


def create_database():
    """Creates role and database"""
    db_user = 'ss'
    db_pass = 'ss'
    db_table = 'manekineko'
    sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\'"' %
        (db_user, db_pass), user='postgres')
    sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"' % (db_table, db_user), user='postgres')


def d():
    """
    Debug.
    """
    reset()
    local("python manage.py runserver")


# def babel():
#     """
#     Babel compile.
#     """
#     local("pybabel extract -F ../lurcat/config -k lazy_gettext -o messages.pot lurcat")
#     local("pybabel init -i messages.pot -d lurcat/translations -l es")
#     local("pybabel init -i messages.pot -d lurcat/translations -l en")
#     local("pybabel compile -f -d lurcat/translations")


def reset():
    """
    Reset local debug env.
    """
    clean()
    local("mkdir /tmp/instance")
    local("python manage.py initdb")


@task
def clean():
    local("rm -rf /tmp/instance")
    local("rm -rf /root/.virtualenvs/phone")


def apt_get(*packages):
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)
