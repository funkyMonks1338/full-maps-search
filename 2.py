from full_maps_search import geocoder
from full_maps_search import pygame_mapper


def ask_for_valid_geocode(msg: str = 'Valid geocode: ') -> tuple:
    ("""Спрашивает геокод, пока тот не будет валидным. """
     """Возвращает строку запроса и полученный топоним""")
    query_toponym = None
    while query_toponym is None:
        gcode = input(msg)
        query_toponym = geocoder.get_geocode(gcode)
    return (gcode, query_toponym)


def main():
    """Пример использования модуля"""
    query_str, toponym = ask_for_valid_geocode()
    # можно получить координаты без указания топонима
    # для этого будет осуществлён отдельный запрос
    lon, lat = geocoder.get_coords(query_str)
    pygame_mapper.show_map(
        ll=f'{lon},{lat}', spn='0.5,0.5', l='sat', caption=query_str)
    # можно указать заранее полученный топоним, тогда другие
    # вспомогательные функции не будут делать запросы
    lonlat, span = geocoder.get_ll_span(toponym=toponym)
    map_type = 'map'
    coords = [lonlat]
    points_descs = ['pm2rdl']
    marks = [1]
    points = '~'.join(f'{ll},{dsc}{mrk}' for ll, dsc, mrk in zip(
        coords, points_descs, marks))
    pygame_mapper.show_map(
        ll=lonlat, spn=span, l=map_type, pt=points,
        caption=toponym['name'])


if __name__ == '__main__':
    main()
