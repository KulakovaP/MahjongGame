import argparse
import pygame
import sys
from menu_screen import MenuScreen
from game_screen import GameScreen
from settings_screen import SettingsScreen
from utils import ResourceManager
from constants import *


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description='Маджонг')
    parser.add_argument('--player_name', type=str, default='Игрок', help='Имя игрока')
    parser.add_argument('--editor', action='store_true', help='Режим редактора')
    parser.add_argument('--level', type=str, help='Файл уровня для редактора')
    args = parser.parse_args()

    pygame.init()
    pygame.mixer.init()  # Инициализация аудио миксера

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Маджонг")

    resource_manager = ResourceManager()
    resource_manager.load_music(MUSIC_FILE)  # Загрузка музыки
    resource_manager.play_music()

    current_screen = "menu"
    menu = MenuScreen(screen, resource_manager, player_name=args.player_name)
    game = None
    settings = None

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_screen == "menu":
                result = menu.handle_input(event)
                if result == "game":
                    current_screen = "game"
                    game = GameScreen(
                        screen,
                        resource_manager,
                        player_name=menu.player_name,
                        editor=args.editor,
                        filename=args.level,
                        layout_index=0
                    )
                elif result == "settings":
                    current_screen = "settings"
                    settings = SettingsScreen(screen, resource_manager, menu.player_name)
                elif result == "quit":
                    running = False

            elif current_screen == "settings":
                result = settings.handle_input(event)
                if result == "back":
                    current_screen = "menu"
                    menu.player_name = settings.player_name

            elif current_screen == "game":
                result = game.handle_input(event)
                if result == "menu":
                    current_screen = "menu"
                    menu.player_name = game.player_name
                elif result == "quit":
                    running = False

        # Отрисовка
        if current_screen == "menu":
            menu.render()
        elif current_screen == "settings":
            settings.render()
        elif current_screen == "game":
            game.update()
            game.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
