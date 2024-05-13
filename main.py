import pygame
import os
import random

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
ENERGY_BAR_WIDTH = 200
ENERGY_BAR_HEIGHT = 20
ENERGY_BAR_COLOR = (0, 255, 0)  # Green color for energy bar
ENERGY_DECREASE_RATE = 5.0  # Increased energy decrease rate per second
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pink_border_active = False
pink_border_timer = 0  # Timer for 10 seconds
PINK_BORDER_COLOR = (255, 105, 180)  # Pink color for the border

# Carregando imagens
RUNNING = [pygame.image.load(os.path.join("Assets/Boy", "BoyWalking1.png")),
           pygame.image.load(os.path.join("Assets/Boy", "BoyWalking2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Boy", "BoyJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Boy", "BoyDuck1.png")),
           pygame.image.load(os.path.join("Assets/Boy", "BoyDuck2.png"))]

OBSTACLE_ONE_SMALL = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                      pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                      pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

OBSTACLE_ONE_LARGE = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                      pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                      pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

OBSTACLE_TWO = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
                pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

POWER_SUPPLY = pygame.image.load(os.path.join("Assets/PC_Hardware", "PowerSupply.png"))
GRAPHICS_CARD = pygame.image.load(os.path.join("Assets/PC_Hardware", "GraphicsCard.png"))
SSD_IMAGE = pygame.image.load(os.path.join("Assets/PC_Hardware", "SSD.png"))

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
        self.last_energy_update_time = pygame.time.get_ticks()  # Last time energy was updated

    def update(self, userInput):
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - self.last_energy_update_time) / 1000  # Convert milliseconds to seconds
        
        # Decrease energy over time
        self.energy -= ENERGY_DECREASE_RATE * time_elapsed
        if self.energy < 0:
            self.energy = 0

        # Update last energy update time
        self.last_energy_update_time = current_time
        
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
        # Draw energy bar
        pygame.draw.rect(SCREEN, ENERGY_BAR_COLOR, (10, 10, self.energy * 2, ENERGY_BAR_HEIGHT))

class PowerSupply:
    def __init__(self, x, y):
        self.image = POWER_SUPPLY
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        player.energy += 20
        if player.energy > 100:  # Limit energy to 100
            player.energy = 100

class GraphicsCard:
    def __init__(self, x, y):
        self.image = GRAPHICS_CARD
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        global pink_border_active, pink_border_timer
        player.visibility_boost = True
        pink_border_active = True  # Activate pink border effect
        pink_border_timer = pygame.time.get_ticks()  # Start the timer

class SSD(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = SSD_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        player.speed_boost = True

def add_powerup():
    min_distance_between_powerups = 400  # Aumentando a distância mínima entre coletáveis
    if random.randint(0, 100) < 2:  # Reduzindo a probabilidade de criação de coletáveis
        powerup_type = random.choice(["power_supply", "graphics_card", "ssd"])
        new_powerup_x = SCREEN_WIDTH
        new_powerup_y = 310
        if len(powerups) > 0:
            last_powerup = powerups[-1]
            new_powerup_x = max(SCREEN_WIDTH, last_powerup.rect.x + min_distance_between_powerups)
        if powerup_type == "power_supply":
            powerups.append(PowerSupply(new_powerup_x, new_powerup_y))
        elif powerup_type == "graphics_card":
            powerups.append(GraphicsCard(new_powerup_x, new_powerup_y))
            if powerup_type == "graphics_card":
                powerups.append(GraphicsCard(new_powerup_x, new_powerup_y))
                pink_border_active = True  # Activate pink border effect
                pink_border_timer = pygame.time.get_ticks()  # Start the timer
        elif powerup_type == "ssd":
            powerups.append(SSD(new_powerup_x, new_powerup_y))
            
powerups = []

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500,3000)
            self.y = random.randint(50,100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self,image,type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        

    def update(self):
       self.rect.x -= game_speed
       if self.rect.x < -self.rect.width:
           obstacles.pop()

       
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
     def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def menu(death_count, points):
    run = True
    while run:
        SCREEN.fill((255,255,255))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Pressione qualquer tecla para começar!", True, (0,0,0))

        elif death_count > 0:
            text = font.render("Pressione qualquer tecla para recomeçar!", True, (0,0,0))
            score = font.render("Pontuação: " + str(points), True, (0,0,0))  # Display score points
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Exit the game
                run = False  # Ensure the loop exits
            if event.type == pygame.KEYDOWN:
                main()

#main
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, pink_border_active, pink_border_timer
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    
    def check_energy():
        if player.energy <= 0:
            return True
        return False

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Pontos: " + str(points), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG,  (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Exit the game
                run = False  # Ensure the loop exits

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        add_powerup()
        
        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallCactus(OBSTACLE_ONE_SMALL))
            elif random.randint(0,2) == 1:
                obstacles.append(LargeCactus(OBSTACLE_ONE_LARGE))
            elif random.randint(0,2) == 2:
                obstacles.append(Bird(OBSTACLE_TWO))
                
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1500)
                death_count += 1
                menu(death_count, points)  # Pass points to the menu

        for item in powerups:
            item.rect.x -= game_speed
            SCREEN.blit(item.image, item.rect)
            if item.rect.x < -item.rect.width:
                powerups.remove(item)
            if pink_border_active:
                pygame.draw.rect(SCREEN, PINK_BORDER_COLOR, item.rect, 3)  # Draw pink border
            SCREEN.blit(item.image, item.rect)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        if check_energy():
            menu(death_count, points)  # Pass points to the menu
            run = False  # End the game and return to menu
            
        current_time = pygame.time.get_ticks()
        if pink_border_active and current_time - pink_border_timer > 10000:  # Check if 10 seconds have passed
            pink_border_active = False  # Deactivate pink border effect
        
        pygame.display.update()
        clock.tick(30)

main()
