# -*- coding: utf-8 -*-
from server.models import *
import requests

class TestProximitySearch(object):
    def test_neighbours(self):
        return

        lat     = '59.33265972650577'
        lng     = '18.06061237898499'
        radius  = 2000
        tag_ids = ''
        neighbours = Shop().get_neighbours(lat, lng, radius, tag_ids)
        assert len(neighbours) == 4965

        lat     = '59.33265972650577'
        lng     = '18.06061237898499'
        radius  = 500
        tag_ids = ''
        neighbours = Shop().get_neighbours(lat, lng, radius, tag_ids)
        assert len(neighbours) == 1408

        lat     = '59.33265972650577'
        lng     = '18.06061237898499'
        radius  = 100
        tag_ids = ''
        neighbours = Shop().get_neighbours(lat, lng, radius, tag_ids)
        assert len(neighbours) == 63

        lat     = '59.33265972650577'
        lng     = '18.06061237898499'
        radius  = 2000
        tags = 'home'
        tag_ids = [ tag.id.hex for tag in Tag.query.filter(Tag.tag.in_(tags.split(','))).all()]
        neighbours = Shop().get_neighbours(lat, lng, radius, tag_ids)
        assert len(neighbours) == 577 

        lat     = '59.33265972650577'
        lng     = '18.06061237898499'
        radius  = 500
        tags = 'home'
        tag_ids = [ tag.id.hex for tag in Tag.query.filter(Tag.tag.in_(tags.split(','))).all()]
        neighbours = Shop().get_neighbours(lat, lng, radius, tag_ids)
        assert len(neighbours) == 166

        lat     = '59.33265972650577'
        lng     = '18.06061237898499'
        radius  = 100
        tags = 'home'
        tag_ids = [ tag.id.hex for tag in Tag.query.filter(Tag.tag.in_(tags.split(','))).all()]
        neighbours = Shop().get_neighbours(lat, lng, radius, tag_ids)
        assert len(neighbours) == 8

    def test_products(self): 
        url = 'http://127.0.0.1:5000/search'

        payload = {
            'lat': '59.33265972650577',
            'lng': '18.06061237898499',
            'radius': 2000,
        }
        resp = requests.get(url, payload)
        assert len(resp.json()['error']) > 0

        payload = {
            'lat': '59.33265972650577',
            'lng': '18.06061237898499',
            'radius': 2000,
            'count' : 10,
        }
        resp = requests.get(url, payload)
        assert len(resp.json()['products']) == 10

        payload = {
            'lat': '59.33265972650577',
            'lng': '18.06061237898499',
            'radius': 100,
            'count' : 10,
            'tags': 'lights'
        }
        resp = requests.get(url, payload)
        print resp.json()
        assert len(resp.json()['products']) == 10
