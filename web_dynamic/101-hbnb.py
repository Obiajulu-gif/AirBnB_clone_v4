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


@app.route('/101-hbnb')
def hbnb_filters():
    """
    Renders the custom template with states, cities & amenities.
    """
    states = storage.all('State').values()
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = {user.id: f"{user.first_name} {user.last_name}"
             for user in storage.all('User').values()}

    return render_template('101-hbnb.html',
                           cache_id=uuid.uuid4(),
                           states=states,
                           amenities=amenities,
                           places=places,
                           users=users)


if __name__ == "__main__":
    """
    MAIN Flask App"""
    app.run(host=host, port=port)
