import pygame
import sys
import os


# Функция для правильного определения путей к ресурсам
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Базовые размеры (оригинальное разрешение игры - ВЕРТИКАЛЬНОЕ)
BASE_WIDTH = 1530
BASE_HEIGHT = 3320

# Размеры окна (вертикальная ориентация)
WINDOW_WIDTH = 400  # Узкое окно
WINDOW_HEIGHT = 800  # Высокое окно
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Рыбалка")

# Коэффициенты масштабирования
SCALE_X = WINDOW_WIDTH / BASE_WIDTH
SCALE_Y = WINDOW_HEIGHT / BASE_HEIGHT
SCALE = min(SCALE_X, SCALE_Y)  # Используем меньший коэффициент для сохранения пропорций


class ScaleManager:
    """Менеджер масштабирования для всех игровых объектов"""

    @staticmethod
    def scale_image(image, base_width, base_height):
        """Масштабирует изображение относительно базовых размеров"""
        new_width = int(base_width * SCALE)
        new_height = int(base_height * SCALE)
        return pygame.transform.scale(image, (new_width, new_height))

    @staticmethod
    def scale_position(x, y):
        """Масштабирует позицию относительно базовых размеров"""
        return (int(x * SCALE_X), int(y * SCALE_Y))

    @staticmethod
    def get_scaled_size(base_width, base_height):
        """Возвращает масштабированные размеры"""
        return (int(base_width * SCALE), int(base_height * SCALE))


class Background:
    def __init__(self, image_path):
        try:
            full_path = resource_path(image_path)
            original_image = pygame.image.load(full_path)
            # Фон масштабируем на весь экран с сохранением пропорций
            self.image = pygame.transform.scale(original_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.image.fill((135, 206, 235))

    def draw(self, surface):
        surface.blit(self.image, (0, 0))


class Character:
    def __init__(self, idle_image_path, casting_image_path, cast_sound_path):
        # Базовые размеры персонажа (в оригинальном разрешении 1530x3320)
        self.BASE_WIDTH = 1530  # Ширина в оригинальном разрешении
        self.BASE_HEIGHT = 3320  # Высота в оригинальном разрешении

        try:
            self.idle_image = pygame.image.load(resource_path(idle_image_path))
            self.casting_image = pygame.image.load(resource_path(casting_image_path))
        except Exception as e:
            print(f"Ошибка загрузки изображений персонажа: {e}")
            # Создаем цветные прямоугольники для отладки
            self.idle_image = pygame.Surface((self.BASE_WIDTH, self.BASE_HEIGHT))
            self.idle_image.fill((255, 0, 0))  # Красный
            self.casting_image = pygame.Surface((self.BASE_WIDTH, self.BASE_HEIGHT))
            self.casting_image.fill((0, 255, 0))  # Зеленый

        # Масштабируем изображения
        self.idle_image = ScaleManager.scale_image(self.idle_image, self.BASE_WIDTH, self.BASE_HEIGHT)
        self.casting_image = ScaleManager.scale_image(self.casting_image, self.BASE_WIDTH, self.BASE_HEIGHT)

        self.current_image = self.idle_image
        self.is_casting = False

        # Создаем rect после масштабирования
        self.rect = self.current_image.get_rect()

        # Базовая позиция в оригинальном разрешении (центр по X, низ по Y)
        base_x = BASE_WIDTH // 2
        base_y = BASE_HEIGHT - 1700  # 400 пикселей от нижнего края

        # Масштабируем позицию
        scaled_x, scaled_y = ScaleManager.scale_position(base_x, base_y)
        self.rect.center = (scaled_x, scaled_y)

        # Звук заброса
        self.cast_sound = None
        try:
            if cast_sound_path:
                self.cast_sound = pygame.mixer.Sound(resource_path(cast_sound_path))
        except Exception as e:
            print(f"Ошибка загрузки звука заброса: {e}")

    def cast(self):
        self.is_casting = True
        self.current_image = self.casting_image
        if self.cast_sound:
            self.cast_sound.play()
        print("Заброс удочки!")  # Для отладки

    def idle(self):
        self.is_casting = False
        self.current_image = self.idle_image
        print("Спокойное состояние")  # Для отладки

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)


class Button:
    def __init__(self, normal_image_path, pressed_image_path, click_sound_path):
        # Базовые размеры кнопки (в оригинальном разрешении 1530x3320)
        self.BASE_WIDTH = 495
        self.BASE_HEIGHT = 495

        try:
            self.normal_image = pygame.image.load(resource_path(normal_image_path))
            self.pressed_image = pygame.image.load(resource_path(pressed_image_path))
        except Exception as e:
            print(f"Ошибка загрузки изображений кнопки: {e}")
            self.normal_image = pygame.Surface((self.BASE_WIDTH, self.BASE_HEIGHT))
            self.normal_image.fill((0, 0, 255))  # Синий
            self.pressed_image = pygame.Surface((self.BASE_WIDTH, self.BASE_HEIGHT))
            self.pressed_image.fill((0, 100, 255))  # Темно-синий

        # Масштабируем изображения
        self.normal_image = ScaleManager.scale_image(self.normal_image, self.BASE_WIDTH, self.BASE_HEIGHT)
        self.pressed_image = ScaleManager.scale_image(self.pressed_image, self.BASE_WIDTH, self.BASE_HEIGHT)

        self.current_image = self.normal_image
        self.is_pressed = False

        # Создаем rect после масштабирования
        self.rect = self.current_image.get_rect()

        # Базовая позиция в оригинальном разрешении (правый нижний угол)
        base_x = BASE_WIDTH - 950 # 400 пикселей от правого края
        base_y = BASE_HEIGHT - 800  # 400 пикселей от нижнего края

        # Масштабируем позицию
        self.rect.topleft = ScaleManager.scale_position(base_x, base_y)

        self.click_sound = None
        try:
            if click_sound_path:
                self.click_sound = pygame.mixer.Sound(resource_path(click_sound_path))
        except Exception as e:
            print(f"Ошибка загрузки звука кнопки: {e}")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.press()
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                self.release()
        return False

    def press(self):
        self.is_pressed = True
        self.current_image = self.pressed_image
        if self.click_sound:
            self.click_sound.play()
        print("Кнопка нажата!")  # Для отладки

    def release(self):
        self.is_pressed = False
        self.current_image = self.normal_image
        print("Кнопка отпущена!")  # Для отладки

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)


class Game:
    def __init__(self):
        print(f"Масштаб: {SCALE:.3f}")  # Для отладки
        print(f"Размер окна: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.background = Background("assets/background.png")
        self.character = Character(
            "assets/character_idle.png",
            "assets/character_casting.png",
            "assets/cast_sound.mp3"
        )
        self.button = Button(
            "assets/button_normal_new.png",
            "assets/button_pressed_new.png",
            "assets/button_click.mp3"
        )

        self.background_music = "assets/background_music.mp3"
        self.setup_music()
        self.clock = pygame.time.Clock()

    def setup_music(self):
        try:
            if os.path.exists(resource_path(self.background_music)):
                pygame.mixer.music.load(resource_path(self.background_music))
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                print("Фоновая музыка запущена")
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.button.handle_event(event):
                self.character.cast()
        return True

    def update(self):
        if self.character.is_casting:
            # Устанавливаем таймер для возврата в спокойное состояние
            pygame.time.set_timer(pygame.USEREVENT, 2000, True)

        # Обрабатываем пользовательские события
        for event in pygame.event.get(pygame.USEREVENT):
            if event.type == pygame.USEREVENT:
                self.character.idle()

    def draw(self):
        self.background.draw(SCREEN)
        self.character.draw(SCREEN)
        self.button.draw(SCREEN)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()