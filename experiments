###################
# By @PATELOM925 
###################

import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Square")

# Colors
LIGHT_THEME = {
    "background": (255, 255, 255),
    "square": (0, 0, 0),
    "ball": (255, 255, 0),
    "button": (200, 200, 200),
    "button_shadow": (150, 150, 150),
    "text": (0, 0, 0),
    "toggle_on": (0, 255, 0),
    "toggle_off": (255, 0, 0),
}

DARK_THEME = {
    "background": (30, 30, 30),
    "square": (255, 255, 255),
    "ball": (255, 255, 0),
    "button": (100, 100, 100),
    "button_shadow": (50, 50, 50),
    "text": (255, 255, 255),
    "toggle_on": (0, 200, 0),
    "toggle_off": (200, 0, 0),
}

current_theme = LIGHT_THEME

# Square properties
square_size = 300
square_angle = 0  # Rotation angle of the square
square_rotation_speed = 0.5  # Degrees per frame
square_thickness = 3  # Initial thickness of the square boundary

# Ball properties
ball_radius = 15
ball_color = current_theme["ball"]
ball_velocity = [3, 4]  # Velocity in x and y directions (local coordinates)

# Button properties
button_font = pygame.font.SysFont("Arial", 20)
button_width = 85
button_height = 20
button_gap = 10

# Dual-part buttons
ball_speed_button = pygame.Rect(10, 10, button_width, 2 * button_height + button_gap)
square_length_button = pygame.Rect(130, 10, button_width, 2 * button_height + button_gap)
square_thickness_button = pygame.Rect(250, 10, button_width, 2 * button_height + button_gap)
ball_size_button = pygame.Rect(370, 10, button_width, 2 * button_height + button_gap)

# Toggle theme button
toggle_theme_button = pygame.Rect(490, 10, button_width, button_height)

# Change ball color button
change_color_button = pygame.Rect(610, 10, button_width, button_height)

# Stop button
stop_button = pygame.Rect(10, 120, button_width, button_height)
is_running = True  # Simulation state

def rotate_point(point, angle):
    """Rotate a point around the origin by a given angle."""
    angle_rad = math.radians(angle)
    x, y = point
    x_new = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    y_new = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return [x_new, y_new]

def draw_rotated_square(angle):
    """Draw a square rotated by a given angle."""
    half_size = square_size // 2
    center = (WIDTH // 2, HEIGHT // 2)
    corners = [
        [-half_size, -half_size],
        [half_size, -half_size],
        [half_size, half_size],
        [-half_size, half_size],
    ]
    rotated_corners = [rotate_point(corner, angle) for corner in corners]
    screen_corners = [[center[0] + x, center[1] + y] for [x, y] in rotated_corners]
    pygame.draw.polygon(screen, current_theme["square"], screen_corners, square_thickness)

def check_collision(ball_local_pos):
    """Check if the ball collides with the square's edges and adjust its velocity."""
    half_size = square_size // 2

    # Check collisions with the unrotated square
    if ball_local_pos[0] - ball_radius < -half_size:
        ball_local_pos[0] = -half_size + ball_radius  # Correct position
        ball_velocity[0] = abs(ball_velocity[0])  # Bounce right
    elif ball_local_pos[0] + ball_radius > half_size:
        ball_local_pos[0] = half_size - ball_radius  # Correct position
        ball_velocity[0] = -abs(ball_velocity[0])  # Bounce left
    if ball_local_pos[1] - ball_radius < -half_size:
        ball_local_pos[1] = -half_size + ball_radius  # Correct position
        ball_velocity[1] = abs(ball_velocity[1])  # Bounce down
    elif ball_local_pos[1] + ball_radius > half_size:
        ball_local_pos[1] = half_size - ball_radius  # Correct position
        ball_velocity[1] = -abs(ball_velocity[1])  # Bounce up

def update_ball(ball_local_pos):
    """Update the ball's position and handle collisions."""
    if is_running:
        ball_local_pos[0] += ball_velocity[0]
        ball_local_pos[1] += ball_velocity[1]
        check_collision(ball_local_pos)

def draw_ball(ball_local_pos, angle):
    """Draw the ball on the screen."""
    center = (WIDTH // 2, HEIGHT // 2)
    ball_screen_pos = rotate_point(ball_local_pos, -angle)
    ball_screen_pos = [center[0] + ball_screen_pos[0], center[1] + ball_screen_pos[1]]
    pygame.draw.circle(screen, ball_color, (int(ball_screen_pos[0]), int(ball_screen_pos[1])), ball_radius)

def draw_dual_part_button(rect, label):
    """Draw a dual-part button with a shadow and centered text."""
    # Draw the button background
    pygame.draw.rect(screen, current_theme["button"], rect)

    # Draw the shadow line
    shadow_y = rect.y + button_height
    pygame.draw.line(screen, current_theme["button_shadow"], (rect.x, shadow_y), (rect.x + rect.width, shadow_y), 2)

    # Draw the increment and decrement labels
    increment_text = button_font.render(f"{label} +", True, current_theme["text"])
    decrement_text = button_font.render(f"{label} -", True, current_theme["text"])

    # Center the text
    increment_rect = increment_text.get_rect(center=(rect.x + rect.width // 2, rect.y + button_height // 2))
    decrement_rect = decrement_text.get_rect(center=(rect.x + rect.width // 2, rect.y + button_height + button_height // 2))

    screen.blit(increment_text, increment_rect)
    screen.blit(decrement_text, decrement_rect)

def draw_toggle_button(rect, is_dark):
    """Draw a toggle button with a slider-like appearance."""
    # Draw the button background
    pygame.draw.rect(screen, current_theme["button"], rect)

    # Draw the toggle slider
    slider_width = rect.width // 2
    slider_x = rect.x + (slider_width if is_dark else 0)
    slider_color = current_theme["toggle_on"] if is_dark else current_theme["toggle_off"]
    pygame.draw.rect(screen, slider_color, (slider_x, rect.y, slider_width, rect.height))

    # Draw the toggle label
    label = "Dark" if is_dark else "Light"
    label_text = button_font.render(label, True, current_theme["text"])
    label_rect = label_text.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
    screen.blit(label_text, label_rect)

def draw_stop_button(rect):
    """Draw the stop/start button."""
    pygame.draw.rect(screen, current_theme["button"], rect)
    label = "Stop" if is_running else "Start"
    label_text = button_font.render(label, True, current_theme["text"])
    label_rect = label_text.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
    screen.blit(label_text, label_rect)

def draw_buttons():
    """Draw all buttons on the screen."""
    # Dual-part buttons
    draw_dual_part_button(ball_speed_button, "Speed")
    draw_dual_part_button(square_length_button, "Length")
    draw_dual_part_button(square_thickness_button, "Thick")
    draw_dual_part_button(ball_size_button, "Size")

    # Toggle theme button
    draw_toggle_button(toggle_theme_button, current_theme == DARK_THEME)

    # Change ball color button
    pygame.draw.rect(screen, current_theme["button"], change_color_button)
    color_text = button_font.render("Color", True, current_theme["text"])
    color_rect = color_text.get_rect(center=(change_color_button.x + change_color_button.width // 2, change_color_button.y + change_color_button.height // 2))
    screen.blit(color_text, color_rect)

    # Stop button
    draw_stop_button(stop_button)

def handle_buttons(mouse_pos):
    """Handle button clicks to adjust properties."""
    global ball_velocity, square_size, square_thickness, ball_radius, current_theme, ball_color, is_running

    # Ball speed
    if ball_speed_button.collidepoint(mouse_pos):
        if mouse_pos[1] < ball_speed_button.y + button_height:
            ball_velocity[0] *= 1.1
            ball_velocity[1] *= 1.1
        else:
            ball_velocity[0] *= 0.9
            ball_velocity[1] *= 0.9

    # Square length
    if square_length_button.collidepoint(mouse_pos):
        if mouse_pos[1] < square_length_button.y + button_height:
            square_size += 20
        else:
            square_size -= 20
            if square_size < 100:
                square_size = 100

    # Square thickness
    if square_thickness_button.collidepoint(mouse_pos):
        if mouse_pos[1] < square_thickness_button.y + button_height:
            square_thickness += 1
        else:
            square_thickness -= 1
            if square_thickness < 1:
                square_thickness = 1

    # Ball size
    if ball_size_button.collidepoint(mouse_pos):
        if mouse_pos[1] < ball_size_button.y + button_height:
            ball_radius += 2
        else:
            ball_radius -= 2
            if ball_radius < 5:
                ball_radius = 5

    # Toggle theme
    if toggle_theme_button.collidepoint(mouse_pos):
        current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
        ball_color = current_theme["ball"]

    # Change ball color
    if change_color_button.collidepoint(mouse_pos):
        ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Stop/Start simulation
    if stop_button.collidepoint(mouse_pos):
        is_running = not is_running

# Main loop
clock = pygame.time.Clock()
running = True
ball_local_pos = [0, 0]  # Ball's position in local coordinates
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_buttons(pygame.mouse.get_pos())

    # Clear the screen
    screen.fill(current_theme["background"])

    # Draw the rotated square
    draw_rotated_square(square_angle)

    # Update and draw the ball
    update_ball(ball_local_pos)
    draw_ball(ball_local_pos, square_angle)

    # Draw buttons
    draw_buttons()

    # Update the square's rotation angle
    if is_running:
        square_angle = (square_angle + square_rotation_speed) % 360

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()