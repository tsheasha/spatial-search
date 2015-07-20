# -*- coding: utf-8 -*-

from geohash import encode
from server.api import data_path
from server.models import *
import csv

def load_shops(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as shops:
        dict_reader = csv.DictReader(shops)
        for row in dict_reader:
            shop = Shop()

            shop.id         = row['id']
            shop.name       = row['name']
            shop.latitude   = row['lat']
            shop.longitude  = row['lng']

            shop.geohash    = encode(float(shop.latitude), float(shop.longitude))
            shop.save()


def load_products(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as products:
        dict_reader = csv.DictReader(products)
        for row in dict_reader:

            product = Product()

            product.id          = row['id']
            product.shop_id     = row['shop_id']
            product.title       = repr(row['title'])
            product.popularity  = int( float( row['popularity'] ) * 1000 )
            product.quantity    = row['quantity']

            product.save()

def load_tags(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as tags:
        dict_reader = csv.DictReader(tags)
        for row in dict_reader:
            tag = Tag()

            tag.id  = row['id']
            tag.tag = row['tag']

            tag.save()

def load_taggings(filename):
    file_path = data_path(filename)
    with open(file_path, 'rb') as taggings:
        dict_reader = csv.DictReader(taggings)
        for row in dict_reader:

            tagging = Tagging()

            tagging.id      = row['id']
            tagging.tag_id  = row['tag_id']
            tagging.shop_id = row['shop_id']

            tagging.save()
