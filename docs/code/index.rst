****
Code
****

======
app.py
======

App.py handles the creation and configuration of the flask application and its extensions.

The WorldPhone uses the following extensions.:

 - `Flask-SQLAlchemy`_
 - `Flask-Mail`_
 - `Flask-Cache`_
 - `Login Manager`_

Check out the documentation for those extensions in order to better understand the details of their configuration in app.py.

.. _Flask-SQLAlchemy: https://pythonhosted.org/Flask-SQLAlchemy/
.. _Flask-Mail: https://pythonhosted.org/flask-mail/
.. _Flask-Cache: https://pythonhosted.org/Flask-Cache/
.. _Login Manager: https://flask-login.readthedocs.org/en/latest/

=======
Modules
=======
.. toctree::
   :maxdepth: 1

   admin
   api
   call
   frontend
   mailchimp
   settings
   user