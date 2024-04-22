#
# Playable pong
#

import pygame
from random import choice, randint


def main():
    # screen specs
    screenWidth = 1000
    screenHeight = 500
    black = [0, 0, 0]
    white = [randint(100, 255), randint(100, 255), randint(100, 255)]  # Screen is 1000x500 with a black background.
    # Time delay on animation set to 10ms
    timeDelay = 4
    leftBound = 0
    highBound = 0
    ballSpeed = 2

    # ball thingz
    startPositionX = 500
    startPositionY = 250
    ballSpeedX = choice([-ballSpeed, ballSpeed])  # ball starts in the middle of the screen
    ballSpeedY = choice([-ballSpeed, ballSpeed])
    ballHeight = 7
    ballThickness = 0

    # paddle thingz
    paddleWidth = 10
    paddleHeight = 60
    opponentX = 912  # opponent position
    opponentY = 220
    playerX = 88
    playerY = 220
    paddleSpeed = 1.5

    pygame.init()
    screen = pygame.display.set_mode([screenWidth, screenHeight])
    pygame.font.init()
    font = pygame.font.Font(None, 74)

    pygame.draw.circle(screen, white, (startPositionX, startPositionY), ballHeight, ballThickness)

    start_screen(screen, font, white)

    play_again = True
    while play_again:
        running = True
        white = [randint(0, 255), randint(0, 255), randint(0, 255)]
        startPositionX = 500
        startPositionY = 250
        ballSpeedX = choice([-ballSpeed, ballSpeed])  # ball starts in the middle of the screen
        ballSpeedY = choice([-ballSpeed, ballSpeed])
        opponentX = 912  # opponent position
        opponentY = 220
        playerX = 88
        playerY = 220
        while running:
            if startPositionX >= screenWidth or startPositionX <= leftBound:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    play_again = False
                    exit()
            screen.fill(black)
            pygame.time.delay(timeDelay)

            # ball animation setup
            pygame.draw.circle(screen, white, (startPositionX, startPositionY), ballHeight)
            startPositionX += ballSpeedX
            startPositionY += ballSpeedY
            ballSpeedY = ballMovementAdjustment(startPositionY, ballHeight, screenHeight,
                                                highBound, ballSpeedY)
            # ball interaction with paddles
            if playerX <= startPositionX - ballHeight <= (playerX + paddleWidth) \
                    and playerY <= startPositionY <= (playerY + paddleHeight):
                ballSpeedX *= -1
            if opponentX <= startPositionX + ballHeight <= opponentX + paddleWidth \
                    and opponentY <= startPositionY <= (opponentY + paddleHeight):
                ballSpeedX *= -1

            # opponent paddle animation and controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:  # move player down
                opponentY += paddleSpeed
            if keys[pygame.K_UP]:  # move player up
                opponentY -= paddleSpeed
            paddleSetUp(screen, white, paddleWidth, paddleHeight, opponentX, opponentY)
            # paddleX, paddleY, rectangleWidth, rectangleHeight, ballX, ballY, radius, ballSpeedX

            # player paddle animation and controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:  # move player up
                playerY -= paddleSpeed
            if keys[pygame.K_s]:  # move player down
                playerY += paddleSpeed
            paddleSetUp(screen, white, paddleWidth, paddleHeight, playerX, playerY)

            font = pygame.font.Font(None, 74)
            text = font.render("PONG", 1, white)
            screen.blit(text, (420, 20))

            pygame.display.update()
            pygame.display.flip()
        if not play_again:
            break


        font = pygame.font.Font(None, 74)


        if startPositionX <= leftBound:
            text_with_line_break = "Player 2 Wins!\n  Play Again?"
            text_line = text_with_line_break.split('\n')
            text = [font.render(line, True, white) for line in text_line]
            y_pos = 200
            for line in text:
                screen.blit(line, (300, y_pos))
                y_pos += line.get_height()
        elif startPositionX >= screenWidth:
            text_with_line_break = "Player 1 Wins!\n  Play Again?"
            text_line = text_with_line_break.split('\n')
            text = [font.render(line, True, white) for line in text_line]
            y_pos = 200
            for line in text:
                screen.blit(line, (300, y_pos))
                y_pos += line.get_height()
        pygame.display.flip()

        while not running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.WINDOWCLOSE and event.gain == 0):
                    running = False
                    play_again = False
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        play_again = True
                        running = True

        pygame.display.update()





# This func makes the ball bounce around the screen. 90 degree bounces only
# @param- x or y directional movement, ball radius, high bound, low bound, ball speed
# @return- updated ball speed
def ballMovementAdjustment(direction, radius, upper_border, lower_border, speed):
    if direction - radius <= lower_border or direction + radius >= upper_border:
        speed *= -1
    if direction <= 0:
        speed *= -1
    return speed


# This function draws both the player 1 and 2's paddles
# @param- screen, color, rectWidth, height, x-position, y-position
# @return- paddle drawing
def paddleSetUp(screen, color, paddleWidth, paddleHeight, paddleX, paddleY):
    paddle = pygame.draw.rect(screen, color, (paddleX, paddleY, paddleWidth, paddleHeight))
    return paddle


def paddleMovement(paddleY, paddleSpeed):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        paddleY += paddleSpeed
        return paddleY
    if keys[pygame.K_UP]:
        paddleY -= paddleSpeed
        return paddleY


def start_screen(screen, font, white):
    screen.fill((0, 0, 0))  # Fill the screen with black
    title_text = font.render("PONG", True, white)
    instruction_text = font.render("Press SPACE to start", True, white)
    
    # Display the title and instructions
    screen.blit(title_text, (450 - title_text.get_width() // 2, 150))
    screen.blit(instruction_text, (460 - instruction_text.get_width() // 2, 250))
    
    pygame.display.flip()

    # Wait for the user to press SPACE
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.type==pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


if __name__ == "__main__":
    main()
