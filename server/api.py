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
    # get lat, lng, count  and radius from get parameters
    # and return an error if either of them is not supplied
    lat     = request.args.get('lat', None)
    lng     = request.args.get('lng', None)
    radius  = request.args.get('radius', None)
    tags    = request.args.get('tags', None)
    threshold = request.args.get('count', None)

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

        return jsonify({'error': err_msg})

    tag_ids = []
    # get tag_ids to filter shops by
    if tags:
        tag_ids = [ tag.id.hex for tag in Tag.query.filter(Tag.tag.in_(tags.split(','))).all()]
        if not tag_ids:
            return jsonify({'errors': 'No results matched the tags provided'})

    neighbours = Shop().get_neighbours(lat, lng, int(radius), tag_ids)

    # get all products that are from the shops neighbouring
    # current location, with a quantity > 0 so we don't return
    # priducts that are out of stock. Also sort by a descending
    # value of popularity to get the cutoff for the count for the
    # top N popular products
    products = [ product.to_json() for product in Product.query.\
        filter(and_(Product.shop_id.in_(neighbours),\
                    Product.quantity > 0)).\
        order_by(Product.popularity.desc()).\
        limit(threshold).\
        all()]

    return jsonify({'products': products})
