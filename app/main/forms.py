from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, ValidationError, Length
from flask import request
from app.models import User



class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[InputRequired()])
    about_me = TextAreaField(_l("About me"), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l("Update"))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.get_user_by_username(username=username.data)
            if user is not None:
                raise ValidationError(_("User already exists"))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[InputRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Post'))


class EmptyForm(FlaskForm):
    submit = SubmitField(_l('Submit'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False

        super(SearchForm, self).__init__(*args, **kwargs)
