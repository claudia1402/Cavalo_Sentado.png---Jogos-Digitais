import pygame
import os
import random
import time

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100


ENERGY_BAR_WIDTH = 200
ENERGY_BAR_HEIGHT = 20
ENERGY_BAR_COLOR = (0, 255, 0)  # Green color for energy bar
ENERGY_DECREASE_RATE = 3.0  # Increased energy decrease rate per second


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pink_border_active = False
pink_border_timer = 0  # Timer for 10 seconds
PINK_BORDER_COLOR = (255, 105, 180)  # Pink color for the border

class PointsUI:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2  # Centered horizontally
        self.y = 100  # At the top of the screen
        self.text = "+50 points!"
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)  # White color
        self.visible = False
        self.timer = 0

    def show(self):
        self.visible = True
        self.timer = pygame.time.get_ticks()

    def update(self):
        if self.visible:
            if pygame.time.get_ticks() - self.timer > 1000:  # UI stays visible for 1 second
                self.visible = False

    def draw(self, screen):
        if self.visible:
            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            screen.blit(text_surface, text_rect)




# Carregando imagens
NEW_BG = pygame.image.load(os.path.join("Assets/Other", "NewBackground.jpeg"))

RUNNING = [pygame.image.load(os.path.join("Assets/Boy", "BoyWalking1.png")),
           pygame.image.load(os.path.join("Assets/Boy", "BoyWalking2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Boy", "BoyJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Boy", "BoyDuck1.png")),
           pygame.image.load(os.path.join("Assets/Boy", "BoyDuck2.png"))]

OBSTACLE_ONE_SMALL = [pygame.image.load(os.path.join("Assets/Cables", "SmallCable11.png")),
                      pygame.image.load(os.path.join("Assets/Cables", "SmallCable22.png")),
                      pygame.image.load(os.path.join("Assets/Cables", "SmallCable33.png"))]

OBSTACLE_ONE_LARGE = [pygame.image.load(os.path.join("Assets/Cables", "LargeCable11.png")),
                      pygame.image.load(os.path.join("Assets/Cables", "LargeCable22.png")),
                      pygame.image.load(os.path.join("Assets/Cables", "LargeCable33.png"))]

OBSTACLE_TWO = [pygame.image.load(os.path.join("Assets/FlyEnemy", "FlyEnemy1.png")),
                pygame.image.load(os.path.join("Assets/FlyEnemy", "FlyEnemy2.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track3.png"))

POWER_SUPPLY = pygame.image.load(os.path.join("Assets/PC_Hardware", "PowerSupply2.png"))
GRAPHICS_CARD = pygame.image.load(os.path.join("Assets/PC_Hardware", "GraphicsCard2.png"))
SSD_IMAGE = pygame.image.load(os.path.join("Assets/PC_Hardware", "SSD2.png"))

class Boy:
    def __init__(self):
        self.energy = 100
        self.visibility_boost = False
        self.speed_boost = False
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.boy_duck = False
        self.boy_run = True
        self.boy_jump = False
        self.step_index = 0
        self.jump_vel = 7.4
        self.image = self.run_img[0]
        self.boy_rect = self.image.get_rect()
        self.boy_rect.x = 80
        self.boy_rect.y = 310
        self.last_energy_update_time = pygame.time.get_ticks()  # Last time energy was updated

    def update(self, userInput):
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - self.last_energy_update_time) / 1000  # Convert milliseconds to seconds
        
         # Debug print
        print("Current Energy:", self.energy)
        
        # Decrease energy over time
        self.energy -= ENERGY_DECREASE_RATE / 60
        if self.energy < 0:
            self.energy = 0
            
        

        # Update last energy update time
        self.last_energy_update_time = current_time
        
        if self.boy_duck:
            self.duck()
        if self.boy_run:
            self.run()
        if self.boy_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        for item in powerups:
            if self.boy_rect.colliderect(item.rect):
                item.effect(self)
                powerups.remove(item)

        if userInput[pygame.K_UP] and not self.boy_jump:
            self.boy_duck = False
            self.boy_run = False
            self.boy_jump = True

        elif userInput[pygame.K_DOWN] and not self.boy_jump:
            self.boy_duck = True
            self.boy_run = False
            self.boy_jump = False

        elif not (self.boy_jump or userInput[pygame.K_DOWN]):
            self.boy_duck = False
            self.boy_run = True
            self.boy_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        
        self.boy_rect.x = 90
        self.boy_rect.y = 330
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        
        self.boy_rect.x = 80
        self.boy_rect.y = 295
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.boy_jump:
            self.boy_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.4
        if self.jump_vel < -10.0:
            self.boy_jump = False
            self.jump_vel = 7.4

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.boy_rect.x, self.boy_rect.y))
        # Draw energy bar
        pygame.draw.rect(SCREEN, ENERGY_BAR_COLOR, (10, 10, self.energy * 2, ENERGY_BAR_HEIGHT))
        pygame.draw.rect(SCREEN, (0, 0, 0), (10, 10, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT), 2)

class PowerSupply:
    def __init__(self, x, y):
        self.image = POWER_SUPPLY
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        global points
        player.energy += 20
        if player.energy > 100:  # Limit energy to 100
            player.energy = 100
        points += 50
        points_ui.show()
        
        # Debug print
        print("Player Energy after collecting Power Supply:", player.energy)

class GraphicsCard:
    def __init__(self, x, y):
        self.image = GRAPHICS_CARD
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        global pink_border_active, pink_border_timer, points
        player.visibility_boost = True
        pink_border_active = True  # Activate pink border effect
        pink_border_timer = pygame.time.get_ticks()  # Start the timer
        points += 50
        points_ui.show()

class SSD(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = SSD_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, player):
        global game_speed, points  # Access the global game_speed variable
        player.speed_boost = True
        game_speed += 0.5
        points += 50
        points_ui.show()
        
def add_powerup():
    min_distance_between_powerups = 400  # Aumentando a distância mínima entre coletáveis
    if random.randint(0, 100) < 2:  # Reduzindo a probabilidade de criação de coletáveis
        powerup_type = random.choice(["power_supply", "graphics_card", "ssd"])
        new_powerup_x = SCREEN_WIDTH
        new_powerup_y = 310
        if len(powerups) > 0:
            last_powerup = powerups[-1]
            min_distance_between_powerups = max(min_distance_between_powerups, last_powerup.rect.width + 600)
            new_powerup_x = max(SCREEN_WIDTH, last_powerup.rect.x + min_distance_between_powerups)
        # Check for overlap with obstacles
        new_powerup_rect = pygame.Rect(new_powerup_x, new_powerup_y, POWER_SUPPLY.get_width(), POWER_SUPPLY.get_height())
        overlapping = False
        for obstacle in obstacles:
            if obstacle.rect.colliderect(new_powerup_rect):
                overlapping = True
                break
        
        for existing_powerup in powerups:
            if existing_powerup.rect.colliderect(new_powerup_rect):
                overlapping = True
                break
        for existing_powerup in powerups:
            if existing_powerup != last_powerup:  # Exclude checking against the last added powerup
                if existing_powerup.rect.colliderect(new_powerup_rect):
                    overlapping = True
                    break
        
        if not overlapping:  # Only add if no overlap with obstacles
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

class SmallCable(Obstacle):
     def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCable(Obstacle):
    def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class FlyEnemy(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 180
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def draw_new_background(screen):
    scaled_bg = pygame.transform.scale(NEW_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))  

    # Create a semi-transparent black surface with the same dimensions as the screen
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Fill the surface with black color and set transparency to 100 (semi-transparent)
    screen.blit(overlay, (0, 0))  # Draw the overlay on top of the background

def gameOver(death_count, points):
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

points_ui = PointsUI()

def menu_screen():
    global SCREEN, NEW_BG
    run_menu = True
    font = pygame.font.Font("freesansbold.ttf", 40)
    play_text = font.render("Jogar", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    help_text = font.render("Como Funciona", True, (255, 255, 255))
    help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, 300))

    while run_menu:
        # Scale and blit background image to cover the entire screen
        scaled_bg = pygame.transform.scale(NEW_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.blit(scaled_bg, (0, 0))
        
        # Blit semi-transparent black surface
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 128 for semi-transparency
        SCREEN.blit(overlay, (0, 0))
        
        # Blit menu text
        SCREEN.blit(play_text, play_rect)
        SCREEN.blit(help_text, help_rect)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if help_rect.collidepoint(mouse_pos):
                    run_menu = False
                    help_screen()
                elif play_rect.collidepoint(mouse_pos):
                    run_menu = False
                    countdown_screen()

def countdown_screen():
    global SCREEN
    font = pygame.font.Font("freesansbold.ttf", 100)
    countdown_text = [font.render("3", True, (255, 255, 255)),
                      font.render("2", True, (255, 255, 255)),
                      font.render("1", True, (255, 255, 255)),
                      font.render("Go!", True, (255, 255, 255))]
    countdown_rect = countdown_text[0].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    for i in range(3, 0, -1):
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(countdown_text[i - 1], countdown_rect)
        pygame.display.update()
        time.sleep(1)

    main()

def help_screen():
    global SCREEN
    run_help = True
    font = pygame.font.Font("freesansbold.ttf", 30)
    title_text = font.render("Help", True, (255, 255, 255))
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    lorem_ipsum_text = font.render(lorem_ipsum, True, (255, 255, 255))
    back_text = font.render("Back", True, (255, 255, 255))
    back_rect = back_text.get_rect(topleft=(20, 20))  # Position top left
    
    while run_help:
        SCREEN.fill((0, 0, 0))
        
        # Draw "Back" label
        SCREEN.blit(back_text, back_rect)
        
        # Draw title and lorem ipsum text
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        SCREEN.blit(lorem_ipsum_text, (50, 200))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run_help = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):  # Check if mouse click is on "Back" label
                    run_help = False
                    menu_screen()

#main
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, pink_border_active, pink_border_timer
    run = True
    clock = pygame.time.Clock()
    player = Boy()
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
            game_speed += 0.2

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
        player.update(userInput)
        draw_new_background(SCREEN)

        player.draw(SCREEN)
        player.update(userInput)

        add_powerup()
        
        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallCable(OBSTACLE_ONE_SMALL))
            elif random.randint(0,2) == 1:
                obstacles.append(LargeCable(OBSTACLE_ONE_LARGE))
            elif random.randint(0,2) == 2:
                obstacles.append(FlyEnemy(OBSTACLE_TWO))
                
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.boy_rect.colliderect(obstacle.rect):
                pygame.time.delay(1500)
                death_count += 1
                gameOver(death_count, points)  # Pass points to the gameOver

        for item in powerups:
            if player.boy_rect.colliderect(item.rect):
                item.effect(player)
                powerups.remove(item)
                points_ui.show()
            item.rect.x -= game_speed
            SCREEN.blit(item.image, item.rect)
            if item.rect.x < -item.rect.width:
                powerups.remove(item)
            if pink_border_active:
                pygame.draw.rect(SCREEN, PINK_BORDER_COLOR, item.rect, 3)  # Draw pink border
            SCREEN.blit(item.image, item.rect)
            
        points_ui.update()
        points_ui.draw(SCREEN)

        background()

        score()

        if check_energy():
            gameOver(death_count, points)  # Pass points to the gameOver
            run = False  # End the game and return to gameOver
            
        current_time = pygame.time.get_ticks()
        if pink_border_active and current_time - pink_border_timer > 10000:  # Check if 10 seconds have passed
            pink_border_active = False  # Deactivate pink border effect
        
        pygame.display.update()
        clock.tick(60)

menu_screen()
