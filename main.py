import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Bouncing Game")

# Set up the ball
ball_radius = 10
ball_color = (255, 255, 255)
ball_pos = [random.randint(ball_radius, screen_width - ball_radius), random.randint(ball_radius, screen_height - ball_radius)]
ball_speed = [random.randint(2, 6), random.randint(2, 6)]
ball_speed = 4
ball_vel = [-2, -2]

max_bounce_angle = 2


# Set up the explosion
explosion_radius = 50
explosion_color = (255, 0, 0)
explosion_pos = [0, 0]
explosion_timer = 0
dot_radius = 2
dot_color = (255, 255, 255)
dots = []

# Set up the obstacles
obstacle_radius = 20
obstacle_color = (0, 255, 0)
obstacle_pos = [random.randint(obstacle_radius, screen_width - obstacle_radius), random.randint(obstacle_radius, screen_height - obstacle_radius)]

# Set up the bat
bat_width = 50
bat_height = 5
bat_color = (255, 255, 255)
bat_pos = [(screen_width - bat_width) / 2, screen_height - bat_height - 10]
bat_speed = 5

# Set up the game loop
running = True
game_over = False
clock = pygame.time.Clock()


while running and not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # End the game if the ball touches the bottom of the screen
    if ball_pos[1] + ball_radius > screen_height:
        game_over = True
          
    # Move the ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # # Check for collision with the bat
    # if ball_pos[1] + ball_radius >= bat_pos[1] and ball_pos[1] - ball_radius <= bat_pos[1] + bat_height and ball_pos[0] + ball_radius >= bat_pos[0] and ball_pos[0] - ball_radius <= bat_pos[0] + bat_width:
    #     ball_speed[1] = -ball_speed[1]

    # Check for ball-bat collision
    if ball_pos[1] + ball_radius >= bat_pos[1] and ball_pos[1] - ball_radius <= bat_pos[1] + bat_height:
        if ball_pos[0] + ball_radius >= bat_pos[0] and ball_pos[0] - ball_radius <= bat_pos[0] + bat_width:
            # Calculate the angle of the bounce
            bat_center = bat_pos[0] + bat_width / 2
            ball_distance = ball_pos[0] - bat_center
            normalized_distance = ball_distance / (bat_width / 2)
            bounce_angle = normalized_distance * max_bounce_angle

            # Change the ball velocity based on the angle of the bounce
            ball_vel[0] = ball_speed * math.sin(bounce_angle)
            ball_vel[1] = -ball_speed * math.cos(bounce_angle)

    # Move the bat
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bat_pos[0] > 0:
        bat_pos[0] -= bat_speed
    if keys[pygame.K_RIGHT] and bat_pos[0] + bat_width < screen_width:
        bat_pos[0] += bat_speed

    # Check for collision with obstacles
    distance = ((ball_pos[0] - obstacle_pos[0])**2 + (ball_pos[1] - obstacle_pos[1])**2)**0.5
    if distance <= ball_radius + obstacle_radius:
        explosion_pos = obstacle_pos
        explosion_timer = 30
        for i in range(50):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            dots.append({'pos': list(explosion_pos), 'vel': [speed * math.cos(angle), speed * math.sin(angle)]})
        obstacle_pos = [random.randint(obstacle_radius, screen_width - obstacle_radius), random.randint(obstacle_radius, screen_height - obstacle_radius)]

    # Update the dots in the explosion
    for dot in dots:
        dot['pos'][0] += dot['vel'][0]
        dot['pos'][1] += dot['vel'][1]
        dot['vel'][1] += 0.2

    # Check for collision with screen edges
    if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > screen_width:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > screen_height:
        ball_vel[1] = -ball_vel[1]

    # Draw the screen
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.draw.circle(screen, obstacle_color, (int(obstacle_pos[0]), int(obstacle_pos[1])), obstacle_radius)

    # Draw the bat
    pygame.draw.rect(screen, bat_color, (int(bat_pos[0]), int(bat_pos[1]), bat_width, bat_height))


    # Draw the explosion dots
    for dot in dots:
        pygame.draw.circle(screen, dot_color, (int(dot['pos'][0]), int(dot['pos'][1])), dot_radius)

    # Update and clear the dots in the explosion
    if explosion_timer > 0:
        explosion_timer -= 1
    else:
        dots = []
    
    # Draw the explosion
    if explosion_timer > 0:
        pygame.draw.circle(screen, explosion_color, (int(explosion_pos[0]), int(explosion_pos[1])), explosion_radius - int(explosion_timer * explosion_radius / 30))
    
    pygame.display.flip()
    
    # Wait for the next frame
    clock.tick(60)
pygame.quit()