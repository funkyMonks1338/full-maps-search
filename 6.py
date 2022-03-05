import sys
import random
from typing import List
from full_maps_search import geocoder
from full_maps_search import pygame_mapper


MAP_TYPES = ['map', 'sat', 'skl']


def main(cities: List[str], zooms: List[int]):
    slides = []
    for city_index, (city_name, zoom) in enumerate(zip(cities, zooms)):
        lon, lat = geocoder.get_coords(geocode_str=city_name)
        if None in (lon, lat):
            print(f'Город {city_name!r} не найден')
            sys.exit(1)
        ll = f'{lon},{lat}'
        map_type = []
        for _ in range(random.randint(1, 2)):
            part_map_type = random.choice(MAP_TYPES)
            while part_map_type in map_type:
                part_map_type = random.choice(MAP_TYPES)
            map_type.append(part_map_type)
        if zoom < 0:
            zoom = 0
        elif zoom > 17:
            zoom = 17
        pygame_mapper.show_map(
            slide_images=slides, ll=ll,
            l=','.join(map_type), z=zoom)
    pygame_mapper.slide_show(slides, slide_time_period=100)


if __name__ == '__main__':
    # города с чётным индексом - города первого игрока
    # с нечётным - города второго игрока
    CITIES = [
        'Москва', 'Йошкар-Ола', 'Оренбург',
        'Курск', 'Омск', 'Севастополь']
    ZOOMS = [15, 17, 17, 17, 17, 15]
    main(CITIES[:], ZOOMS[:])
