import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра на выживание")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Параметры игрока
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

# Параметры врагов
enemy_size = 50
enemy_list = []
enemy_speed = 3

# Функция для генерации нового врага в случайной позиции
def create_enemy():
    x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
    y_pos = random.randint(0, SCREEN_HEIGHT - enemy_size)
    return [x_pos, y_pos]

# Функция для перемещения врагов
def move_enemies():
    for enemy in enemy_list:
        enemy[1] += enemy_speed  # Двигаем врагов вниз
        # Перемещаем врага обратно вверх, если он выходит за экран
        if enemy[1] > SCREEN_HEIGHT:
            enemy[0] = random.randint(0, SCREEN_WIDTH - enemy_size)
            enemy[1] = 0

# Функция для проверки столкновений
def check_collision(player_pos, enemies):
    for enemy in enemies:
        if (player_pos[0] < enemy[0] + enemy_size and
            player_pos[0] + player_size > enemy[0] and
            player_pos[1] < enemy[1] + enemy_size and
            player_pos[1] + player_size > enemy[1]):
            return True
    return False

# Счетчик времени выживания
clock = pygame.time.Clock()
survival_time = 0

# Основной цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получение нажатых клавиш для управления игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += player_speed

    # Добавление новых врагов с увеличением времени
    if random.randint(1, 20) == 1:
        enemy_list.append(create_enemy())

    # Движение врагов и проверка столкновений
    move_enemies()
    if check_collision(player_pos, enemy_list):
        print(f"Вы проиграли! Время выживания: {survival_time // 1000} секунд")
        running = False

    # Заливка фона
    screen.fill(WHITE)

    # Отрисовка игрока
    pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))

    # Отрисовка врагов
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

    # Обновление времени выживания и его вывод
    survival_time += clock.get_time()
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Время выживания: {survival_time // 1000} сек", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Обновление дисплея и ограничение кадров
    pygame.display.flip()
    clock.tick(30)  # 30 FPS

# Завершение работы Pygame
pygame.quit()
sys.exit()
