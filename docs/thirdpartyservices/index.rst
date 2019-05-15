********************
Third-Party Services
********************

TheWorldPhone utilizes the following third-party services:

=========
MailChimp
=========

MailChimp is an email marketing service provider.  MailChimp's features allow TheWorldPhone to send e-mails to users for user registration or lost passwords.

API Set-Up
^^^^^^^^^^

In order to set up MailChimp API for deployment, you must register for a `MailChimp API key
<http://mailchimp.com/>`_. Once you've registered, enter your API key into the appropriate field of the config file located at:

.. code-block:: shell
    
    theworldphone.com/theworldphone/config/local.cfg

======
Twilio
======

The WorldPhone uses the Twilio API to facilitate VOIP calling. Twilio's voice application stack is designed for "instant scale, flexibility, and cost-effective communications."

API Set-Up
^^^^^^^^^^

In order to set up Twilio API for deployment, you must register for a `Twilio API key
<https://www.twilio.com/try-twilio>`_. Once you've registered, enter your:

 - account_sid
 - auth_token
 - application_sid
 - old_application_sid

into the appropriate lines of the config file located at:


.. code-block:: shell
    
    theworldphone.com/theworldphone/config/local.cfg

Pricing
^^^^^^^

The Twilio API is priced based on usage.  You can view their full pricing information `here
<https://www.twilio.com/voice/pricing>`_.

======================
Virtual Private Server
======================
A virtual private server (VPS) is a virtual machine sold as a service by an Internet hosting service. A VPS runs its own copy of an operating system, and customers have superuser-level access to that operating system instance, so they can install almost any software that runs on that OS.

We recommend deploying the application through a VPS in order to save time and money.  There are many companies which sell virtual private servers. CuttleSoft uses `Digital Ocean 
<https://www.digitalocean.com/?refcode=293df6cdfd6d>`_.
