import pygame
from constants import *


class Tile:
    """Класс плитки маджонга"""

    def __init__(self, tile_type, x, y, z=0):
        self.tile_type = tile_type
        self.x = x
        self.y = y
        self.z = z
        self.selected = False
        self.removed = False
        self.rect = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        self.update_position()

    def update_position(self):
        """Обновление позиции плитки на экране"""
        field_offset_x = (SCREEN_WIDTH - 1080) // 2  # Центрирование поля
        field_offset_y = 50  # Отступ сверху

        self.rect.x = field_offset_x + self.x - self.z * 5
        self.rect.y = field_offset_y + self.y - self.z * 5
        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT

    def draw(self, surface, tile_images):
        """Отрисовка плитки"""
        if self.removed:
            return

        # Тень
        shadow_rect = self.rect.move(3, 3)
        shadow = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 100))
        surface.blit(shadow, shadow_rect)

        # Сама плитка
        if tile_images and self.tile_type in tile_images:
            surface.blit(tile_images[self.tile_type], self.rect)
        else:
            color = [
                COLOR_RED, COLOR_GREEN, COLOR_BLUE,
                COLOR_YELLOW, COLOR_PINK, COLOR_WHITE
            ][self.tile_type % 6]
            pygame.draw.rect(surface, color, self.rect, border_radius=5)
            pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2, border_radius=5)
            font = pygame.font.SysFont('Arial', 20)
            text = font.render(str(self.tile_type), True, COLOR_BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

        # Выделение
        if self.selected:
            pygame.draw.rect(surface, COLOR_RED, self.rect.inflate(4, 4), 2, border_radius=7)

    def is_covered(self, all_tiles):
        """Проверка, закрыта ли плитка другими"""
        for tile in all_tiles:
            if tile != self and not tile.removed and self.is_covered_by(tile):
                return True
        return False

    def is_covered_by(self, other):
        """Проверка, перекрывает ли другая плитка текущую"""
        if other.removed or self.removed:
            return False

        return (other.z > self.z and
                abs(other.rect.x - self.rect.x) < TILE_WIDTH and
                abs(other.rect.y - self.rect.y) < TILE_HEIGHT)

    def is_blocked(self, tiles):
        """Проверка, заблокирована ли плитка"""
        for tile in tiles:
            if tile != self and not tile.removed and tile.z > self.z:
                if (abs(tile.rect.x - self.rect.x) < TILE_WIDTH and
                        abs(tile.rect.y - self.rect.y) < TILE_HEIGHT):
                    return True
        return False
