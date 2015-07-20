# -*- coding: utf-8 -*-

from ast import literal_eval
from extensions import db, GUID
from geohash import encode, decode, expand

from geopy.point import Point as GeopyPoint
from geopy.distance import distance
import uuid

# number of cahracters to covered radius
# *radius in meters*
GEOHASH_CHARS_TO_DISTANCE = {
    5: 2400,
    6: 610,
    7: 76,
    8: 19,
}

class Shop(db.Model):
    """
    Shop database model defining 5 columns
        id: GUID  field specifying primary key of row.
        geohash: String field specifying geohash and it is indexed
        name: String field specifying the name of the shop
        latitude: String specifying latitude
        longitude: String field specifying longitude
    """
    __tablename__ = 'shop'
    id          = db.Column(GUID, primary_key=True)
    geohash     = db.Column(db.String, index=True)
    name        = db.Column(db.String)
    latitude    = db.Column(db.String)
    longitude   = db.Column(db.String)

    # to allow products to ge the shop by a simple instance method
    products = db.relationship("Product", backref="shop")

    def get_neighbours(cls, lat, lng, radius, tags):
        # get length of geohash for the required radius
        geohash_length = 12
        for to_remove, accuracy in sorted(GEOHASH_CHARS_TO_DISTANCE.items()):
            if  accuracy < radius:
                geohash_length = ( to_remove - 1 )
                break

        query = []
        param = []
        result = []

        # get encoding of current lat, lng
        geohash_code = encode(float(lat), float(lng), geohash_length)

        # get neighbours of current geohash accoridng to radius
        # and generate sql statements for them
        # the choice to run the sql statements as literal SQL
        # and not through the ORM was a concious decision since
        # I did not want all these objects to be created just
        # and pass through the layers of the ORM, this is a performance
        # critical method and no need for that overhead.
        for prefix in expand(geohash_code):
            query.append("geohash LIKE ?")
            param.append(prefix+"%")

        query_text = "SELECT DISTINCT(shop.id), latitude, longitude FROM shop LEFT JOIN tagging"+\
                     " ON shop.id = tagging.shop_id WHERE (" +\
                     " OR ".join(query)+ ")"

        # include tags in the search
        if tags:
            query_text += " AND tag_id IN (%s) AND tagging.id IS NOT NULL" % ','.join('?' * len(tags))
            param += tags

        # manually filter the outliers after that do not
        # fall within the exact radius, but fall within the geohash
        # neighbours
        orig = GeopyPoint(latitude=lat, longitude=lng)
        for row in db.engine.execute(query_text, param):
            shop_as_point = GeopyPoint(latitude=row[1], longitude=row[2])
            if distance(orig, shop_as_point).meters <= radius:
                result.append(row[0])

        return result

    # Transforms Model to JSON format
    def to_json(self):
        return {
                "name": self.name,
                "lat":  self.latitude,
                "long": self.longitude,
            }

    def save(self):
        db.session.add(self)
        db.session.commit()

class Product(db.Model):
    """
    Product database model defining 5 columns
        id: GUID  field specifying primary key of row.
        title: String field specifying the name of the product
        popularity: SmallInteger specifying popularity of product
        quantity: Integer field specifying quantity of product in shop stock
        shop_id: Foreign Key to Shop Model.
    """
    __tablename__ = 'product'
    id          = db.Column(GUID, primary_key=True)
    title       = db.Column(db.String)
    popularity  = db.Column(db.SmallInteger)
    quantity    = db.Column(db.Integer)
    shop_id     = db.Column(GUID, db.ForeignKey('shop.id'))

    # Transforms Model to JSON format
    def to_json(self):
        return {
                "title"     : literal_eval(self.title),
                "populatiry": float(self.popularity) / 1000,
                "shop"      : { 'lat' : self.shop.latitude,
                                'lng' : self.shop.longitude
                            }
            }

    def save(self):
        db.session.add(self)
        db.session.commit()

class Tag(db.Model):
    """
    Tag database model defining 2 columns
        id: GUID  field specifying primary key of row.
        tag: String field specifying the tag name
    """
    __tablename__ = 'tag'
    id  = db.Column(GUID, primary_key=True)
    tag = db.Column(db.String)
    
    # Transforms Model to JSON format
    def to_json(self):
        return {
                "tag": self.tag,
            }

    def save(self):
        db.session.add(self)
        db.session.commit()

class Tagging(db.Model):
    """
    Tagging database model defining 3 columns
        id: GUID  field specifying primary key of row.
        tag_id: Foreign Key to Tag Model.
        shop_id: Foreign Key to Shop Model.
    """
    __tablename__ = 'tagging'
    id      = db.Column(GUID, primary_key=True)
    tag_id  = db.Column(GUID, db.ForeignKey('tag.id'))
    shop_id = db.Column(GUID, db.ForeignKey('shop.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()
