from flask.ext.wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField
)

from wtforms import validators
from wtforms.fields.html5 import EmailField


class ArticleForm(Form):
    title = StringField(
        'Title', [validators.data_required(u'Please enter a title.')],
        description={'placeholder': 'Please enter a title.'}
    )
    content = TextAreaField(
        'Content', [validators.data_required(u'Please enter a content.')],
        description={'placeholder': 'Please enter a content'}
    )
    author = StringField(
        'Author',
        [validators.data_required(u'Please enter your name.')],
        description={'placeholder': 'Please enter your name.'}
    )
    category = StringField(
        'Category',
        [validators.data_required(u'Please enter a category')],
        description={'placeholder': 'Please enter a category'}
    )


class CommentForm(Form):
    author = StringField(
        'Author',
        [validators.data_required(u'Please enter your name.')],
        description={'placeholder': 'Please enter your name.'}
    )
    email = StringField(
        'Email',
        [validators.data_required(u'Please enter your email.'),
         validators.Email(
         message=u'Invalid email address.')],
        description={'placeholder': 'Please enter your email.'}
    )
    content = TextAreaField(
        'Content', [validators.data_required(u'Please enter a content.')],
        description={'placeholder': 'Please enter a content.'}
    )
    password = StringField(
        'Password',
        [validators.data_required('Please enter password.')],
        description={'placeholder': 'Please enter password.'}
    )


class JoinForm(Form):
    email = EmailField(
        u'Email',
        [validators.data_required(u'Please enter your email.')],
        description={'placeholder:Please enter your name.'}
    )
    password = PasswordField(
        u'Password',
        [validators.data_required(u'Please enter password.'),
        validators.EqualTo(
            'confirm_password', message=u'Password does not match')],
        description={'placeholder': 'Please enter password again.'}
    )
    confirm_password = PasswordField(
        u'Confirm Password',
        [validators.data_required(u'Please enter password again.')],
        description={'placeholder': 'Please enter password again.'}
    )
    name = StringField(
        u'Name',
        [validators.data_required(u'Please enter your name.')],
        description={'placeholder': u'Please enter your name.'}
    )


class LoginForm(Form):
    email = EmailField(
        u'Email',
        [validators.data_required(u'Please enter your email.')],
        description={'placeholder:Please enter your name.'}
    )
    password = PasswordField(
        u'Password',
        [validators.data_required(u'Please enter password.')],
        description={'placeholder': 'Please enter password again.'}
    )
