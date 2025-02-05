from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class UpdateForm(FlaskForm):
    review = TextAreaField("REVIEW : ", validators=[DataRequired()])
    ratings = IntegerField("RATINGS : ", validators=[DataRequired(), NumberRange(min = 1, max=10, message="Ratings should be between 1 to 10")])
    submit = SubmitField("SUBMIT")