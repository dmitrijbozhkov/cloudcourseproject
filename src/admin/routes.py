""" Admin tasks to manage site """
from flask import Blueprint

admin = Blueprint("admin", "admin", url_prefix="/admin")

def newest_complaints():
    """ See newest article complaints """
    pass

def article_complaints():
    """ See article's complaints """
    pass

def mark_complaint():
    """ Mark complaint as fullfilled or declined """
    pass

def suspend_article():
    """ Make article suspended """
    pass