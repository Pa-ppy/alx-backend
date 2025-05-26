#!/usr/bin/env python3
"""Flask app with simulated user login."""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


class Config:
    """App config with languages and defaults."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)
app.config.from_object(Config)


babel = Babel(app)


def get_user():
    """Retrieve user from mock database."""
    try:

        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set g.user before handling requests."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best language using URL, user, header, or default."""
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale
    if g.get('user'):
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render template with optional user greeting."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run()
