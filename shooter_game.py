import pygame
import random

pygame.init()
window_size = (700, 500)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("КОСМОС")

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, window_size)

sprite2 = pygame.image.load("rocket.png")
sprite2 = pygame.transform.scale(sprite2, (75, 75))

sprite2_x, sprite2_y = (window_size[0] - sprite2.get_width()) // 2, window_size[1] - sprite2.get_height()


pygame.mixer.music.load("space.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

font = pygame.font.Font(None, 36)
score = 0
missed = 0

shoot_sound = pygame.mixer.Sound("fire.ogg")

win_condition = 10
lose_condition = 3


game_paused = False
game_over = False

def show_message(message):
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    screen.blit(text, text_rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ufo.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = random.randint(1, 2)

    def reset_position(self):
        self.rect.x = random.randint(0, window_size[0] - self.rect.width)
        self.rect.y = random.randint(-self.rect.height, -self.rect.height // 2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_size[1]:
            self.reset_position()
            global missed
            missed += 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for _ in range(5):
    enemy = Enemy()
    enemies.add(enemy)

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_paused:
            bullet = Bullet(sprite2_x + sprite2.get_width() // 2, sprite2_y)
            bullets.add(bullet)
            shoot_sound.play()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p and not game_over:
            game_paused = not game_paused

    keys_pressed = pygame.key.get_pressed()

    if not game_paused:
        if keys_pressed[pygame.K_LEFT] and sprite2_x > 0:
            sprite2_x -= 10
        if keys_pressed[pygame.K_RIGHT] and sprite2_x < window_size[0] - sprite2.get_width():
            sprite2_x += 10

        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))
        screen.blit(sprite2, (sprite2_x, sprite2_y))

        enemies.update()
        enemies.draw(screen)

        bullets.update()
        bullets.draw(screen)

        hits = pygame.sprite.groupcollide(bullets, enemies, False, False)
        for bullet, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.reset_position()
                score += 1
            bullet.kill()

        if score >= win_condition:
            game_over = True

        if missed >= lose_condition:
            game_over = True

        text = font.render(f"Сбито: {score} Пропущено: {missed}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    if game_over:
        if score >= win_condition:
            show_message("WIN")
        else:
            show_message("LOSE")

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()