from flask import Blueprint
from ckan.plugins import toolkit

eaw_theme = Blueprint('eaw_theme', __name__)


def help():
    return toolkit.render('home/help.html')


eaw_theme.add_url_rule('/help', view_func=help, endpoint='help')
