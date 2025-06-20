import os
import pygame
import time
from constants import *


class TimeManager:
    """Класс для управления временем игры"""

    def __init__(self):
        self.start_time = 0
        self.current_time = 0
        self.paused_time = 0
        self.pause_start = 0

    def start(self):
        """Запуск таймера"""
        self.start_time = time.time()

    def pause(self):
        """Пауза таймера"""
        self.pause_start = time.time()

    def resume(self):
        """Возобновление таймера"""
        if self.pause_start:
            self.paused_time += time.time() - self.pause_start
            self.pause_start = 0

    def update(self):
        """Обновление текущего времени"""
        if not self.pause_start:
            self.current_time = time.time() - self.start_time - self.paused_time

    def get_formatted_time(self):
        """Получение отформатированного времени (MM:SS)"""
        minutes = int(self.current_time // 60)
        seconds = int(self.current_time % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def reset(self):
        """Сброс таймера"""
        self.start_time = time.time()
        self.current_time = 0
        self.paused_time = 0
        self.pause_start = 0


class ResourceManager:
    """Класс для управления ресурсами (шрифты, изображения)"""

    def __init__(self):
        self.fonts = {}
        self.images = {}

    def load_font(self, name, size):
        """Загрузка шрифта"""
        key = f"{name}_{size}"
        if key not in self.fonts:
            try:
                font_path = os.path.abspath(FONT_FILE)
                if os.path.exists(font_path):
                    self.fonts[key] = pygame.font.Font(font_path, size)
                else:
                    raise FileNotFoundError
            except:
                self.fonts[key] = pygame.font.SysFont('Arial', size, bold=True)
        return self.fonts[key]

    def load_image(self, path):
        """Загрузка изображения"""
        if path not in self.images:
            try:
                img_path = os.path.abspath(path)
                if os.path.exists(img_path):
                    self.images[path] = pygame.image.load(img_path)
                else:
                    self.images[path] = None
            except:
                self.images[path] = None
        return self.images[path]

    def load_music(self, path):
        """Загрузка музыки"""
        try:
            pygame.mixer.music.load(path)
            self.music_loaded = True
        except Exception as e:
            print(f"Не удалось загрузить музыку: {e}")
            self.music_loaded = False

    def play_music(self, loops=-1, volume=0.5):
        """Воспроизведение музыки (loops=-1)"""
        if self.music_loaded:
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)

    def stop_music(self):
        """Остановка музыки"""
        pygame.mixer.music.stop()


def save_best_time(time_value):
    """Сохранение лучшего времени в файл"""
    try:
        with open(BEST_TIME_FILE, 'w') as f:
            f.write(str(time_value))
    except:
        pass


def load_best_time():
    """Загрузка лучшего времени из файла"""
    try:
        with open(BEST_TIME_FILE, 'r') as f:
            return float(f.read())
    except:
        return 0
