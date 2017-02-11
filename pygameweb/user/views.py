from flask import Blueprint, render_template, abort, redirect, url_for, request, Response

from pygameweb.user.models import User, Group
from pygameweb.wiki.forms import WikiForm

user_blueprint = Blueprint('user',
                           __name__,
                           template_folder='../templates/')


# http://flask-sqlalchemy-session.readthedocs.org/en/v1.1/
from flask_sqlalchemy_session import current_session

# https://flask-security-fork.readthedocs.io/en/latest/customizing.html#views
# https://flask-security-fork.readthedocs.io/en/latest/quickstart.html#id1

from flask_security import Security, login_required
from flask_security.utils import get_identity_attributes
from flask_security.datastore import SQLAlchemyDatastore, UserDatastore


# create a SQLAlchemyUserDatastore which doesn't use a flask db session.
# inside create app.
class PretendFlaskSQLAlchemyDb(object):
    """ This is a pretend db object, so we can just pass in a session.
    """
    def __init__(self, session):
        self.session = session

class SQLAlchemyUserDatastore(SQLAlchemyDatastore, UserDatastore):
    """A SQLAlchemy datastore implementation for Flask-Security that assumes the
    use of the Flask-SQLAlchemy extension.
    """
    def __init__(self, db, user_model, role_model):
        SQLAlchemyDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def get_user(self, identifier):
        if self._is_numeric(identifier):
            return self.db.session.query(self.user_model).get(identifier)
        for attr in get_identity_attributes():
            query = getattr(self.user_model, attr).ilike(identifier)
            rv = self.db.session.query(self.user_model).filter(query).first()
            if rv is not None:
                return rv

    def _is_numeric(self, value):
        try:
            int(value)
        except (TypeError, ValueError):
            return False
        return True

    def find_user(self, **kwargs):
        return self.db.session.query(self.user_model).filter_by(**kwargs).first()

    def find_role(self, role):
        return self.db.session.query(self.role_model).filter_by(name=role).first()


class SQLAlchemySessionUserDatastore(SQLAlchemyUserDatastore):
    """A SQLAlchemy datastore implementation for Flask-Security that assumes the
       use of the flask_sqlalchemy_session extension.
    """
    def __init__(self, session, user_model, role_model):
        SQLAlchemyUserDatastore.__init__(self,
                                         PretendFlaskSQLAlchemyDb(session),
                                         user_model,
                                         role_model)





@user_blueprint.route('/home')
@login_required
def home():
    # app.user_datastore.create_user(email='renesd@gmail.com', password='password')
    # current_session.commit()
    return render_template('base.html')



def add_user_blueprint(app):
    """ to the app.
    """
    app.user_datastore = SQLAlchemySessionUserDatastore(current_session, User, Group)

    security = Security(app, app.user_datastore)

    from flask_security import user_confirmed
    @user_confirmed.connect_via(app)
    def when_the_user_is_confirmed(app, user):
        """ we can add a newbie role.

        After a couple of hours we can add a 'member' role.
        The idea is to combat spam a bit.
        """

        # we add a newbie role, once the user confirms their email.
        # default_role = app.user_datastore.find_role("newbie")
        # app.user_datastore.add_role_to_user(user, default_role)
        # current_session.commit()


    app.register_blueprint(user_blueprint)