flickr_feed
===========

How to run ?

* `git clone https://github.com/vipul-sharma20/flickr_feed.git`
* `cd flickr_feed`
* `virtualenv ff`
* `workon ff` or source `ff/bin/activate`
* `pip install -r requirements.txt`
* `export FLASK_APP=flickr_feed/__init__.py`
* `flask run`

Features
--------

* **Search** : Displays photos based on search query
* **Like / Favorite** : Liked photos are favorited in the user's Flickr account
* **OAuth** : To sync up with the favorites in concerned Flickr account

App Architecture
----------------
        .
        ├── README.md ------------------> Description of this application
        ├── flickr_feed
        │   ├── __init__.py ------------> FLASK_APP starts here
        │   ├── config.py --------------> API configuration and app configs
        │   ├── flickr.py --------------> Flickr OAuth and API requests ** (I found this interesting) **
        │   ├── static
        │   │   ├── css
        │   │   │   ├── main.css  ------> Templates CSS
        │   │   │   └── main.min.css ---> Minified version of above
        │   │   └── js
        │   │       ├── main.js --------> All of JavaScript code
        │   │       └── main.min.js ----> Minified version of above
        │   ├── templates
        │   │   └── index.html ---------> The only page of this app
        │   └──  views.py --------------> View functions for all the routes
        └──  requirements.txt -----------> App requirements

