""" Article routes """
from flask import Blueprint, render_template, request
from cloudcourseproject.src.article.validators import CreateArticle

article = Blueprint("article", "article", url_prefix="/article")

@article.route("/add", methods=["GET", "POST"])
def add():
    """ Adding article route """
    form = CreateArticle()
    if request.method == "GET" or not form.validate_on_submit():
        return render_template("article/add.jinja", form=form)
    if request.method == "POST":
        print("check")
    raise RuntimeError("Invalid request")

@article.route("/tag/search", methods=["GET"])
def search_tags():
    """ Search tags by name """
    pass

def view_article():
    """ View article by id """
    pass

def search_articles():
    """ Search articles by tags, title and how new it is """
    pass

def make_complaint():
    """ write complaint to the administrators on an article """
    pass

def comment():
    """ write comment on an article """
    pass

def expand_comments():
    """ Expand comment tree """
    pass
