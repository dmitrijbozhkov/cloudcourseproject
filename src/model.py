""" Database model """
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

article_tag = db.Table("ArticleTag",
    db.Column("article_id", db.Integer, db.ForeignKey("article.article_id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.tag_id"))
)

rated_comment = db.Table("RatedComment",
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("comment_id", db.Integer, db.ForeignKey("comment.comment_id"))
)

class Role(db.Model):
    """ User role model """
    role_id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    rank = db.Column(db.Integer, nullable=False)
    users = db.relationship("User", back_populates="role")


class Tag(db.Model):
    """ Model for article tags """
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    articles = db.relationship("Article", secondary=article_tag)


class User(db.Model):
    """ User model """
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(20))
    is_activated = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"), nullable=False)
    role = db.relationship("Role", back_populates="users", lazy="joined")
    complaints = db.relationship("Complaint", back_populates="user")
    articles = db.relationship("Article", back_populates="user")
    rated_comments = db.relationship("Comment", secondary=rated_comment)


class Complaint(db.Model):
    """ Table for complaints on articles """
    complaint_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)
    is_fullfilled = db.Column(db.Boolean, default=False, nullable=False)
    is_declined = db.Column(db.Boolean, default=False, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("article.article_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    user = db.relationship("User", back_populates="complaints")
    article = db.relationship("Article", back_populates="complaints")


class Article(db.Model):
    """ Article table """
    article_id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(200), unique=True, nullable=False)
    contents = db.Column(db.Text, nullable=False)
    analysis = db.Column(db.Text, nullable=False)
    political_bias = db.Column(db.Float, nullable=False)
    source_backing = db.Column(db.Float, nullable=False)
    story_choices = db.Column(db.Float, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False)
    icon_link = db.Column(db.String())
    is_suspended = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    user = db.relationship("User", back_populates="articles", lazy="joined")
    comments = db.relationship("Comment", back_populates="article")
    tags = db.relationship("Tag", secondary=article_tag)
    complaints = db.relationship("Complaint", back_populates="article")


class Comment(db.Model):
    """ Table for article comments """
    comment_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)
    karma = db.Column(db.Integer, default=0, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("article.article_id"), nullable=False)
    article = db.relationship("Article", back_populates="comments")
    users_rated = db.relationship("Comment", secondary=rated_comment)
    child_comments = db.relationship("CommentTree", primaryjoin="CommentTree.ancestor==Comment.comment_id")


class CommentTree(db.Model):
    """ Comment Hirerarchy """
    ancestor = db.Column(db.Integer, db.ForeignKey("comment.comment_id"), primary_key=True)
    descendant = db.Column(db.Integer, db.ForeignKey("comment.comment_id"), primary_key=True)
    length = db.Column(db.Integer, nullable=False)
    child = db.relationship("Comment", foreign_keys=[descendant])
