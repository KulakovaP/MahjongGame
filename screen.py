import pygame
from constants import *


class BaseScreen:
    """Базовый класс для всех экранов игры"""

    def __init__(self, screen, resource_manager):
        self.screen = screen
        self.resource_manager = resource_manager
        self.base_font = resource_manager.load_font('base', 40)
        self.small_font = resource_manager.load_font('small', 30)

    def handle_input(self, event):
        """Обработка ввода"""
        raise NotImplementedError

    def update(self):
        """Обновление состояния экрана"""
        pass

    def render(self):
        """Отрисовка экрана"""
        raise NotImplementedError

    def draw_text_centered(self, text, y, font=None, color=COLOR_WHITE):
        """Для отрисовки текста по центру"""
        font = font or self.base_font

        # Защита от некорректных значений текста
        if text is None:
            text = ""
        elif not isinstance(text, (str, bytes)):
            try:
                text = str(text)
            except:
                text = ""

        try:
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text_surface, text_rect)
        except Exception as e:
            print(f"Ошибка при рендеринге текста: {e}")
            print(f"Текст: {text}, тип: {type(text)}")
