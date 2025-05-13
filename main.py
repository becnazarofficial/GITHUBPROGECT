import pygame
import random
import asyncio
import platform

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
WATERMELON_RADIUS = 20
FPS = 60

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лови Арбуз!")
clock = pygame.time.Clock()

# Переменные игры
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
basket_speed = 5
watermelons = []
score = 0
game_over = False

# Шрифт для отображения счёта и текста
font = pygame.font.SysFont("Arial", 36)

def setup():
    """Инициализация начального состояния игры"""
    global basket_x, score, watermelons, game_over
    basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
    score = 0
    watermelons = []
    game_over = False

def spawn_watermelon():
    """Создание нового арбуза в случайной позиции наверху экрана"""
    x = random.randint(WATERMELON_RADIUS, SCREEN_WIDTH - WATERMELON_RADIUS)
    watermelons.append([x, 0])

def update_loop():
    """Основной цикл обновления игры"""
    global basket_x, score, game_over

    if game_over:
        return

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Управление корзиной
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - BASKET_WIDTH:
        basket_x += basket_speed

    # Создание нового арбуза с некоторой вероятностью
    if random.random() < 0.02:
        spawn_watermelon()

    # Обновление позиций арбузов
    for watermelon in watermelons[:]:
        watermelon[1] += 3  # Скорость падения
        # Проверка, пойман ли арбуз
        if (basket_y < watermelon[1] + WATERMELON_RADIUS and
                basket_x < watermelon[0] < basket_x + BASKET_WIDTH):
            watermelons.remove(watermelon)
            score += 1
        # Проверка, упал ли арбуз
        elif watermelon[1] > SCREEN_HEIGHT:
            watermelons.remove(watermelon)
            game_over = True

    # Отрисовка
    screen.fill(WHITE)
    
    # Отрисовка корзины
    pygame.draw.rect(screen, BROWN, (basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT))
    
    # Отрисовка арбузов
    for watermelon in watermelons:
        # Зелёная кожура
        pygame.draw.circle(screen, GREEN, (watermelon[0], watermelon[1]), WATERMELON_RADIUS)
        # Красная мякоть
        pygame.draw.circle(screen, RED, (watermelon[0], watermelon[1]), WATERMELON_RADIUS - 5)
    
    # Отрисовка счёта
    score_text = font.render(f"Счёт: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    # Отрисовка текста при проигрыше
    if game_over:
        game_over_text = font.render("Игра окончена! Нажмите R для рестарта", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        
        # Проверка нажатия R для рестарта
        if keys[pygame.K_r]:
            setup()

    pygame.display.flip()

async def main():
    """Основная функция для асинхронного выполнения"""
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())