# -*- coding: utf-8 -*-

from geohash import encode
from server.api import data_path
from extensions import db
import csv

def load_shops(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as shops:
        dict_reader = csv.DictReader(shops)
        query_text = "INSERT INTO shop "+\
                     "(id, name, latitude, longitude, geohash) "+\
                     "VALUES "
        query = []
        param = []
        counter = 0
        for row in dict_reader:
            query.append("( ?, ?, ?, ?, ? )")

            param.append(row['id'])
            param.append(row['name'])
            param.append(row['lat'])
            param.append(row['lng'])

            param.append(encode(float(row['lat']), float(row['lng'])))
            counter += 1
            if counter == 499:
                batch_text = query_text + ','.join(query)
                db.engine.execute(batch_text, param)
                query = []
                param = []
                counter = 0
        query_text += ','.join(query)
        db.engine.execute(query_text, param)


def load_products(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as products:
        dict_reader = csv.DictReader(products)
        query_text = "INSERT INTO product "+\
                     "(id, shop_id, title, popularity, quantity) "+\
                     "VALUES "
        query = []
        param = []
        counter = 0
        for row in dict_reader:
            query.append("( ?, ?, ?, ?, ? )")

            param.append(row['id'])
            param.append(row['shop_id'])
            param.append(repr(row['title']))
            param.append(int( float( row['popularity'] ) * 1000 ))
            param.append(row['quantity'])
            counter += 1
            if counter == 499:
                batch_text = query_text + ','.join(query)
                db.engine.execute(batch_text, param)
                query = []
                param = []
                counter = 0

        query_text += ','.join(query)
        db.engine.execute(query_text, param)


def load_tags(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as tags:
        dict_reader = csv.DictReader(tags)
        query_text = "INSERT INTO tag "+\
                     "(id, tag) "+\
                     "VALUES "
        query = []
        param = []
        counter = 0
        for row in dict_reader:
            query.append("( ?, ? )")

            param.append(row['id'])
            param.append(row['tag'])
            counter += 1
            if counter == 499:
                batch_text = query_text + ','.join(query)
                db.engine.execute(batch_text, param)
                query = []
                param = []
                counter = 0

        query_text += ','.join(query)
        db.engine.execute(query_text, param)

def load_taggings(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as taggings:
        dict_reader = csv.DictReader(taggings)
        query_text = "INSERT INTO tagging "+\
                     "(id, tag_id, shop_id) "+\
                     "VALUES "
        query = []
        param = []
        counter = 0
        for row in dict_reader:
            query.append("( ?, ?, ? )")

            param.append(row['id'])
            param.append(row['tag_id'])
            param.append(row['shop_id'])
            counter += 1
            if counter == 499:
                batch_text = query_text + ','.join(query)
                db.engine.execute(batch_text, param)
                query = []
                param = []
                counter = 0

        query_text += ','.join(query)
        db.engine.execute(query_text, param)
