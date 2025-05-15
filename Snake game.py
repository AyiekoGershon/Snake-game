import pygame
import time
import random
import json
import os

pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)
purple = (128, 0, 128)
lightgreen = (144, 238, 144)  

# Display settings
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Mufasa Snake Game')

# Game settings
snake_block = 20
initial_speed = 10
clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# High score file
high_score_file = "snake_highscore.json"

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as f:
            try:
                data = json.load(f)
                return data.get('high_score', 0)
            except:
                return 0
    return 0

def save_high_score(score):
    with open(high_score_file, 'w') as f:
        json.dump({'high_score': score}, f)

def draw_walls():
    # Draw border walls
    pygame.draw.rect(dis, blue, [0, 0, dis_width, snake_block])
    pygame.draw.rect(dis, blue, [0, dis_height - snake_block, dis_width, snake_block])
    pygame.draw.rect(dis, blue, [0, 0, snake_block, dis_height])
    pygame.draw.rect(dis, blue, [dis_width - snake_block, 0, snake_block, dis_height])
    
    # Draw some random obstacles
    obstacles = [
        [200, 200, snake_block*3, snake_block],
        [400, 400, snake_block, snake_block*2],
        [100, 500, snake_block*4, snake_block],
        [600, 100, snake_block, snake_block*3]
    ]
    
    for obstacle in obstacles:
        pygame.draw.rect(dis, blue, obstacle)
    
    return obstacles

def generate_food(snake_list, obstacles):
    food_types = [
        {'color': red, 'score': 1, 'effect': 'normal'},
        {'color': yellow, 'score': 3, 'effect': 'speed_boost'},
        {'color': purple, 'score': 5, 'effect': 'slow_down'}
    ]
    
    while True:
        food_type = random.choice(food_types)
        foodx = round(random.randrange(snake_block, dis_width - snake_block*2) / snake_block) * snake_block
        foody = round(random.randrange(snake_block, dis_height - snake_block*2) / snake_block) * snake_block
        
        # Check if food spawns on snake or obstacle
        valid_position = True
        
        # Check snake collision
        for block in snake_list:
            if block[0] == foodx and block[1] == foody:
                valid_position = False
                break
        
        # Check obstacle collision
        for obstacle in obstacles:
            if (obstacle[0] <= foodx < obstacle[0] + obstacle[2] and 
                obstacle[1] <= foody < obstacle[1] + obstacle[3]):
                valid_position = False
                break
        
        if valid_position:
            return {'x': foodx, 'y': foody, 'type': food_type}

def your_score(score, high_score):
    value = score_font.render(f"Score: {score} | High Score: {high_score}", True, black)
    dis.blit(value, [10, 10])

def our_snake(snake_block, snake_list):
    lightgreen = (144, 238, 144)  # Define the light green color
    for i, x in enumerate(snake_list):
        # Use ternary operator to choose color
        color = green if i == 0 else lightgreen
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block], 1)  # Optional: add border

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False
    
    high_score = load_high_score()
    
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    
    snake_List = []
    Length_of_snake = 1
    
    obstacles = draw_walls()
    food = generate_food(snake_List, obstacles)
    current_speed = initial_speed
    speed_boost_end = 0
    
    while not game_over:
        while game_close:
            dis.fill(white)
            message("Game Over! Press Q-Quit or C-Play Again", red)
            your_score(Length_of_snake - 1, high_score)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change <= 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change >= 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change <= 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change >= 0:
                    y1_change = snake_block
                    x1_change = 0
        
        # Check wall collision
        if (x1 >= dis_width - snake_block or x1 < snake_block or 
            y1 >= dis_height - snake_block or y1 < snake_block):
            game_close = True
        
        # Check obstacle collision
        for obstacle in obstacles:
            if (obstacle[0] <= x1 < obstacle[0] + obstacle[2] and 
                obstacle[1] <= y1 < obstacle[1] + obstacle[3]):
                game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        
        # Draw walls and obstacles
        obstacles = draw_walls()
        
        # Draw food
        pygame.draw.rect(dis, food['type']['color'], [food['x'], food['y'], snake_block, snake_block])
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        
        # Check self collision
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1, high_score)
        
        pygame.display.update()
        
        # Check food collision
        if x1 == food['x'] and y1 == food['y']:
            # Apply food effect
            if food['type']['effect'] == 'speed_boost':
                current_speed += 5
                speed_boost_end = time.time() + 10  # Boost lasts 10 seconds
            elif food['type']['effect'] == 'slow_down':
                current_speed = max(5, current_speed - 3)
            
            Length_of_snake += food['type']['score']
            food = generate_food(snake_List, obstacles)
            
            # Increase difficulty every 5 points
            if (Length_of_snake - 1) % 5 == 0:
                current_speed += 1
            
            # Update high score
            if Length_of_snake - 1 > high_score:
                high_score = Length_of_snake - 1
                save_high_score(high_score)
        
        # Check if speed boost expired
        if speed_boost_end and time.time() > speed_boost_end:
            current_speed = initial_speed + ((Length_of_snake - 1) // 5)
            speed_boost_end = 0
        
        clock.tick(current_speed)
    
    pygame.quit()
    quit()

gameLoop()
