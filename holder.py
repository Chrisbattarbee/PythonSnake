prevState = 'left'
state = 'right'

speed = [0,0]

black = 0,0,0

screen = pygame.display.set_mode(size)

ball = pygame.image.load('Resources/square_white_24_ns.bmp')
ballrect = ball.get_rect()

gameTick = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #Handling key presses
        if event.type == pygame.KEYDOWN:
            prevState = state
            if event.key == pygame.K_w:
                state = 'up';
            if event.key == pygame.K_s:
                state = 'down'
            if event.key == pygame.K_a:
                state = 'left'
            if event.key == pygame.K_d:
                state = 'right'

    # Handles speed logic
    speed = SetSpeed(state, gameTick, speed, prevState)

    ballrect = ballrect.move(speed)

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()

    gameTick += 1