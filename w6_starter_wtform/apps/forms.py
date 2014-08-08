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
        description={'placeholder:Please enter a title.'}
    )
    content = TextAreaField(
        'Content', [validators.data_required(u'Please enter a content.')],
        description={'placeholder:Please enter a content'}
    )
    author = StringField(
        'Author',
        [validators.data_required(u'Please enter your name.')],
        description={'placeholder:Please enter your name.'}
    )
    category = StringField(
        'Category',
        [validators.data_required(u'Please enter a category')],
        description={'placeholder:Please enter a category'}
    )


class CommentForm(Form):
    author = StringField(
        'Author',
        [validators.data_required(u'Please enter your name.')],
        description={'placeholder:Please enter your name.'}
    )
    email = StringField(
        'Email',
        [validators.data_required(u'Please enter your email.'),
         validators.Email(
         message=u'Invalid email address.')],
         description={'placeholder:Please enter your email.'}
    )
    content = TextAreaField(
        'Content', [validators.data_required(u'Please enter a content.')],
        description={'placeholder:Please enter a content'}
    )
    password = StringField(
        'Password',
        [validators.data_required('Please enter password.')],
        description={'placeholder:Please enter password.'}
    )