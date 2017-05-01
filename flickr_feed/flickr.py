import datetime
import urlparse

import oauth2
from flask import session
import httplib2

from flickr_feed.config import API_KEY, API_SECRET, REQUEST_TOKEN_URL, \
        AUTH_URL, ACCESS_TOKEN_URL, API_ROOT


def authenticate(view):
    def protected_view(*args, **kwargs):
        if session.get('user_oauth_token'):
            return view(*args, **kwargs)
        else:
            flickr = FlickrAuth()
            content = flickr.request_token()
            redirect_url = flickr.authorize(content)

            return view(*args, **{'redirect_url': redirect_url})
    return protected_view


class FlickrAuth(object):
    def __init__(self, *args, **kwargs):
        self.params = {
                    'oauth_signature_method': "HMAC-SHA1",
                    'oauth_version': "1.0",
                    'oauth_callback': "http://127.0.0.1:5000/auth/callback/",
                    'oauth_consumer_key': API_KEY,
                    'oauth_timestamp': datetime.datetime.now().isoformat(),
                    'oauth_nonce': oauth2.generate_nonce(),
                }

    def request_token(self):
        consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)

        # set up request
        req = oauth2.Request(method="GET", url=REQUEST_TOKEN_URL,
                             parameters=self.params)

        # create the signature and assign to request
        signature = oauth2.SignatureMethod_HMAC_SHA1().sign(req, consumer, None)
        req['oauth_signature'] = signature

        # make the request
        h = httplib2.Http(".cache")
        _, content = h.request(req.to_url(), "GET")

        return content

    def authorize(self, content):
        # parse the content
        request_token = dict(urlparse.parse_qsl(content))

        token = oauth2.Token(request_token['oauth_token'],
                             request_token['oauth_token_secret'])
        session['token'] = token.to_string()
        session['oauth_token'] = request_token['oauth_token']

        # redirect login url
        redirect_url = "{url}?oauth_token={oauth_token}&perms=write".format(
                        url=AUTH_URL, oauth_token=request_token['oauth_token'])

        return redirect_url

    def exchange_token(self, token, oauth_verifier):
        self.params['oauth_token'] = session.get('oauth_token')
        self.params['oauth_verifier'] = oauth_verifier

        consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)

        # setup request
        req = oauth2.Request(method="GET", url=ACCESS_TOKEN_URL,
                             parameters=self.params)

        # create the signature
        signature = oauth2.SignatureMethod_HMAC_SHA1().sign(req, consumer, token)

        # assign the signature to the request
        req['oauth_signature'] = signature

        # make the request
        h = httplib2.Http(".cache")
        resp, content = h.request(req.to_url(), "GET")

        # parse the response
        access_token_resp = dict(urlparse.parse_qsl(content))

        session['user_oauth_token'] = access_token_resp['oauth_token']
        session['oauth_token_secret'] = access_token_resp['oauth_token_secret']
        session['authenticated'] = True


class FlickrAPI(object):
    """
    Flickr API wrapper for authenticated requests
    """

    def __init__(self, *args, **kwargs):
        self.payload = {
                'oauth_consumer_key': API_KEY,
                'oauth_timestamp': datetime.datetime.now().isoformat(),
                'oauth_signature_method': 'HMAC-SHA1',
                'oauth_version': '1.0',
                'oauth_token': session.get('user_oauth_token'),
                'oauth_nonce': oauth2.generate_nonce(),
                'format': 'json'
                }
        self.payload.update(kwargs)

    def favorite(self):
        """
        Like/Favorite image
        """

        consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)

        # setup request
        req = oauth2.Request(method="POST", url=API_ROOT, parameters=self.payload)

        token = oauth2.Token(session.get('user_oauth_token'),
                             session.get('oauth_token_secret'))
        req['oauth_signature'] = oauth2.SignatureMethod_HMAC_SHA1().sign(
                                    req, consumer, token)
        h = httplib2.Http(".cache")
        resp, content = h.request(req.to_url(), "POST")

        return resp, content
