import pygame
import os
import random

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Boy","BoyWalking1.png")),
           pygame.image.load(os.path.join("Assets/Boy","BoyWalking2.png"))]


JUMPING = pygame.image.load(os.path.join("Assets/Boy","BoyJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Boy","BoyDuck1.png")),
           pygame.image.load(os.path.join("Assets/Boy","BoyDuck2.png"))]

OBSTACLE_ONE_SMALL = [pygame.image.load(os.path.join("Assets/Cactus","SmallCactus1.png")),
           pygame.image.load(os.path.join("Assets/Cactus","SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus","SmallCactus3.png"))]

OBSTACLE_ONE_LARGE = [pygame.image.load(os.path.join("Assets/Cactus","LargeCactus1.png")),
           pygame.image.load(os.path.join("Assets/Cactus","LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus","LargeCactus3.png"))]

OBSTACLE_TWO = [pygame.image.load(os.path.join("Assets/Bird","Bird1.png")),
           pygame.image.load(os.path.join("Assets/Bird","Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other","Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other","Track.png"))

POWER_SUPPLY = pygame.image.load(os.path.join("Assets/PC_Hardware", "PowerSupply.png"))
GRAPHICS_CARD = pygame.image.load(os.path.join("Assets/PC_Hardware", "GraphicsCard.png"))
SSD = pygame.image.load(os.path.join("Assets/PC_Hardware", "SSD.png"))

class Dinosaur:
    def __init__(self):
        self.energy = 100
        self.visibility_boost = False
        self.speed_boost = False
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.step_index = 0
        self.jump_vel = 8.5
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = 310

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        for item in powerups:
            if self.dino_rect.colliderect(item.rect):
                item.effect(self)
                powerups.remove(item)

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = 340
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = 310
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -8.5:
            self.dino_jump = False
            self.jump_vel = 8.5

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class PowerSupply:
    def __init__(self, x, y):
        self.image = POWER_SUPPLY
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        player.energy += 20

class GraphicsCard:
    def __init__(self, x, y):
        self.image = GRAPHICS_CARD
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        player.visibility_boost = True

class SSD(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets/PC_Hardware","SSD.png"))  # SSD_IMAGE deve ser substituído pela sua imagem do SSD
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        player.speed_boost = True

def add_powerup():
    if random.randint(0, 100) < 5:
        powerup_type = random.choice(["power_supply", "graphics_card", "ssd"])
        if powerup_type == "power_supply":
            powerups.append(PowerSupply(SCREEN_WIDTH, 310))
        elif powerup_type == "graphics_card":
            powerups.append(GraphicsCard(SCREEN_WIDTH, 310))
        elif powerup_type == "ssd":
            powerups.append(SSD(SCREEN_WIDTH, 310))

powerups = []

def main():
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 14
    x_pos_bg = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        add_powerup()

        for item in powerups:
            item.rect.x -= game_speed
            SCREEN.blit(item.image, item.rect)
            if item.rect.x < -item.rect.width:
                powerups.remove(item)

        x_pos_bg -= game_speed
        SCREEN.blit(BG, (x_pos_bg, 380))
        SCREEN.blit(BG, (BG.get_width() + x_pos_bg, 380))
        if x_pos_bg <= -BG.get_width():
            x_pos_bg = 0

        pygame.display.update()
        clock.tick(30)

main()