# -*- coding: utf-8 -*-
"""
    theworldphone.modules.chimp.services
    ~~~~~~~~~~~~~~~~

    chimp module controllers
"""

import json
import mailchimp
from flask import jsonify

from flask import Blueprint, request, current_app


chimp = Blueprint('chimp', __name__, url_prefix='/mailchimp')


@chimp.route('/subscribe/', methods=['GET', 'POST'])
def subscribe(list_id=None):
    '''Adds user to Theworldphone mailing list.

    :param list_id: ID of Mailchimp list to subscribe user to.
    :type list_id: string.
    :returns: JSON object containing response string.
    :raises: mailchimp.ListAlreadySubscribedError, mailchimp.Error.
    '''

    data = json.loads(request.data)
    list_id = 'bf774de909'
    email = data['email']

    try:
        m = mailchimp.Mailchimp(current_app.config['MAILCHIMP_API_KEY'])
        if not list_id:
            lists = m.lists.list()
            if lists:
                list_id = lists['data'][0]['id']
        m.lists.subscribe(list_id, {'email': email})
        resp = "You subscribed."
    except mailchimp.ListAlreadySubscribedError:
        resp = "That email is already subscribed."
    except mailchimp.Error as e:
        resp = 'An error occurred: %s - %s' % (e.__class__, e)

    return jsonify({'result': resp})
