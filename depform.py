from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class DepForm(FlaskForm):
    chief = IntegerField('Chief Id', validators=[DataRequired()])
    title = StringField('Department title', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    submit = SubmitField('Submit')
