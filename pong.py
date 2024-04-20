import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 90
BALL_SPEED_X = 7
BALL_SPEED_Y = 7
AI_SPEED = 10
SCORE_FONT = pygame.font.SysFont("comicsans", 40)


# Create objects
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
left_score = 0
right_score = 0

# Draw objects
def draw_objects():
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, left_paddle)
    pygame.draw.rect(WIN, WHITE, right_paddle)
    pygame.draw.ellipse(WIN, WHITE, ball)
    draw_dotted_line()
    draw_score()

# Draw dotted line
def draw_dotted_line():
    dash_length = 6
    gap_length = 4
    num_dashes = HEIGHT // (dash_length + gap_length)

    for i in range(num_dashes):
        y = i * (dash_length + gap_length)
        pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 1, y, 2, dash_length))

# Draw score
def draw_score():
    left_text = SCORE_FONT.render(str(left_score), 1, WHITE)
    right_text = SCORE_FONT.render(str(right_score), 1, WHITE)
    WIN.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    WIN.blit(right_text, (3 * WIDTH // 4 - right_text.get_width() // 2, 20))

# Move paddles
def move_paddles():
    global left_paddle, right_paddle

    # AI movement for left paddle
    if ball_speed_x < 0:
        if random.random() < 0.65:  # 65% chance AI will track the ball
            if left_paddle.centery < ball.centery:
                left_paddle.y += AI_SPEED
            elif left_paddle.centery > ball.centery:
                left_paddle.y -= AI_SPEED

    # AI movement for right paddle
    if ball_speed_x > 0:
        if random.random() < 0.65:  # 65% chance AI will track the ball
            if right_paddle.centery < ball.centery:
                right_paddle.y += AI_SPEED
            elif right_paddle.centery > ball.centery:
                right_paddle.y -= AI_SPEED

# Move ball
def move_ball():
    global ball_speed_x, ball_speed_y, left_score, right_score

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball reset if it goes out of bounds
    if ball.left <= 0:
        right_score += 1
        ball_restart()
    elif ball.right >= WIDTH:
        left_score += 1
        ball_restart()

# Ball reset
def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

# Main game loop
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        move_paddles()
        move_ball()
        draw_objects()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
