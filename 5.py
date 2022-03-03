import sys
from full_maps_search import geocoder


def main():
    """Пример использования модуля"""
    query_str = ' '.join(sys.argv[1:])
    lon, lat = geocoder.get_coords(geocode_str=query_str)
    if None in (lon, lat):
        print('Целевой объект не найден')
        sys.exit(1)
    ll = f'{lon},{lat}'
    toponym = geocoder.get_geocode(ll, ll=ll, kind='district')
    if toponym is None:
        print('Целевой объект не принадлежит какому-либо району')
        sys.exit(1)
    address_components = (
        toponym['metaDataProperty']['GeocoderMetaData']
        ['Address']['Components'])
    district_components = []
    for addr_component in address_components:
        if addr_component['kind'] == 'district':
            district_components.append(addr_component['name'])
    print(', '.join(district_components))


if __name__ == '__main__':
    main()
