*********
Mailchimp
*********

.. automodule:: theworldphone.modules.mailchimp
    :members:

.. function:: get_mailchimp_api(keys_file=None):

    Retrieves Mailchimp api key from config file using SafeConfigParser()

    :param keys_file: File containing API keys.
    :type keys_file: string.
    :returns: Mailchimp API key if one is found, False if no key is found.


======
Views
======

.. autoflask:: theworldphone.app:create_app()
   :undoc-static:
   :blueprints: mailchimpbp