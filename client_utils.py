from typing import Any
from datetime import date, datetime
from collections import namedtuple
from urllib.parse import urlencode, urlunparse

Components = namedtuple(
    typename='Components',
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
)


def neo_url_from_date(day: date) -> str:
    str_day = day.strftime('%Y-%m-%d')
    return urlunparse(
        Components(
            scheme='http',
            netloc='api.nasa.gov',
            url='/neo/rest/v1/feed',
            path='',
            query=urlencode({'start_date': str_day, 'end_date': str_day,
                             'api_key': 'VSNS16eUgblwgwNXimKUYBTljBcMclhGkb9bwpaJ'}),
            fragment=''
        )
    )


class NeoData:
    def __init__(self, remaining_requests: int, day: date, data: list[dict]):
        self.remaining_requests = remaining_requests
        self.day = day
        self.data = data


def only_last_four(neo_reference_id: str) -> str:
    return ''.join(neo_reference_id[-4:])


def seconds_from_milliseconds(millis: float) -> float:
    return millis * 0.001


def filter_json_resp(json: dict) -> list[dict[str, Any]]:
    neos = json['near_earth_objects']
    day = list(neos.keys())[0]
    out = []
    for neo in neos[day]:
        diameter_miles = neo['estimated_diameter']['miles']
        diameter_feet = neo['estimated_diameter']['feet']
        close_approach_data = neo['close_approach_data']
        out.append({'date': day,
                    'data': {
                        'neo_reference_id': only_last_four(neo['neo_reference_id']),
                        'name': neo['name'],
                        'estimated_diameter': {
                            'miles': {
                                'min': diameter_miles['estimated_diameter_min'],
                                'max': diameter_miles['estimated_diameter_max'],
                            },
                            'feet': {
                                'min': diameter_feet['estimated_diameter_min'],
                                'max': diameter_feet['estimated_diameter_max'],
                            },
                        },
                        'is_potentially_hazardous_asteroid': neo[
                            'is_potentially_hazardous_asteroid'],
                        'close_approach_data': [{
                            'date': cod['close_approach_date'],
                            'date_full': cod['close_approach_date_full'],
                            'iso_8601': datetime.fromtimestamp(
                                seconds_from_milliseconds(
                                    cod['epoch_date_close_approach'])).isoformat(),
                            'relative_velocity': {
                                'miles_per_hour': cod['relative_velocity']['miles_per_hour']},
                            'miss_distance': {
                                'miles': cod['miss_distance']['miles']
                            },
                            'orbiting_body': cod['orbiting_body']
                        } for cod in close_approach_data],
                        'is_sentry_object': neo['is_sentry_object']
                    }})
    return out
