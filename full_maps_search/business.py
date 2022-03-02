import requests
import json
from typing import List, Tuple
from . import utils


API_KEY = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'


def find_businesses(
        lonlat: str, span: str, query: str, locale: str = 'ru_RU',
        use_traceback: bool = True) -> List[dict]:
    DEFAULT = []
    req_url = 'https://search-maps.yandex.ru/v1/'
    search_params = {
        'apikey': API_KEY, 'text': query,
        'lang': locale, 'll': lonlat,
        'spn': span, 'type': 'biz'}
    response = requests.get(req_url, params=search_params)
    if not response:
        if use_traceback:
            utils.traceback(response, req_url)
        return DEFAULT
    try:
        json_response = response.json()
    except json.JSONDecodeError as json_exc:
        if use_traceback:
            utils.traceback(utils.exc_to_response(json_exc), req_url)
        return DEFAULT
    try:
        organizations = json_response['features']
    except KeyError as dict_exc:
        if use_traceback:
            utils.traceback(utils.exc_to_response(dict_exc), req_url)
        return DEFAULT
    return organizations


def get_coords(org: dict) -> Tuple[float]:
    DEFAULT = (None, None)
    if not isinstance(org, dict):
        return DEFAULT
    try:
        coords = org['geometry']['coordinates']
    except KeyError:
        return DEFAULT
    try:
        lon, lat = map(float, coords)
    except ValueError:
        return DEFAULT
    return (lon, lat)


def to_org_properties(org: dict) -> dict:
    ("""Если json словарь имеет тип Feature, то """
     """он преобразовывается в json словарь типа properties""")
    if not isinstance(org, dict):
        return org
    feature_keys = ['geometry', 'properties', 'type']
    keys_match = sorted(org.keys()) == feature_keys
    if keys_match and org[feature_keys[2]] == 'Feature':
        org = org[feature_keys[1]]
    return org


def is_around_the_clock(org: dict) -> bool:
    """Проверяет круглосуточность организации"""
    DEFAULT = None
    org = to_org_properties(org)
    try:
        hours = org['CompanyMetaData']['Hours']
        avail_times = hours['Availabilities']
        if not avail_times:
            return DEFAULT
        all_hours = avail_times[0]['TwentyFourHours']
        every_day = avail_times[0]['Everyday']
    except KeyError:
        return DEFAULT
    return all_hours and every_day


def get_addr_name_hours(org: dict) -> Tuple[str]:
    ("""Возвращает адрес, название организации """
     """и время её работы.""")
    DEFAULT = (None, None, None)
    org = to_org_properties(org)
    try:
        company_meta = org['CompanyMetaData']
        address = company_meta['address']
        name = org['name']
        hours = company_meta['Hours']['text']
    except KeyError:
        return DEFAULT
    return (address, name, hours)


def find_business(
        ll: str, spn: str, query: str, locale: str = 'ru_RU',
        use_traceback: bool = True) -> dict:
    orgs = find_businesses(ll, spn, query, locale=locale)
    if orgs:
        return orgs[0]
