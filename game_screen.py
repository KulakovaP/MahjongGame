import pygame
import random
import time
from screen import BaseScreen
from tile import Tile
from tile_factory import TileFactory
from constants import *
from utils import TimeManager, load_best_time, save_best_time


class GameScreen(BaseScreen):
    """Экран игры"""

    def __init__(self, screen, resource_manager, player_name="Игрок", editor=False, filename=None, layout_index=0):
        super().__init__(screen, resource_manager)
        self.player_name = player_name
        self.editor = editor
        self.filename = filename
        self.layout_index = layout_index
        self.time_manager = TimeManager()
        self.tile_factory = TileFactory()
        self.tile_images = self.tile_factory.create_tile_images(resource_manager)
        self.reset_game()
        self.best_time = load_best_time()

    def reset_game(self):
        """Сброс игры"""
        self.tiles = []
        self.selected_tile = None
        self.time_manager.reset()
        self.time_manager.start()
        self.game_over = False
        self.win = False

        if self.editor and self.filename:
            self.load_layout()
        else:
            self.generate_layout()

    def generate_layout(self):
        """Генерация раскладки из предопределенных полей"""
        self.tiles = []
        if self.layout_index < len(CUSTOM_LAYOUTS):
            layout = CUSTOM_LAYOUTS[self.layout_index]

            # Создаем список всех типов плиток (пары)
            tile_types = []
            for i in range(1, 19):  # 18 пар (36 плиток)
                tile_types.extend([i, i])

            # Перемешиваем типы плиток
            random.shuffle(tile_types)

            # Создаем плитки с перемешанными типами, но сохраняем позиции из layout
            for i, tile_data in enumerate(layout):
                if i < len(tile_types):
                    _, x, y, z = tile_data
                    tile_type = tile_types[i]
                    tile = self.tile_factory.create_tile(tile_type, x, y, z)
                    tile.update_position()
                    self.tiles.append(tile)
        else:
            self.generate_winning_layout()

    def generate_winning_layout(self):
        """Генерация выигрышной раскладки"""
        self.tiles = []
        pairs = [(i, i) for i in range(1, 19)]
        random.shuffle(pairs)

        tile_types = []
        for pair in pairs:
            tile_types.extend(pair)

        positions = CUSTOM_LAYOUTS[0][:len(tile_types)]

        for i, tile_type in enumerate(tile_types):
            _, x, y, z = positions[i]
            tile = self.tile_factory.create_tile(tile_type, x, y, z)
            tile.update_position()
            self.tiles.append(tile)

    def handle_input(self, event):
        """Обработка ввода"""
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                return "menu"
            elif event.key == pygame.K_n:
                self.layout_index = (self.layout_index + 1) % len(CUSTOM_LAYOUTS)
                self.reset_game()
            elif self.editor and event.key == pygame.K_s:
                self.save_layout()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

        return "game"

    def handle_click(self, pos):
        """Обработка клика"""
        if self.game_over:
            return

        for tile in self.tiles:
            tile.selected = False

        clicked_tile = None
        for tile in sorted(self.tiles, key=lambda t: (-t.z, -(t.x + t.y))):
            if not tile.removed and tile.rect.collidepoint(pos):
                if not tile.is_covered(self.tiles) and not tile.is_blocked(self.tiles):
                    clicked_tile = tile
                    break

        if clicked_tile:
            if self.selected_tile is None:
                self.selected_tile = clicked_tile
                clicked_tile.selected = True
            else:
                if self.selected_tile == clicked_tile:
                    self.selected_tile.selected = False
                    self.selected_tile = None
                else:
                    self.handle_tile_match(clicked_tile)

    def handle_tile_match(self, clicked_tile):
        """Обработка совпадения плиток"""
        if self.selected_tile.tile_type == clicked_tile.tile_type:
            self.selected_tile.removed = True
            clicked_tile.removed = True

            # Проверка на победу
            if all(tile.removed for tile in self.tiles):
                self.game_over = True
                self.win = True
                self.time_manager.update()
                if self.best_time == 0 or self.time_manager.current_time < self.best_time:
                    self.best_time = self.time_manager.current_time
                    save_best_time(self.best_time)
        else:
            # Неправильное совпадение - снимаем выделение
            pass

        self.selected_tile.selected = False
        self.selected_tile = None

        # Проверка на проигрыш (нет доступных ходов)
        if not self.has_available_moves():
            self.game_over = True
            self.win = False

    def has_available_moves(self):
        """Проверка доступных ходов"""
        available_tiles = [t for t in self.tiles
                           if not t.removed
                           and not t.is_covered(self.tiles)
                           and not t.is_blocked(self.tiles)]

        type_counts = {}
        for tile in available_tiles:
            type_counts[tile.tile_type] = type_counts.get(tile.tile_type, 0) + 1

        return any(count >= 2 for count in type_counts.values())

    def update(self):
        """Обновление состояния игры"""
        if not self.game_over and not self.win:
            self.time_manager.update()

    def render(self):
        """Отрисовка игры"""
        self.screen.fill((50, 100, 150))

        # Панели сверху и снизу
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, 0, SCREEN_WIDTH, 50))
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

        if self.game_over:
            self.render_game_over()
        else:
            # Отрисовка плиток
            for tile in sorted(self.tiles, key=lambda t: (t.z, t.y, t.x)):
                if not tile.removed:
                    tile.draw(self.screen, self.tile_images)

            # Отрисовка интерфейса
            self.render_ui()

    def render_ui(self):
        """Отрисовка интерфейса"""
        # Имя игрока
        name_text = self.small_font.render(f"Игрок: {self.player_name}", True, COLOR_WHITE)
        self.screen.blit(name_text, (10, 10))

        # Время игры
        time_text = self.small_font.render(f"Время: {self.time_manager.get_formatted_time()}", True, COLOR_WHITE)
        self.screen.blit(time_text, (10, SCREEN_HEIGHT - 40))

        # Лучшее время
        best_min = int(self.best_time // 60)
        best_sec = int(self.best_time % 60)
        best_time_text = self.small_font.render(f"Лучшее: {best_min:02d}:{best_sec:02d}", True, COLOR_WHITE)
        self.screen.blit(best_time_text, (SCREEN_WIDTH - best_time_text.get_width() - 10, SCREEN_HEIGHT - 40))

        # Номер раскладки
        layout_text = self.small_font.render(f"Раскладка: {self.layout_index + 1}/{len(CUSTOM_LAYOUTS)}", True,
                                             COLOR_WHITE)
        self.screen.blit(layout_text, (SCREEN_WIDTH - layout_text.get_width() - 10, 10))

    def render_game_over(self):
        """Отрисовка экрана окончания игры"""
        # Полупрозрачный
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Основное сообщение
        if self.win:
            message = f"Вы победили! Время: {self.time_manager.get_formatted_time()}"
            self.draw_text_centered(message, SCREEN_HEIGHT // 2 - 50, color=COLOR_GREEN)

            # Если установлен новый рекорд
            if self.time_manager.current_time == self.best_time:
                self.draw_text_centered("Новый рекорд!", SCREEN_HEIGHT // 2, color=(255, 255, 0))
        else:
            self.draw_text_centered("Игра окончена", SCREEN_HEIGHT // 2 - 50, color=COLOR_RED)

        # Инструкции
        self.draw_text_centered("Нажмите R для рестарта", SCREEN_HEIGHT // 2 + 50, font=self.small_font)
        self.draw_text_centered("ESC для выхода в меню", SCREEN_HEIGHT // 2 + 90, font=self.small_font)
        self.draw_text_centered("N для смены раскладки", SCREEN_HEIGHT // 2 + 130, font=self.small_font)

    def load_layout(self):
        """Загрузка раскладки из файла"""
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        tile_type, x, y, z = map(int, parts)
                        self.tiles.append(self.tile_factory.create_tile(tile_type, x, y, z))
        except Exception as e:
            print(f"Ошибка загрузки раскладки: {e}")
            self.generate_layout()

    def save_layout(self):
        """Сохранение раскладки"""
        if not self.editor or not self.filename:
            return

        try:
            with open(self.filename, 'w') as f:
                for tile in self.tiles:
                    f.write(f"{tile.tile_type},{tile.x},{tile.y},{tile.z}\n")
            print(f"Раскладка сохранена в {self.filename}")
        except Exception as e:
            print(f"Ошибка сохранения раскладки: {e}")

    def handle_editor_input(self, event):
        """Обработка ввода в редакторе"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                # Добавление/изменение плитки
                pass
            elif event.button == 3:
                # Удаление плитки
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS:
                # Увеличение слоя
                pass
            elif event.key == pygame.K_MINUS:
                # Уменьшение слоя
                pass
