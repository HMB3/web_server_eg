This python script creates an mock API that allows client-side interaction with an 
underlying database (adapted from https://www.freecodecamp.org/news/build-a-simple-json-api-in-python/).

Here's an overview of the steps involved:

1). Define a database using Flask-SQLAlchemy
2). Create a data abstraction with Marshmallow-JSONAPI
3). Create resource managers with Flask-REST-JSONAPI
4). Create URL endpoints and start the server with Flask


```

## Import Python Libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from marshmallow_jsonapi.flask import Relationship
from flask_rest_jsonapi import ResourceRelationship

```

1). Define a database using Flask-SQLAlchemy

```

## 1). Create the SQL database
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"D:\web_server_eg\data\artists.db")


##  Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////artists.db'
db = SQLAlchemy(app)

```

2). Create a data abstraction with Marshmallow-JSONAPI

```
## 2). Create data abstractions 
class ArtistSchema(Schema):
    class Meta:
        type_ = 'artist'
        self_view = 'artist_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'artist_many'

    id = fields.Integer()
    name = fields.Str(required=True)
    birth_year = fields.Integer(load_only=True)
    genre = fields.Str()
    artworks = Relationship(self_view = 'artist_artworks',
        self_view_kwargs = {'id': '<id>'},
        related_view = 'artwork_many',
        many = True,
        schema = 'ArtworkSchema',
        type_ = 'artwork')

class ArtworkSchema(Schema):
    class Meta:
        type_ = 'artwork'
        self_view = 'artwork_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'artwork_many'

    id = fields.Integer()
    title = fields.Str(required=True)
    artist_id = fields.Integer(required=True)
    
## Define the Artwork table
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist_id = db.Column(db.Integer, 
        db.ForeignKey('artist.id'))
    artist = db.relationship('Artist',
        backref=db.backref('artworks'))

```

3). Create resource managers with Flask-REST-JSONAPI

```
 ## Create resource managers and endpoints   
class ArtworkMany(ResourceList):
    schema = ArtworkSchema
    data_layer = {'session': db.session,
                  'model': Artwork}

class ArtworkOne(ResourceDetail):
    schema = ArtworkSchema
    data_layer = {'session': db.session,
                  'model': Artwork}

class ArtistArtwork(ResourceRelationship):
    schema = ArtistSchema
    data_layer = {'session': db.session,
                  'model': Artist}
    
class ArtistMany(ResourceList):
    schema = ArtistSchema
    data_layer = {'session': db.session,
                  'model': Artist}

class ArtistOne(ResourceDetail):
    schema = ArtistSchema
    data_layer = {'session': db.session,
                  'model': Artist}  
```

4). Finally, create the URL endpoints and start the server with Flask

```

## 4). Create endpoints    
api = Api(app)
api.route(ArtistMany,    'artist_many',  '/artists')
api.route(ArtistOne,     'artist_one',   '/artists/<int:id>')
api.route(ArtworkOne,    'artwork_one',  '/artworks/<int:id>')
api.route(ArtworkMany,   'artwork_many', '/artworks')
api.route(ArtistArtwork, 'artist_artworks',
    '/artists/<int:id>/relationships/artworks')
    
## main loop to run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
    
```

5). Finally, try running the application via the command line

```

## Run application.py and trying posting some data from the command line via curl:
curl -i -X POST -H 'Content-Type: application/json' -d '{"data":{"type":"artwork", "attributes":{"title":"The Persistance of Memory", "artist_id":1}}}'

```
