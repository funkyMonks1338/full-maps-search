import pygame
import requests
import sys
from io import BytesIO
from . import utils


SCREEN_SIZE = (600, 450)
# гарантированно валидный
DEFAULT_FILL = 'black'


def show_map(
        use_traceback: bool = True, caption: str = 'Map',
        background_color=DEFAULT_FILL, **map_params: dict) -> None:
    """Показывает картинку карты"""
    map_request = 'http://static-maps.yandex.ru/1.x/'
    try:
        response = requests.get(map_request, params=map_params)
    except requests.exceptions.RequestException as req_exc:
        if use_traceback:
            utils.traceback(utils.exc_to_response(req_exc), map_request)
        return None
    if not response:
        if use_traceback:
            utils.traceback(response, map_request)
        return None
    try:
        map_bytes_io = BytesIO(response.content)
    except IOError as exc:
        exc.args = ('Ошибка записи контента картинки',) + exc.args
        sys.exit(exc)
    pygame.init()
    try:
        map_image = pygame.image.load(map_bytes_io)
    except pygame.error as pg_exc:
        pg_exc.args = ('Ошибка загрузки картинки',) + pg_exc.args
        sys.exit(pg_exc)
    map_image_rect = map_image.get_rect()
    map_is_smaller = any((
        map_image_rect.width < SCREEN_SIZE[0],
        map_image_rect.height < SCREEN_SIZE[1]))
    try:
        background_color = pygame.Color(background_color)
    except ValueError:
        background_color = DEFAULT_FILL
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(caption)
    if map_is_smaller:
        screen.fill(background_color)
    screen.blit(map_image, (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
