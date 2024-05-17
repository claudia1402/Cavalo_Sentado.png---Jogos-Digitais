import pygame
import os
import random
import time
import pygame.freetype


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
    global score_saved
    score_saved = False
    run = True
    font = pygame.font.Font("freesansbold.ttf", 30)
    menu_text = font.render("Menu", True, (0, 0, 0))
    restart_text = font.render("Restart", True, (0, 0, 0))
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 100))

    while run:
        SCREEN.fill((0, 0, 0))

        if death_count == 0:
            text = font.render("GAME OVER!", True, (255, 255, 255))
        elif death_count > 0:
            text = font.render("GAME OVER!", True, (255, 255, 255))
            score = font.render("Sua Pontuação: " + str(points), True, (255, 255, 255))
            score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            SCREEN.blit(score, score_rect)

        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(text, text_rect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))

        pygame.draw.rect(SCREEN, (200, 200, 200), menu_rect)
        pygame.draw.rect(SCREEN, (200, 200, 200), restart_rect)
        SCREEN.blit(menu_text, menu_rect)
        SCREEN.blit(restart_text, restart_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Exit the game
                run = False  # Ensure the loop exits
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_rect.collidepoint(mouse_pos):
                    menu_screen()  # Return to the menu screen if the "Menu" button is clicked
                    run = False
                elif restart_rect.collidepoint(mouse_pos):
                    main()  # Restart the game if the "Restart" button is clicked
                    run = False
        if not score_saved:  # Check if the score has not been saved already
            save_score(player_name, points)  # Save the player's name and score
            score_saved = True  # Set the flag to indicate that the score has been saved


points_ui = PointsUI()

def menu_screen():
    global SCREEN, NEW_BG
    run_menu = True
    font = pygame.font.Font("freesansbold.ttf", 40)
    play_text = font.render("Jogar", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    help_text = font.render("Como Funciona", True, (255, 255, 255))
    help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    
    name_input_rect = pygame.Rect(400, 200, 300, 40)
    global player_name
    player_name = ""

    while run_menu:
        # Scale and blit background image to cover the entire screen
        scaled_bg = pygame.transform.scale(NEW_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.blit(scaled_bg, (0, 0))
        
        # Blit semi-transparent black surface
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 128 for semi-transparency
        SCREEN.blit(overlay, (0, 0))
        
        #input text
        pygame.draw.rect(SCREEN, (255, 255, 255), name_input_rect, 2)
        font = pygame.freetype.SysFont(None, 32)
        font.render_to(SCREEN, (name_input_rect.x + 5, name_input_rect.y + 5), player_name, (255, 255, 255))
        
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
                if play_rect.collidepoint(mouse_pos):
                    if player_name.strip():  # Check if player name is not empty or only contains spaces
                        run_menu = False
                        countdown_screen()  # Start the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Remove last character
                else:
                    player_name += event.unicode  # Add typed character to player name


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
  

    
def help_screen_2():
    global SCREEN
    run_help_2 = True
    font_title = pygame.font.Font("freesansbold.ttf", 40)
    font_subtitle = pygame.font.Font("freesansbold.ttf", 30)
    font_description = pygame.font.Font("freesansbold.ttf", 10)
    cable_card_image = OBSTACLE_ONE_SMALL 
    cable_card_image2 = OBSTACLE_ONE_SMALL 
    cable_card_image3 = OBSTACLE_ONE_SMALL
    enemy_card_image = OBSTACLE_TWO

    title_text = font_title.render("Como Funciona - EVITE", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    


    back_text = font_subtitle.render("voltar", True, (255, 255, 255))
    back_rect = back_text.get_rect(topleft=(20, 20))

    cable1_card_image_rect = cable_card_image[0].get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))  # Positioned at center-left
    description_cables = font_description.render("Pule os cabos com mau contato com a Seta para cima!", True, (255, 255, 255))
    description_cables_rect = description_cables.get_rect(center=(SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 70))
    
    
    enemy_card_image_rect = enemy_card_image[0].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # Positioned at center-left
    description_enemy = font_description.render("Agache com a Seta para baixo para escapar do Super Malware!", True, (255, 255, 255))
    description_enemy_rect = description_enemy.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))



    while run_help_2:
        SCREEN.fill((0, 0, 0))

        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(back_text, back_rect)
        # Add any additional content rendering here

        SCREEN.blit(cable_card_image[0], cable1_card_image_rect)
        SCREEN.blit(description_cables, description_cables_rect)
        
        SCREEN.blit(enemy_card_image[0], enemy_card_image_rect)
        SCREEN.blit(description_enemy, description_enemy_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run_help_2 = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    run_help_2 = False
                    help_screen()  # Return to the previous help screen if the "Back" button is clicked


                
    
def help_screen():
    global SCREEN
    run_help = True
    font_title = pygame.font.Font("freesansbold.ttf", 40)
    font_subtitle = pygame.font.Font("freesansbold.ttf", 30)
    font_description = pygame.font.Font("freesansbold.ttf", 10)
    graphic_card_image = GRAPHICS_CARD  # Assuming GRAPHICS_CARD is the image for the graphic card
    SSD_card_image = SSD_IMAGE
    PowerSupply_card_image = POWER_SUPPLY

    title_text = font_title.render("Como Funciona - Colete", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))

    back_text = font_subtitle.render("Voltar", True, (255, 255, 255))
    back_rect = back_text.get_rect(topleft=(20, 20))

    next_text = font_subtitle.render("Próximo", True, (255, 255, 255))
    next_rect = next_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    
    title_subtext = font_subtitle.render("Ganhe pontos conforme o tempo passa!", True, (255, 255, 255))
    title_subtext_rect = title_subtext.get_rect(center=(SCREEN_WIDTH // 2, 150))
    
    
    #GraphicCard
    description_GraphicCard = font_description.render("Colete a placa de video para visualizar os coletáveis melhor por 5 segundos", True, (255, 255, 255))
    description_GraphicCard_rect = description_GraphicCard.get_rect(center=(SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 70))

    description_GraphicCard2 = font_description.render("+50 PONTOS", True, (255, 255, 255))
    additional_rect = description_GraphicCard2.get_rect(center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 150))

    graphic_card_rect = graphic_card_image.get_rect(center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 50))
    
    #SSD
    description_SSD = font_description.render("Colete o SSD para aumentar a velocidade do jogo", True, (255, 255, 255))
    description_SSD_rect = description_SSD.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

    description_SSD2 = font_description.render("+50 PONTOS", True, (255, 255, 255))
    additional_SSD_rect = description_SSD2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

    SSD_card_image_rect = SSD_card_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    
    #PowerSupply
    description_PowerSuplly = font_description.render("Colete fontes para recuperar vida", True, (255, 255, 255))
    description_PowerSuplly_rect = description_PowerSuplly.get_rect(center=(SCREEN_WIDTH // 1.2, SCREEN_HEIGHT // 2 + 70))

    description_PowerSuplly2 = font_description.render("+50 PONTOS", True, (255, 255, 255))
    description_PowerSuplly2_rect = description_PowerSuplly2.get_rect(center=(SCREEN_WIDTH // 1.2, SCREEN_HEIGHT // 2 + 150))

    PowerSupply_card_image_rect = PowerSupply_card_image.get_rect(center=(SCREEN_WIDTH // 1.2, SCREEN_HEIGHT // 2 - 50))

    while run_help:
        SCREEN.fill((0, 0, 0))

        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(back_text, back_rect)
        SCREEN.blit(next_text, next_rect)
        SCREEN.blit(title_subtext, title_subtext_rect)
        SCREEN.blit(description_GraphicCard, description_GraphicCard_rect)
        SCREEN.blit(description_GraphicCard2, additional_rect)
        SCREEN.blit(graphic_card_image, graphic_card_rect)
        SCREEN.blit(description_SSD, description_SSD_rect)
        SCREEN.blit(description_SSD2, additional_SSD_rect)
        SCREEN.blit(SSD_card_image, SSD_card_image_rect)
        
        SCREEN.blit(description_PowerSuplly, description_PowerSuplly_rect)
        SCREEN.blit(description_PowerSuplly2, description_PowerSuplly2_rect)
        SCREEN.blit(PowerSupply_card_image, PowerSupply_card_image_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run_help = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    run_help = False
                    menu_screen()  # Return to the home screen if the "Back" button is clicked
                # Add functionality for the "Next" button if needed
                elif next_rect.collidepoint(mouse_pos):
                    run_help = False
                    help_screen_2()




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

        text = font.render("Pontos: " + str(points), True, (255,255,255))
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
            save_score(player_name, points)
            
        current_time = pygame.time.get_ticks()
        if pink_border_active and current_time - pink_border_timer > 10000:  # Check if 10 seconds have passed
            pink_border_active = False  # Deactivate pink border effect
        
        pygame.display.update()
        clock.tick(60)

def save_score(player_name, score):
    with open("scores.txt", "a") as file:
        file.write(player_name + " " + str(score) + "\n")

def load_scores():
    scores = []
    with open("scores.txt", "r") as file:
        for line in file:
            player_name, player_score = line.strip().split()
            scores.append((player_name, int(player_score)))
    return scores

def update_high_score(player_name, score):
    scores = load_scores()
    highest_score = max(scores, key=lambda x: x[1])[1] if scores else 0
    if score > highest_score:
        with open("scores.txt", "w") as file:
            file.write(player_name + " " + str(score) + "\n")

# Example usage:
# save_score("Player1", 100)
# update_high_score("Player1


menu_screen()
