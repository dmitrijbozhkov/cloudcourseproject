""" Main flask configuration """
from flask import Flask, redirect, url_for, session, send_from_directory, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_wtf.csrf import CSRFProtect
from jinja2 import Environment
from sqlalchemy import desc
from cloudcourseproject.src.model import db, User, Role, Article
from .celery import celery
from .config import config
from .auth import create_token, AuthorizationError, hash_password

app = Flask(__name__)
app.config.update(config)
db.init_app(app)
app.jinja_options["extensions"].append("jinja2.ext.do")
csrf = CSRFProtect()
csrf.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

# Configure celery

class ContextTask(celery.Task):
    """ Run celery tasks in request context """
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

# Configure blueprint routes

def route_factory():
    """ Initialize blueprints in a factory in order to not to deal with circular imports """
    from cloudcourseproject.src.authorization.routes import authorization
    from cloudcourseproject.src.user.routes import user
    from cloudcourseproject.src.article.routes import article
    from cloudcourseproject.src.admin.routes import admin
    google_bp = make_google_blueprint(scope=["profile", "email"], redirect_url="/")
    app.register_blueprint(google_bp, url_prefix="/login")
    app.register_blueprint(authorization)
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(admin)

route_factory()

# Configure google signup
# redirect(url_for("google.login"))
def set_google_authorization():
    """ Authorize user through google """
    resp = google.get("/oauth2/v1/userinfo")
    user_info = resp.json()
    if user_info.get("error"):
        raise AuthorizationError("Can't fetch google account information")
    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        user = User(
            username=user_info["name"],
            email=user_info["email"],
            is_activated=user_info["verified_email"],
            role=Role.query.filter_by(name=config["roles"][0]).first())
        db.session.add(user)
        db.session.commit()
    session.clear()
    session[config["SESSION_TOKEN"]] = create_token(user)
    return user

@app.route("/", methods=["GET"])
def index():
    """ Landing page """
    newest_articles = Article.query.order_by(desc(Article.post_time)).paginate(1, 10, False)
    if session.get(config["SESSION_TOKEN"]):
        return render_template("index.jinja", article_list=newest_articles.items, is_authorized=True)
    if google.authorized and not session.get(config["SESSION_TOKEN"]):
        set_google_authorization()
        return render_template("index.jinja", article_list=newest_articles.items, is_authorized=True)
    return render_template("index.jinja", article_list=newest_articles.items, is_authorized=False)


@app.route("/static/serve/<path:path>")
def send_static(path):
    """ Debug static serve """
    return send_from_directory("../static/serve", path)

@app.before_first_request
def init_database_entities():
    """ Add roles and admin user """
    for i, role_name in enumerate(config["roles"]):
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(
                name=role_name,
                rank=i
            )
        else:
            role.rank = i
        db.session.add(role)
    user = User.query.filter_by(email=config["default_admin"]["email"]).first()
    if not user:
        user = User(
            username=config["default_admin"]["username"],
            email=config["default_admin"]["email"],
            password=hash_password(config["default_admin"]["password"]),
            is_activated=True,
            role=Role.query.filter_by(name=config["roles"][-1]).first()
        )
    else:
        user.username = config["default_admin"]["username"]
        user.password = hash_password(config["default_admin"]["password"])
    db.session.add(user)
    db.session.commit()

from cloudcourseproject.src.error_handlers import *

if __name__ == "__main__":
    app.run()