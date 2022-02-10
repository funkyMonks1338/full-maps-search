import requests
import json
from typing import Tuple
from . import utils


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def get_geocode(
        geocode_str: str, result_index: int = 0,
        use_traceback: bool = True) -> dict:
    """Возвращает топоним по запросу"""
    DEFAULT = None
    if not geocode_str:
        return DEFAULT
    req_url = 'http://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': API_KEY,
        'geocode': geocode_str,
        'format': 'json'
    }
    try:
        res = requests.get(req_url, params=params)
    except requests.exceptions.RequestException as req_exc:
        if use_traceback:
            utils.traceback(utils.exc_to_response(req_exc), req_url)
        return DEFAULT
    if not res:
        if use_traceback:
            utils.traceback(res, req_url)
        return DEFAULT
    try:
        json_res = res.json()
    except json.JSONDecodeError:
        if use_traceback:
            utils.traceback(res, req_url)
        return DEFAULT
    try:
        results = json_res['response']['GeoObjectCollection']['featureMember']
        if not results:
            return DEFAULT
        toponym = results[result_index]['GeoObject']
    except (KeyError, IndexError) as exc:
        if use_traceback:
            utils.traceback(utils.exc_to_response(exc), req_url)
        toponym = DEFAULT
    return toponym


def get_coords(geocode_str: str = '', toponym: dict = ...) -> Tuple[float]:
    """Возвращает координаты топонима или топонима по запросу"""
    DEFAULT = (None, None)
    if toponym is (...):
        toponym = get_geocode(geocode_str)
    if toponym is None:
        return DEFAULT
    try:
        coords_str = toponym['Point']['pos']
    except KeyError:
        return DEFAULT
    try:
        lon, lat = map(float, coords_str.split())
    except ValueError:
        return DEFAULT
    return (lon, lat)


def get_ll_span(geocode_str: str = '', toponym: dict = ...) -> Tuple[str]:
    DEFAULT = (None, None)
    if toponym is (...):
        toponym = get_geocode(geocode_str)
    if toponym is None:
        return DEFAULT
    lon, lat = get_coords(toponym=toponym)
    if lon is None or lat is None:
        return DEFAULT
    ll = f'{lon},{lat}'
    try:
        envelope = toponym['boundedBy']['Envelope']
        upper_corner = envelope['upperCorner']
        lower_corner = envelope['lowerCorner']
    except KeyError:
        return DEFAULT
    try:
        right, top = map(float, upper_corner.split())
        left, bottom = map(float, lower_corner.split())
    except ValueError:
        return DEFAULT
    delta_y = abs(left - right) / 2
    delta_x = abs(top - bottom) / 2
    span = f'{delta_x},{delta_y}'
    return (ll, span)
