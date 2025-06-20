import pygame
from screen import BaseScreen
from constants import *

class MenuScreen(BaseScreen):
    """Экран меню"""
    def __init__(self, screen, resource_manager, player_name="Игрок"):
        super().__init__(screen, resource_manager)
        self.player_name = player_name
        self.options = ["Новая игра", "Настройки", "Выход"]
        self.selected = 0
        self.background = resource_manager.load_image(MENU_BG)

    def handle_input(self, event):
        """Обработка ввода"""
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected] == "Новая игра":
                    return "game"
                elif self.options[self.selected] == "Настройки":
                    return "settings"
                elif self.options[self.selected] == "Выход":
                    return "quit"
            elif event.key == pygame.K_ESCAPE:
                return "quit"

        return "menu"

    def render(self):
        """Отрисовка меню"""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((50, 100, 150))

        self.draw_text_centered("Маджонг", 50)

        for i, option in enumerate(self.options):
            color = COLOR_YELLOW if i == self.selected else COLOR_WHITE
            self.draw_text_centered(option, 200 + i * 60, color=color)

        player_text = f"Игрок: {self.player_name}"
        self.draw_text_centered(player_text, SCREEN_HEIGHT - 40, self.small_font)
