from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[InputRequired(message='Username field is required.')])
    password = PasswordField(_l('Password'), validators=[InputRequired(message='Password field is required.')])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l("Username"), validators=[InputRequired(message='Username field is required.')])
    email = StringField(_l("Email"), validators=[InputRequired(message='Email field is required.'), Email()])
    password = PasswordField(_l('Password'), validators=[InputRequired(message='Password field is required.')])
    password2 = PasswordField(_l('Repeat Password'),
                              validators=[InputRequired(message='Password field is required.'), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.get_user_by_username(username=username.data)
        if user is not None:
            raise ValidationError(_("User already exists"))

    def validate_email(self, email):
        user = User.get_user_by_email(email=email.data)
        if user is not None:
            raise ValidationError(_("Email Id already exists try to login"))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('email'), validators=[InputRequired(), Email()])
    submit = SubmitField(_l("Request password Reset"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[InputRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset Password'))
