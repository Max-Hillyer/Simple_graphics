from simple_graphics import *
import random

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 8
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICKS_COLS = 9
BRICKS_ROWS = 4

paddle = Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40, 
              PADDLE_WIDTH, PADDLE_HEIGHT, color="#00ff00")

ball = Circle(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, BALL_RADIUS, color="#ffff00")

ball_vx = 5
ball_vy = -5
score = 0
lives = 3
game_over = False
won = False

bricks = []
for row in range(BRICKS_ROWS):
    for col in range(BRICKS_COLS):
        x = col * BRICK_WIDTH + 10
        y = row * BRICK_HEIGHT + 30
        brick = Rect(x, y, BRICK_WIDTH - 2, BRICK_HEIGHT - 2, 
                    color="#ff00ff")
        bricks.append(brick)

score_text = None
lives_text = None
game_state_text = None


def reset_ball():
    global ball_vx, ball_vy
    ball.x = SCREEN_WIDTH // 2
    ball.y = SCREEN_HEIGHT - 100
    ball_vx = random.choice([-5, 5])
    ball_vy = -5


def check_collisions():
    global ball_vx, ball_vy, score, lives, game_over, won
    
    if is_colliding(ball, paddle):
        ball_vy = -abs(ball_vy)
        paddle_center = paddle.x + PADDLE_WIDTH // 2
        ball_offset = ball.x - paddle_center
        ball_vx = (ball_offset / (PADDLE_WIDTH // 2)) * 8
    
    if ball.x - BALL_RADIUS < 0 or ball.x + BALL_RADIUS > SCREEN_WIDTH:
        ball_vx = -ball_vx
    
    if ball.y - BALL_RADIUS < 0:
        ball_vy = -ball_vy
    
    if ball.y - BALL_RADIUS > SCREEN_HEIGHT:
        lives -= 1
        if lives <= 0:
            game_over = True
        else:
            reset_ball()
    
    for brick in bricks[:]:
        if is_colliding(ball, brick):
            bricks.remove(brick)
            erase(brick)
            ball_vy = -ball_vy
            score += 10
            break
    
    if len(bricks) == 0:
        won = True


@on_hold("left")
def move_paddle_left():
    if paddle.x > 0:
        paddle.x -= 6


@on_hold("right")
def move_paddle_right():
    if paddle.x + PADDLE_WIDTH < SCREEN_WIDTH:
        paddle.x += 6

@on_tick
def update():
    global ball_vx, ball_vy, score_text, lives_text, game_state_text
    
    if not game_over and not won:
        ball.x += ball_vx
        ball.y += ball_vy
        
        check_collisions()
    
    if score_text:
        erase(score_text)
    if lives_text:
        erase(lives_text)
    if game_state_text:
        erase(game_state_text)
    
    score_text = Text(20, 10, f"Score: {score}", size=20, color="#ffffff")
    lives_text = Text(SCREEN_WIDTH - 120, 10, f"Lives: {lives}", size=20, color="#ffffff")
    
    if game_over:
        game_state_text = Text(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2,
            f"GAME OVER! Final Score: {score}",
            size=24, color="#ff0000"
        )
    elif won:
        game_state_text = Text(
            SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2,
            f"YOU WON! Score: {score}",
            size=24, color="#00ff00"
        )


reset_ball()
set_bg("#0a0a0a")
run(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Block Breaker", resizable=False)
