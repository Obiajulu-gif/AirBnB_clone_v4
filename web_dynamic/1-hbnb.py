#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, render_template, url_for
from models import storage
import uuid

# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


# begin flask page rendering
@app.teardown_appcontext
def close_session(error):
    """
    Closes the session after each request.
    """
    storage.close_session()


@app.route('/1-hbnb')
def hbnb_filters():
    """
    Renders the HBNB template with state, city, and amenity data.
    """
    states = storage.all('State').values()
    cities_by_state = {}
    for state in states:
        cities_by_state[state.name] = storage.state_to_cities(state.id)
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = {user.id: "{} {}".format(user.first_name, user.last_name)
             for user in storage.all('User').values()}
    return render_template('1-hbnb.html',
                           cache_id=uuid.uuid4(),
                           states=states,
                           cities_by_state=cities_by_state,
                           amenities=amenities,
                           places=places,
                           users=users)


if __name__ == "__main__":
    """
    MAIN Flask App"""
    app.run(host=host, port=port)
