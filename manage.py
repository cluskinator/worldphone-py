# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from theworldphone import create_app
from theworldphone.extensions import db
from theworldphone.modules.user import User
from theworldphone.modules.user.models import Language


manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
        auth0_user_id='x',
        name=u'admin',
        email=u'admin@example.com',
        password=u'123456',
        role='admin',
        status='active',
        gender='other',
        location=u'US')

    # emily = User(
    #     auth0_user_id='y',
    #     name=u'emily',
    #     email=u'emily@cuttlesoft.com',
    #     password=u'123456',
    #     role='user',
    #     status='active',
    #     gender='female',
    #     location=u'US')
    #
    # frank = User(
    #     auth0_user_id='z',
    #     name=u'frankie',
    #     email=u'frank@cuttlesoft.com',
    #     password=u'123456',
    #     role='user',
    #     status='active',
    #     gender='male',
    #     location=u'CU')

    language_list = [
        'English',
        'Spanish',
        'French',
        'German',
        'Chinese (Mandarin)',
        'Japanese',
        'Arabic',
        'Turkish',
        'Farsi',
        'Hindi',
        'Korean',
        'Portuguese',
        'Russian'
    ]
    for language in language_list:
        Language().create(**{'name': language})

    db.session.add(admin)
    # db.session.add(emily)
    # db.session.add(frank)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
