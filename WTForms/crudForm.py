from flask_wtf import FlaskForm
from wtforms import SubmitField

class CRUDForm(FlaskForm):
    createReview = SubmitField("CREATE_REVIEW")
    readReview = SubmitField("READ_REVIEW")
    updateReview = SubmitField("UPDATE_REVIEW")
    deleteReview = SubmitField("DELETE_REVIEW")
    logout = SubmitField("LOGOUT")