import sys
from full_maps_search import geocoder
from full_maps_search import pygame_mapper
from full_maps_search import business
from full_maps_search import utils


def main():
    """Пример использования модуля"""
    query_str = ' '.join(sys.argv[1:])
    toponym = geocoder.get_geocode(query_str)
    lonlat, span = geocoder.get_ll_span(toponym=toponym)
    if not (lonlat and span):
        print('Целевой объект не найден')
        sys.exit(1)
    organization = business.find_business(lonlat, span, 'аптека')
    aor_lon, aor_lat = business.get_coords(organization)
    if None in (organization, aor_lon, aor_lat):
        print('Ближайшая аптека не найдена')
        sys.exit(1)
    org_prop = organization['properties']
    aor_ll = f'{aor_lon},{aor_lat}'
    map_type = 'map'
    coords = [lonlat, aor_ll]
    points_descs = ['pm2rdl', 'pm2bll']
    marks = [1, 2]
    names = [toponym['name'], org_prop['name']]
    points = '~'.join(
        f'{ll},{dsc}{mrk}' for ll, dsc, mrk in zip(
            coords, points_descs, marks))
    title = '; '.join(
        f'{num} - {name}' for num, name in zip(marks, names))
    addr, name, hours = business.get_addr_name_hours(organization)
    toponym_coords = geocoder.get_coords(toponym=toponym)
    distance = utils.lonlat_distance(toponym_coords, (aor_lon, aor_lat))
    if None not in (addr, name, hours):
        print(
            'Данные организации:\n'
            f'Адрес: {addr}\n'
            f'Название: {name}\n'
            f'Время работы: {hours}\n'
            f'Расстояние от исходной точки: {int(distance)}м')
    pygame_mapper.show_map(
        ll=lonlat, spn=span, l=map_type, pt=points, caption=title)


if __name__ == '__main__':
    main()
