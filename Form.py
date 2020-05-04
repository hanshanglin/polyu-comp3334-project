from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,SubmitField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField(u'username', validators=[
                DataRequired(message= u'username length must in 16 '), Length(1, 16)])
    password = PasswordField(u'password', 
                  validators=[DataRequired(message= u'password can not be empty')])
    submit = SubmitField(u'login')

class RegisterForm(FlaskForm):
    username = StringField(u'username', validators=[
                DataRequired(message= u'username length must in 16 '), Length(1, 16)])
    password = PasswordField(u'password', 
                  validators=[DataRequired(message= u'password can not be empty')])
    submit = SubmitField(u'login')