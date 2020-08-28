This script creates an mock API that allows client-side interaction with an 
underlying database (adapted from https://www.freecodecamp.org/news/build-a-simple-json-api-in-python/).

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

1). First create a 'flask' application

```

# Create a new Flask application
app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////artists.db'
db = SQLAlchemy(app)

# Define a class for the Artist table
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    genre = db.Column(db.String)

# Create the table
db.create_all()

```

2). Second, create a data abstraction

```
# Create data abstraction 
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
```

3). Then create data layers

```
# Define the Artwork table
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist_id = db.Column(db.Integer, 
        db.ForeignKey('artist.id'))
    artist = db.relationship('Artist',
        backref=db.backref('artworks'))
 
    
 # Create resource managers and endpoints   
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

4). Then create endpoints 

```

# Create endpoints    
api = Api(app)
api.route(ArtistMany,    'artist_many',  '/artists')
api.route(ArtistOne,     'artist_one',   '/artists/<int:id>')
api.route(ArtworkOne,    'artwork_one',  '/artworks/<int:id>')
api.route(ArtworkMany,   'artwork_many', '/artworks')
api.route(ArtistArtwork, 'artist_artworks',
    '/artists/<int:id>/relationships/artworks')
    
```

5). Finally, try running the application via the command line

```

## Run application.py and trying posting some data from the command line via curl:
curl -i -X POST -H 'Content-Type: application/json' -d '{"data":{"type":"artwork", "attributes":{"title":"The Persistance of Memory", "artist_id":1}}}'

```
