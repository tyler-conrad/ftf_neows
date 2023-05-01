from datetime import date
import json

from client_utils import neo_url_from_date, only_last_four, seconds_from_milliseconds, \
    filter_json_resp


def test_neo_url_from_date():
    assert neo_url_from_date(date(2023, 1,
                                  1)) == 'http://api.nasa.gov/neo/rest/v1/feed?start_date=2023-01-01&end_date=2023-01-01&api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ'
    assert neo_url_from_date(date(1, 1,
                                  1)) == 'http://api.nasa.gov/neo/rest/v1/feed?start_date=0001-01-01&end_date=0001-01-01&api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ'


def test_only_last_four():
    assert only_last_four('9845uhr984u') == '984u'
    assert only_last_four('') == ''


def test_seconds_from_milliseconds():
    assert seconds_from_milliseconds(1000.0) == 1.0
    assert seconds_from_milliseconds(100.0) == 0.1
    assert seconds_from_milliseconds(0.0) == 0.0


def test_filter_json_resp():
    json_data = '''{
        "links": {
            "next": "http://api.nasa.gov/neo/rest/v1/feed?start_date=1982-12-14&end_date=1982-12-14&detailed=false&api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ",
            "prev": "http://api.nasa.gov/neo/rest/v1/feed?start_date=1982-12-12&end_date=1982-12-12&detailed=false&api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ",
            "self": "http://api.nasa.gov/neo/rest/v1/feed?start_date=1982-12-13&end_date=1982-12-13&detailed=false&api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ"
        },
        "element_count": 3,
        "near_earth_objects": {
            "1982-12-13": [
                {
                    "links": {
                        "self": "http://api.nasa.gov/neo/rest/v1/neo/2159699?api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ"
                    },
                    "id": "2159699",
                    "neo_reference_id": "2159699",
                    "name": "159699 (2002 PQ142)",
                    "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=2159699",
                    "absolute_magnitude_h": 17.7,
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.7665755735,
                            "estimated_diameter_max": 1.7141150923
                        },
                        "meters": {
                            "estimated_diameter_min": 766.5755735311,
                            "estimated_diameter_max": 1714.1150923063
                        },
                        "miles": {
                            "estimated_diameter_min": 0.4763278307,
                            "estimated_diameter_max": 1.065101409
                        },
                        "feet": {
                            "estimated_diameter_min": 2515.0118046636,
                            "estimated_diameter_max": 5623.7373594423
                        }
                    },
                    "is_potentially_hazardous_asteroid": false,
                    "close_approach_data": [
                        {
                            "close_approach_date": "1982-12-13",
                            "close_approach_date_full": "1982-Dec-13 20:13",
                            "epoch_date_close_approach": 408658380000,
                            "relative_velocity": {
                                "kilometers_per_second": "21.6943518245",
                                "kilometers_per_hour": "78099.666568069",
                                "miles_per_hour": "48528.0955961426"
                            },
                            "miss_distance": {
                                "astronomical": "0.4835899754",
                                "lunar": "188.1165004306",
                                "kilometers": "72344030.273192398",
                                "miles": "44952495.9368271724"
                            },
                            "orbiting_body": "Earth"
                        }
                    ],
                    "is_sentry_object": false
                },
                {
                    "links": {
                        "self": "http://api.nasa.gov/neo/rest/v1/neo/3799748?api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ"
                    },
                    "id": "3799748",
                    "neo_reference_id": "3799748",
                    "name": "(2018 DA2)",
                    "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=3799748",
                    "absolute_magnitude_h": 23.3,
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.058150704,
                            "estimated_diameter_max": 0.130028927
                        },
                        "meters": {
                            "estimated_diameter_min": 58.1507039646,
                            "estimated_diameter_max": 130.0289270043
                        },
                        "miles": {
                            "estimated_diameter_min": 0.0361331611,
                            "estimated_diameter_max": 0.0807962044
                        },
                        "feet": {
                            "estimated_diameter_min": 190.7831555951,
                            "estimated_diameter_max": 426.6041048727
                        }
                    },
                    "is_potentially_hazardous_asteroid": false,
                    "close_approach_data": [
                        {
                            "close_approach_date": "1982-12-13",
                            "close_approach_date_full": "1982-Dec-13 12:28",
                            "epoch_date_close_approach": 408630480000,
                            "relative_velocity": {
                                "kilometers_per_second": "16.4180461305",
                                "kilometers_per_hour": "59104.9660696355",
                                "miles_per_hour": "36725.5273892132"
                            },
                            "miss_distance": {
                                "astronomical": "0.3197487772",
                                "lunar": "124.3822743308",
                                "kilometers": "47833736.004224564",
                                "miles": "29722505.3021404232"
                            },
                            "orbiting_body": "Earth"
                        }
                    ],
                    "is_sentry_object": false
                },
                {
                    "links": {
                        "self": "http://api.nasa.gov/neo/rest/v1/neo/3835962?api_key=VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ"
                    },
                    "id": "3835962",
                    "neo_reference_id": "3835962",
                    "name": "(2018 VB1)",
                    "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=3835962",
                    "absolute_magnitude_h": 23.7,
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.0483676488,
                            "estimated_diameter_max": 0.1081533507
                        },
                        "meters": {
                            "estimated_diameter_min": 48.3676488219,
                            "estimated_diameter_max": 108.1533506775
                        },
                        "miles": {
                            "estimated_diameter_min": 0.0300542543,
                            "estimated_diameter_max": 0.0672033557
                        },
                        "feet": {
                            "estimated_diameter_min": 158.6865169607,
                            "estimated_diameter_max": 354.8338390368
                        }
                    },
                    "is_potentially_hazardous_asteroid": false,
                    "close_approach_data": [
                        {
                            "close_approach_date": "1982-12-13",
                            "close_approach_date_full": "1982-Dec-13 01:46",
                            "epoch_date_close_approach": 408591960000,
                            "relative_velocity": {
                                "kilometers_per_second": "16.6861090932",
                                "kilometers_per_hour": "60069.9927356978",
                                "miles_per_hour": "37325.1574306896"
                            },
                            "miss_distance": {
                                "astronomical": "0.2216654423",
                                "lunar": "86.2278570547",
                                "kilometers": "33160678.020687901",
                                "miles": "20605089.8513429938"
                            },
                            "orbiting_body": "Earth"
                        }
                    ],
                    "is_sentry_object": false
                }
            ]
        }
    }'''

    assert filter_json_resp(json.loads(json_data)) == [
        {'data': {'close_approach_data': [{'date': '1982-12-13',
                                           'date_full': '1982-Dec-13 20:13',
                                           'iso_8601': '1982-12-13T14:13:00',
                                           'miss_distance': {'miles': '44952495.9368271724'},
                                           'orbiting_body': 'Earth',
                                           'relative_velocity': {
                                               'miles_per_hour': '48528.0955961426'}}],
                  'estimated_diameter': {'feet': {'max': 5623.7373594423,
                                                  'min': 2515.0118046636},
                                         'miles': {'max': 1.065101409,
                                                   'min': 0.4763278307}},
                  'is_potentially_hazardous_asteroid': False,
                  'is_sentry_object': False,
                  'name': '159699 (2002 PQ142)',
                  'neo_reference_id': '9699'},
         'date': '1982-12-13'},
        {'data': {'close_approach_data': [{'date': '1982-12-13',
                                           'date_full': '1982-Dec-13 12:28',
                                           'iso_8601': '1982-12-13T06:28:00',
                                           'miss_distance': {'miles': '29722505.3021404232'},
                                           'orbiting_body': 'Earth',
                                           'relative_velocity': {
                                               'miles_per_hour': '36725.5273892132'}}],
                  'estimated_diameter': {'feet': {'max': 426.6041048727,
                                                  'min': 190.7831555951},
                                         'miles': {'max': 0.0807962044,
                                                   'min': 0.0361331611}},
                  'is_potentially_hazardous_asteroid': False,
                  'is_sentry_object': False,
                  'name': '(2018 DA2)',
                  'neo_reference_id': '9748'},
         'date': '1982-12-13'},
        {'data': {'close_approach_data': [{'date': '1982-12-13',
                                           'date_full': '1982-Dec-13 01:46',
                                           'iso_8601': '1982-12-12T19:46:00',
                                           'miss_distance': {'miles': '20605089.8513429938'},
                                           'orbiting_body': 'Earth',
                                           'relative_velocity': {
                                               'miles_per_hour': '37325.1574306896'}}],
                  'estimated_diameter': {'feet': {'max': 354.8338390368,
                                                  'min': 158.6865169607},
                                         'miles': {'max': 0.0672033557,
                                                   'min': 0.0300542543}},
                  'is_potentially_hazardous_asteroid': False,
                  'is_sentry_object': False,
                  'name': '(2018 VB1)',
                  'neo_reference_id': '5962'},
         'date': '1982-12-13'}]
