************
Introduction
************


=======
Purpose
=======

This document has been provided to give you an understanding of the the inner workings of the project.  It provides an overview of the deployment process. This document also serves as a starting point for your team to develop or modify the code.


=========
Structure
=========

theworldphone.com's codebase is contained in the following folder structure:

.. code-block:: shell

    theworldphone.com
    ├── deploy
    ├── docs
    │   └── modules
    ├── tests
    └── theworldphone
        ├── addons
        │   └── redis
        ├── config
        ├── modules
        │   ├── admin
        │   ├── api
        │   ├── call
        │   ├── frontend
        │   ├── mailchimp
        │   ├── ratings
        │   ├── settings
        │   └── user
        ├── static
        │   ├── common-files
        │   ├── css
        │   ├── flat-ui
        │   ├── img
        │   ├── js
        │   ├── less
        │   ├── uploads
        │   └── vendor
        ├── templates
        │   ├── admin
        │   ├── call
        │   ├── emails
        │   ├── errors
        │   ├── frontend
        │   ├── layouts
        │   ├── macros
        │   ├── settings
        │   └── user
        └── tmp
            └── instance
