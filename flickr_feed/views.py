import requests
from flask import render_template, request, redirect, jsonify, session, url_for
from oauth2 import Token

from flickr_feed import app
from flickr_feed.config import PUB_FEED_URL
from flickr_feed.flickr import FlickrAuth, authenticate, FlickrAPI


@app.route('/')
def home():
    """
    Landing page view
    """

    response = _request_flickr_pub()
    data = {}
    try:
        data['images'] = response.json()['items']
    except ValueError:
        return redirect(url_for('home'))

    return render_template('index.html', data=data)


@app.route('/search/')
def search():
    """
    Search tag view
    """

    tags = request.args.get('q')
    if tags:
        try:
            data = {}
            response = _request_flickr_pub(tags)
            data['images'] = response.json()['items']
            return jsonify(data)
        except ValueError:
            return redirect(url_for('search'))
    return redirect('/')


@app.route('/auth/callback/')
def auth_callback():
    """
    Flickr auth callback view
    """

    token = session.get('token')
    oauth_verifier = request.args.get('oauth_verifier')

    if not oauth_verifier:
        return redirect(url_for('home'))

    token = Token.from_string(token)
    token.set_verifier(oauth_verifier)

    flickr = FlickrAuth()
    flickr.exchange_token(token, oauth_verifier)

    return redirect(url_for('home'))


@app.route('/like/<image_id>')
@authenticate
def like(image_id=None, **kwargs):
    """
    Like photo view
    """

    data = {}
    if kwargs.get('redirect_url'):
        data['redirect_url'] = kwargs['redirect_url']
        return jsonify(data)

    flickr = FlickrAPI(**{'photo_id': image_id, 'method': 'flickr.favorites.add'})
    resp, _ = flickr.favorite()

    if resp.status == '200':
        data['status'] = True
        data['message'] = 'success'
    else:
        data['status'] = False
        data['message'] = 'error'

    return jsonify(data)


@app.route('/login/')
def login():
    """
    Login to flickr account view
    """

    flickr = FlickrAuth()
    content = flickr.request_token()
    redirect_url = flickr.authorize(content)

    return redirect(redirect_url)


def _request_flickr_pub(tags=None):
    """
    Utility function for public API calls
    """

    payload = {'format': 'json',
               'nojsoncallback': 1}
    if tags:
        payload['tags'] = tags
        payload['tagmode'] = 'any'
    response = requests.get(PUB_FEED_URL, params=payload)

    return response

