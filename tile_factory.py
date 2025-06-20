import pygame
from tile import Tile
from constants import *


class TileFactory:
    """Фабрика для создания плиток"""

    @staticmethod
    def create_tile(tile_type, x, y, z=0):
        """Создание новой плитки"""
        return Tile(tile_type, x, y, z)

    @staticmethod
    def create_tile_images(resource_manager, count=36):
        """Создание изображений плиток"""
        tile_images = {}
        colors = [COLOR_RED, COLOR_GREEN, COLOR_BLUE,
                  COLOR_YELLOW, COLOR_WHITE, (255, 0, 255), (0, 255, 255)]

        font = resource_manager.load_font('small', 20)

        for i in range(1, count + 1):
            color = colors[i % len(colors)]
            tile_surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)

            # Градиент
            for y_pos in range(TILE_HEIGHT):
                alpha = 255 - int(y_pos * 0.5)
                line_color = (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255), alpha)
                pygame.draw.line(tile_surface, line_color, (2, y_pos), (TILE_WIDTH - 3, y_pos))

            pygame.draw.rect(tile_surface, COLOR_BLACK,
                             (2, 2, TILE_WIDTH - 4, TILE_HEIGHT - 4), 2, border_radius=5)

            # Номер плитки
            text = font.render(str(i), True, COLOR_BLACK)
            text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 2))
            tile_surface.blit(text, text_rect)

            tile_images[i] = tile_surface

        return tile_images
