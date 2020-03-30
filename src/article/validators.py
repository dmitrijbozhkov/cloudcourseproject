""" Form validators for article """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo, NumberRange, URL

BIAS_CHOICES = [
    (0, "Extreme left"),
    (1, "Left"),
    (2, "Center left"),
    (3, "Least biased"),
    (4, "Center right"),
    (5, "Right"),
    (6, "Extreme right")
]

class CreateArticle(FlaskForm):
    """ Form validation for creating an article """
    title = StringField("Title", validators=[
        DataRequired("Please enter title")
    ])
    source = StringField("Source", validators=[
        DataRequired("Please add article source"),
        URL(message="Source should be valid url")
    ])
    tags = StringField("tags")
    political_bias = SelectField(
        "political_bias",
        coerce=int,
        choices=BIAS_CHOICES,
        validators=[
            DataRequired("Please give political bias rating"),
        ])
    source_backing = DecimalField("source_backing", validators=[
        DataRequired("Please give source backing rating"),
        NumberRange(min=0, max=10, message="Source backing rating should be between 0 and 10")
    ])
    story_choices = DecimalField("story_choices", validators=[
        DataRequired("Please give story choices rating"),
        NumberRange(min=0, max=10, message="Story choices rating should be between 0 and 10")
    ])
    analysis = HiddenField("analysis", validators=[
        DataRequired("Please type your analysis here")
    ])
    submit = SubmitField("Post")
