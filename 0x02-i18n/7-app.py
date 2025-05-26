#!/usr/bin/env python3
"""Flask app with timezone selection."""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _, timezoneselector
import pytz


class Config:
    """App config with language and timezone settings."""
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
    """Get user based on login_as parameter."""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Run before each request to set global user."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine best match locale."""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:

        return locale
    if g.user:
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@timezoneselector
def get_timezone():
    """Determine user's timezone with fallbacks."""
    try:
        tz_param = request.args.get('timezone')
        if tz_param:
            return pytz.timezone(tz_param).zone
        if g.user:
            user_tz = g.user.get('timezone')
            return pytz.timezone(user_tz).zone
    except (pytz.UnknownTimeZoneError, AttributeError):
        pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Display localized greeting."""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run()
