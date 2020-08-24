# Imports the Flask library, making the code available to the rest of the application
import flask
from flask import request, jsonify
import sqlite3


# Creates the Flask application object, which contains data about the application and 
# also methods (object functions) that tell the application to do certain actions. 
# The last line, app.run(), is one such method.
app = flask.Flask(__name__)


# Starts the debugger. With this line, if your code is malformed, you’ll see an error 
# when you visit your app. Otherwise you’ll only see a generic message such as Bad 
# Gateway in the browser when there’s a problem with your code.
app.config["DEBUG"] = True


# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


## A function to 
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


# Inside our function, we do two things:
# First, examine the provided URL for an id and select the books that match that id. 
# The id must be provided like this: ?id=0. Data passed through URLs like this (after the ?) 
# are called query parameters—we’ve seen them before when we worked with the Chronicling 
# America API. They’re a feature of HTTP used for filtering for specific kinds of data.
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results.
    # Then this section moves through our test catalog of books, matches 
    # those books that have the provided ID, and appends them to the list 
    # that will be returned to the user:
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


## A method that runs the application server
app.run()



