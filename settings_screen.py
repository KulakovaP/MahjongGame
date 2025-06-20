import pygame
from screen import BaseScreen
from constants import *
from utils import load_best_time


class SettingsScreen(BaseScreen):
    """Экран настроек"""

    def __init__(self, screen, resource_manager, player_name):
        super().__init__(screen, resource_manager)
        self.player_name = player_name
        self.options = [
            f"Имя игрока: {player_name}",
            "Музыка: Вкл",  # Добавлено
            "Назад"
        ]
        self.selected = 0
        self.editing_name = False
        self.name_input = player_name
        self.best_time = load_best_time()
        self.music_on = True  # Добавлено

    def handle_input(self, event):
        """Обработка ввода"""
        if event.type == pygame.KEYDOWN:
            if self.editing_name:
                if event.key == pygame.K_RETURN:
                    self.editing_name = False
                    self.player_name = self.name_input
                    self.options[0] = f"Имя игрока: {self.player_name}"
                elif event.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                else:
                    if len(self.name_input) < 15 and event.unicode.isprintable():
                        self.name_input += event.unicode
            else:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        self.editing_name = True
                    elif self.selected == 1:  # Добавлено - переключение музыки
                        self.music_on = not self.music_on
                        if self.music_on:
                            pygame.mixer.music.unpause()
                            self.options[1] = "Музыка: Вкл"
                        else:
                            pygame.mixer.music.pause()
                            self.options[1] = "Музыка: Выкл"
                    elif self.selected == 2:
                        return "back"
                elif event.key == pygame.K_ESCAPE:
                    return "back"
        return "settings"

    def render(self):
        """Отрисовка настроек"""
        self.screen.fill((50, 100, 150))
        self.draw_text_centered("Настройки", 50)

        for i, option in enumerate(self.options):
            color = COLOR_YELLOW if i == self.selected else COLOR_WHITE
            if i == 0 and self.editing_name:
                option_text = f"Имя игрока: {self.name_input}_"
                color = COLOR_YELLOW
            else:
                option_text = option

            self.draw_text_centered(option_text, 200 + i * 60, color=color)

        if self.editing_name:
            self.draw_text_centered("Введите новое имя и нажмите Enter", 400, self.small_font)

        # Лучшее время
        best_min = int(self.best_time // 60)
        best_sec = int(self.best_time % 60)
        best_time_text = f"Лучшее время: {best_min:02d}:{best_sec:02d}"
        self.draw_text_centered(best_time_text, 500, self.small_font)
