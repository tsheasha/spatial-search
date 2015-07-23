# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request
from server.models import *
from sqlalchemy import and_

api = Blueprint('api', __name__)
POPULARITY_THRESHOLD = 500

def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
def search():
    params = validate_params(request.args)

    if params.get('error', None):
        return report_error(params['error'])

    if params.get('valid', None):
        lat, lng, radius, threshold, tags = params['valid']

    tag_ids = []
    # get tag_ids to filter shops by
    if tags:
        tag_ids = [ tag.id.hex for tag in Tag.query.filter(Tag.tag.in_(tags.split(','))).all()]
        if not tag_ids:
            return jsonify({'errors': 'No results matched the tags provided'})

    neighbours = Shop().get_neighbours(lat, lng, radius, tag_ids)

    # get all products that are from the shops neighbouring
    # current location, with a quantity > 0 so we don't return
    # priducts that are out of stock. Also sort by a descending
    # value of popularity to get the cutoff for the count for the
    # top N popular products
    products = []
    if neighbours:
        products = [ product.to_json() for product in Product.query.\
            filter(and_(Product.shop_id.in_(neighbours),\
                        Product.quantity > 0)).\
            order_by(Product.popularity.desc()).\
            limit(threshold).\
            all()]

    return jsonify({'products': products})

def validate_params(params):

    # get lat, lng, count  and radius from get parameters
    # and return an error if either of them is not supplied
    lat     = params.get('lat', None)
    lng     = params.get('lng', None)
    radius  = params.get('radius', None)
    tags    = params.get('tags', None)
    threshold = params.get('count', None)

    err_str = []
    if lat is None:
        err_str.append('`lat`')

    if lng is None:
        err_str.append('`lng`')

    if radius is None:
        err_str.append('`radius`')

    if threshold is None:
        err_str.append('`count`')

    if err_str :
        err_msg = "Please supply the following parameters so we can process your request :-\
{0}".format(", ".join(err_str))

        return {'error': err_msg}

    try:
        radius = int(radius)
        threshold = int(threshold)
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        err_msg = "Incorrect input types, please make sure the following holds:- \
radius: Integer, \
lat:    Float, \
lng:    Float, \
radius: Integer, \
tags:   String"
        return {'error': err_msg}

    # Some sanity checking to avoid doing full table scans
    if threshold > 50 or threshold < 10:
        err_msg = "The number of products has to be between 10 and 50 products"
        return {'error': err_msg}

    # Some sanity checking to avoid searched that cover the entire world
    if radius > 2000 or radius < 100:
        err_msg = "Your search can cover a radius range from 100 up to 2000 meters"
        return {'error': err_msg}

    # Some sanity checking to avoid searched that cover the entire world
    if lat > 90 or lat < -90 or lng > 90 or lng < -90:
        err_msg = "Values for lat and lng but be withing a range of 90 and -90"
        return {'error': err_msg}

    return { 'valid': [ lat, lng, radius, threshold, tags ] }

def report_error(err_msg):
    return jsonify({'error': err_msg})
