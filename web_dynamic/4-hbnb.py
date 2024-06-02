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
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.route('/4-hbnb')
def hbnb_filters():
    """
    Renders the custom template with states, cities, and amenities.
    """
    states = storage.all('State').values()
    cities_by_state = {}
    for state in states:
        cities_by_state[state.name] = storage.all(
            'City').filter_by(state_id=state.id).values()
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    user_names = {user.id: f"{user.first_name} {user.last_name}"
                  for user in storage.all('User').values()}
    return render_template('4-hbnb.html',
                           cache_id=uuid.uuid4(),
                           states=cities_by_state,
                           amenities=amenities,
                           places=places,
                           user_names=user_names)


if __name__ == "__main__":
    """
    MAIN Flask App"""
    app.run(host=host, port=port)
