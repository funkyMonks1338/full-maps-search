import sys
import math
import requests
from typing import Tuple


def exc_to_response(exception: Exception) -> requests.Response:
    response = requests.Response()
    response.reason = exception.__class__.__name__
    return response


def traceback(response: requests.Response, request: str) -> None:
    print(
        f'Ошибка выполнения запроса:\n{request}\n'
        f'Http статус: {response.status_code} ({response.reason})')
    sys.exit(1)


def lonlat_distance(a_coords: Tuple[float], b_coords: Tuple[float]) -> float:
    """Считает расстояние между двумя точками, заданными координатами"""
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a_coords
    b_lon, b_lat = b_coords
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance
