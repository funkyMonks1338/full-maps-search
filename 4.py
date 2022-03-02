import sys
from full_maps_search import geocoder
from full_maps_search import pygame_mapper
from full_maps_search import business


def main():
    """Пример использования модуля"""
    N_ORGS = 10
    MARK_SIZE = 'm'
    query_str = ' '.join(sys.argv[1:])
    toponym = geocoder.get_geocode(query_str)
    lonlat, span = geocoder.get_ll_span(toponym=toponym)
    if not (lonlat and span):
        print('Целевой объект не найден')
        sys.exit(1)
    organizations = business.find_businesses(
        lonlat, span, 'аптека')[:N_ORGS]
    coords = [lonlat]
    points_descs = [f'pm2rd{MARK_SIZE}']
    marks = [1]
    for i, organization in enumerate(organizations):
        aor_lon, aor_lat = business.get_coords(organization)
        if None in (organization, aor_lon, aor_lat):
            continue
        org_prop = organization['properties']
        aor_ll = f'{aor_lon},{aor_lat}'
        coords.append(aor_ll)
        is_round_the_clock = business.is_around_the_clock(org_prop)
        if is_round_the_clock is None:
            color = 'gr'
        elif is_round_the_clock:
            color = 'gn'
        else:
            color = 'bl'
        points_descs.append(f'pm2{color}{MARK_SIZE}')
        marks.append((i + 2) % 100)
    map_type = 'map'
    points = '~'.join(
        f'{ll},{dsc}{mrk}' for ll, dsc, mrk in zip(
            coords, points_descs, marks))
    pygame_mapper.show_map(
        ll=lonlat, l=map_type, pt=points, caption=(
            f'Найдено {len(coords) - 1}/{N_ORGS} аптек'))


if __name__ == '__main__':
    main()
