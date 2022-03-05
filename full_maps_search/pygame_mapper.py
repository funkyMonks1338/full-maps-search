import pygame
import requests
import sys
import time
import random
from io import BytesIO
from . import utils


SCREEN_SIZE = (600, 450)
# гарантированно валидный
DEFAULT_FILL = 'black'

pygame.init()


def show_map(
        use_traceback: bool = True, caption: str = 'Map',
        background_color=DEFAULT_FILL, slide_images: list = None,
        **map_params: dict) -> None:
    """Показывает картинку карты.
    Если указан список слайдов, то картинка не показывается,
    а добавляется в конец указанного списка"""
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
    try:
        map_image = pygame.image.load(map_bytes_io)
    except pygame.error as pg_exc:
        pg_exc.args = ('Ошибка загрузки картинки',) + pg_exc.args
        sys.exit(pg_exc)
    if slide_images is not None:
        slide_images.append(map_image)
        return None
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


def get_new_slide_index(prev_slide_index, player_index, n_slides):
    new_slide_index = int(not player_index)
    while new_slide_index % 2 != player_index or \
            (n_slides != 2 and new_slide_index == prev_slide_index):
        new_slide_index = random.randint(0, n_slides - 1)
    return new_slide_index


def slide_show(slide_images: list, slide_time_period=5):
    if not slide_images:
        return None
    slide_images = slide_images[:]
    N_SLIDES = len(slide_images)
    font = pygame.font.Font(None, 30)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    running = True
    player_index = 0
    slide_index = get_new_slide_index(
        -1, player_index, N_SLIDES)
    redraw_slide = True
    new_slide_time_moment = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                redraw_slide = event.key in (
                    pygame.K_LEFT, pygame.K_RIGHT)
                if redraw_slide:
                    new_slide_time_moment = time.time()
        if time.time() - new_slide_time_moment >= slide_time_period:
            new_slide_time_moment = time.time()
            redraw_slide = True
        if redraw_slide:
            screen.fill((0, 0, 0))
            slide_index = get_new_slide_index(
                slide_index, player_index, N_SLIDES)
            screen.blit(slide_images[slide_index], (0, 0))
            font_rendered = font.render(
                f'Загадывает игрок {player_index + 1}', True, 'red')
            screen.blit(font_rendered, (0, 0))
            pygame.display.flip()
            redraw_slide = False
            player_index = int(not player_index)
