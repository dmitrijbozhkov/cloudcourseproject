""" Main flask configuration """
from flask import Flask, redirect, url_for, session, send_from_directory, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from sqlalchemy import desc
from cloudcourseproject.src.model import db, User, Role, Article
from .celery import celery
from .config import config
from .auth import create_token

app = Flask(__name__)
app.config.update(config)
db.init_app(app)

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
    google_bp = make_google_blueprint(scope=["profile", "email"], redirect_url="/")
    app.register_blueprint(google_bp, url_prefix="/login")
    app.register_blueprint(authorization)

route_factory()

# Configure google signup
# redirect(url_for("google.login"))
def set_google_authorization():
    """ Authorize user through google """
    resp = google.get("/oauth2/v1/userinfo")
    user_info = resp.json()
    if user_info.get("error"):
        session.clear()
        return False
    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        user = User(
            username=user_info["name"],
            email=user_info["email"],
            is_activated=user_info["email_verified"],
            role=Role.query.filter_by(name=config["roles"][0]).first())
    session[config["SESSION_TOKEN"]] = create_token(user)
    return True

@app.route("/", methods=["GET"])
def index():
    """ Landing page """
    newest_articles = Article.query.order_by(desc(Article.post_time)).paginate(1, 10, False)
    if google.authorized and not session.get(config["SESSION_TOKEN"]):
        set_google_authorization()
    return render_template("index.jinja", article_list=newest_articles.items)

@app.route("/static/serve/<path:path>")
def send_js(path):
    return send_from_directory("../static/serve", path)

from cloudcourseproject.src.error_handlers import *

if __name__ == "__main__":
    app.run()