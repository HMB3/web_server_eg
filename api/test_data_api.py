# Imports the Flask library, making the code available to the rest of the application
import flask
from flask import request, jsonify
import sqlite3


## Need to define the endpoint
# 127.0.0.1:5000/api/v1/resources/books?id=0 127.0.0.1:5000/api/v1/resources/books?id=1 
# 127.0.0.1:5000/api/v1/resources/books?id=2 127.0.0.1:5000/api/v1/resources/books?id=3


# Creates the Flask application object, which contains data about the application and 
# also methods (object functions) that tell the application to do certain actions. 
# The last line, app.run(), is one such method.
app = flask.Flask(__name__)


# Starts the debugger. With this line, if your code is malformed, you’ll see an error 
# when you visit your app. Otherwise you’ll only see a generic message such as Bad 
# Gateway in the browser when there’s a problem with your code.
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


# The page_not_found function creates an error page seen by the 
# user if the user encounters an error or inputs a route that hasn’t been defined:
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# This api_filter function is an improvement on our previous api_id function that 
# returns a book based on its ID. This new function allows for filtering by three 
# different fields: id, published, and author. The function first grabs all the 
# query parameters provided in the URL (remember, query parameters are the part 
# of the URL that follows the ?, like ?id=10).


# This code reads query parameters provided by the user, builds an SQL query based 
# on those parameters, executes that query to find matching books in the database, a
# and returns those matches as JSON to the user
@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    # First grabs all the query parameters provided in the URL.
    # It then pulls the supported parameters id, published, and 
    # author and binds them to appropriate variables:
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    # The next segment begins to build an SQL query that will be used to find 
    # the requested information in the database. SQL queries used to find data 
    # in a database take this form:
    query = "SELECT * FROM books WHERE"
    to_filter = []

    # Then, if id, published, or author were provided as query parameters, 
    # we add them to both the query and the filter list
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()



