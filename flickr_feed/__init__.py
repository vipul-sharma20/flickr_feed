from flask import Flask

app = Flask(__name__)

# generated by os.urandom(24)
app.secret_key = 'E\xb7?-\x9b\x9f\xd9\xd2y\xf3\x0b\xb2o\xce\xb1\xe3\xc1\xc5\xe9h)\xf7\x11\x84'
app.config['SESSION_TYPE'] = 'filesystem'

with app.app_context():
    import flickr_feed.views
