class Config(object):
    pass


class Production(Config):
    DEBUG = False
    pass

# set the secret key.  keep this really secret:
import os
# os.urandom(24)
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.secret_key = os.urandom(24)
