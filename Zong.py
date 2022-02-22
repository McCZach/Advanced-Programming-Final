'''
Created on May 1, 2018

@author: 21zacharymccolgan
'''

import sys, time, random, math, pygame
from pygame.locals import *
from MyLib_Blocks import *
from pygame.cursors import ball
from test.test_xmlrpc import BaseKeepaliveServerTestCase

def title():
    pygame.mixer.music.load('Contra.mp3') #IF YOU DO NOT KNOW THE CONTRA JUNGLE THEME, GOOGLE IT
    pygame.mixer.music.play(-1)  
    font2 = pygame.font.Font(None,48) #Used for the players
    font3 = pygame.font.Font(None,44) #Used/Custom for long text; how to launch ball
    font4 = pygame.font.Font(None,52) #Used to say how to begin
    font5 = pygame.font.Font(None,70)
    red = (204,0,0)
    orange = (204,102,0)
    yellow = (204,204,0)
    green = (0,204,0)
    blue = (0,0,204)
    print_text(font2,0,0,"Player 1 (Left): Use Keys 'W' and 'S'.", red)
    print_text(font2,0,75,"Player 2 (Right): Use Arrow Keys 'Up' and 'Down'.", blue)
    print_text(font4,0,185,"Press 'R' to reset.", orange)
    print_text(font3,0,255,"Press 'ENTER' to launch the ball, and after one scores.", orange)
    print_text(font5,0,400,"Left Click to Begin!")

def draw_box():
    pos_x1 = 400 #This method is long and boring
    pos_y1 = 25
    pos_x2 = 400
    pos_y2 = 75
    pos_x3 = 400
    pos_y3 = 125
    pos_x4 = 400
    pos_y4 = 175
    pos_x5 = 400
    pos_y5 = 225
    pos_x6 = 400
    pos_y6 = 275
    pos_x7 = 400
    pos_y7 = 325
    pos_x8 = 400
    pos_y8 = 375
    pos_x9 = 400
    pos_y9 = 425
    pos_x10 = 400
    pos_y10 = 475
    pos_x11 = 400
    pos_y11 = 525
    width = 0
    gray = (192,192,192)
    pos1 = pos_x1, pos_y1, 20, 20
    pygame.draw.rect(screen,gray,pos1,width)
    pos2 = pos_x2, pos_y2, 20, 20
    pygame.draw.rect(screen,gray,pos2,width)
    pos3 = pos_x3, pos_y3, 20, 20
    pygame.draw.rect(screen,gray,pos3,width)
    pos4 = pos_x4, pos_y4, 20, 20
    pygame.draw.rect(screen,gray,pos4,width)
    pos5 = pos_x5, pos_y5, 20, 20
    pygame.draw.rect(screen,gray,pos5,width)
    pos6 = pos_x6, pos_y6, 20, 20
    pygame.draw.rect(screen,gray,pos6,width)
    pos7 = pos_x7, pos_y7, 20, 20
    pygame.draw.rect(screen,gray,pos7,width)
    pos8 = pos_x8, pos_y8, 20, 20
    pygame.draw.rect(screen,gray,pos8,width)
    pos9 = pos_x9, pos_y9, 20, 20
    pygame.draw.rect(screen,gray,pos9,width)
    pos10 = pos_x10, pos_y10, 20, 20
    pygame.draw.rect(screen,gray,pos10,width)
    pos11 = pos_x11, pos_y11, 20, 20
    pygame.draw.rect(screen,gray,pos11,width)
    print_text(font,200,0,str(paddle1_score))
    print_text(font,600,0,str(paddle2_score))

def print_text(font,x,y,text,color=(255,255,255)):
    imgText = font.render(text,True,color)
    screen.blit(imgText, (x,y))
    
def audio_init():
        global collision_sound, collision2_sound, wall_sound
        #initialize the audio mixer
        pygame.mixer.init() #There are 3 sounds even if the title doesn't work, there are subtle differences between the two paddle collision sounds the wall is completely different too.
        #load sound files
        collision_sound = pygame.mixer.Sound("Paddle_collision16.wav")
        collision2_sound = pygame.mixer.Sound("Paddle2_collision.wav")
        wall_sound = pygame.mixer.Sound("wall_collision.wav")
        
def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)

#this function initializes the game
def game_init():
    #global variables can be accessed/used by all methods
    global screen, font, timer
    global paddle_group, paddle2_group, ball_group
    global paddle, paddle2, ball
    
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Zong")
    font = pygame.font.Font(None, 100)
    pygame.mouse.set_visible(False)
    timer = pygame.time.Clock()
    
    #create sprite groups
    paddle_group = pygame.sprite.Group()
    paddle2_group = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()
    
    paddle = MySprite()
    paddle.load("pong_player.png")
    paddle.position = 25,300
    paddle_group.add(paddle)
    
    paddle2 = MySprite()
    paddle2.load("pong_player.png")
    paddle2.position = 750,300
    paddle2_group.add(paddle2)
    
    ball = MySprite()
    ball.load("ball.png")
    ball.position = 400,300
    ball_group.add(ball)
    
#this function moves the paddle1
def move_paddle1():
    global movex,movey,keys,waiting
    
    paddle_group.update(ticks, 50)
    
    if keys[K_w]: 
        paddle.velocity.y = -8.0
    elif keys[K_s]: 
        paddle.velocity.y = 8.0
        
    paddle.Y += paddle.velocity.y
    if paddle.Y < 0: paddle.Y = 0
    elif paddle.Y > 550: paddle.Y = 550
    
def move_paddle2():
    global movex,movey,keys,waiting
    
    paddle2_group.update(ticks, 50)
    
    if keys[K_UP]:
        paddle2.velocity.y = -8.0
    elif keys[K_DOWN]:
        paddle2.velocity.y = 8.0
    
    paddle2.Y += paddle2.velocity.y
    if paddle2.Y < 0: paddle2.Y = 0
    elif paddle2.Y > 550: paddle2.Y = 550
    
#this function resets the ball's velocity
def reset_ball():
    x = random.choice([-5,5])
    y = random.choice([-6,-5,-4,-3,3,4,5,6])
    ball.velocity = Point(x,y)
    
#this function moves the ball
def move_ball():
    global waiting, ball, game_over, lives, paddle1_score, paddle2_score
    #move the ball
    ball_group.update(ticks, 50)
    
    print_text(font,200,0,str(paddle1_score))
    print_text(font,600,0,str(paddle2_score))
    
    if waiting:
        ball.X = 400
        ball.Y = 300
    ball.X += ball.velocity.x
    ball.Y += ball.velocity.y
    if ball.X < 0: #Goes past left side of screen
        paddle2_score += 1
        paddle.position = 25,300
        paddle2.position = 750,300
        ball.X = 0
        waiting = True
    elif ball.X > 775: #Goes past right side of screen
        paddle1_score += 1
        paddle.position = 25,300
        paddle2.position = 750,300
        ball.X = 775
        waiting = True
    if ball.Y < 0:  #The "Y" controls bounces, up and down
        play_sound(wall_sound)
        ball.Y = 0
        ball.velocity.y *= -1
    elif ball.Y > 575: #The "Y" controls bounces, up and down
        play_sound(wall_sound)
        ball.Y = 575
        ball.velocity.y *= -1

def collision_ball_paddle():
    if pygame.sprite.collide_rect(ball, paddle):
        ball.velocity.y = -abs(ball.velocity.y)
        play_sound(collision_sound)
        bx = ball.X + 8
        by = ball.Y + 8
        px = paddle.X + paddle.frame_width/2
        py = paddle.Y + paddle.frame_height/2
        if bx < px: #left side of paddle?
            ball.velocity.x = -abs(ball.velocity.x)
        else: #right side of paddle?
            ball.velocity.x = abs(ball.velocity.x)
            
def collision_ball_paddle2():
    if pygame.sprite.collide_rect(ball, paddle2):
        ball.velocity.y = -abs(ball.velocity.y)
        play_sound(collision2_sound)
        bx = ball.X + 8
        by = ball.Y + 8
        px2 = paddle2.X + paddle2.frame_width/2
        py2 = paddle2.Y + paddle2.frame_height/2
        if bx < px2: #left side of paddle?
            ball.velocity.x = -abs(ball.velocity.x)
        else: #right side of paddle?
            ball.velocity.x = abs(ball.velocity.x)

#main program begins
game_init()
audio_init()
black = (0,0,0)
white = (255,255,255)
playing = False
game_over = True
restart = False
waiting = True
level = 0
paddle1_score = 0
paddle2_score = 0

#repeating loop
while True: #Changed from 'True'
    timer.tick(30)
    ticks = pygame.time.get_ticks()
    
    #hand events
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            game_over = False   
            playing = True
        elif event.type == KEYUP:
            if waiting and playing:
                if event.key == K_RETURN:
                    waiting = False
                    reset_ball()
            if not game_over and playing:
                if event.key == K_r: restart = True
            if event.key == K_w: paddle.velocity.y = 0.0
            if event.key == K_s: paddle.velocity.y = 0.0
            if event.key == K_UP: paddle2.velocity.y = 0.0
            if event.key == K_DOWN: paddle2.velocity.y = 0.0
            
    #handle key presses
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    
    #do updates
    if not game_over and playing:
        pygame.mixer.music.stop()
        move_paddle1()
        move_paddle2()
        move_ball()
        collision_ball_paddle()
        collision_ball_paddle2()
        screen.fill((black))
        draw_box()
        paddle_group.draw(screen)
        paddle2_group.draw(screen)
        ball_group.draw(screen)
        
    if game_over and not playing:
        title()
    
    if restart:
        game_init()
        audio_init()
        black = (0,0,0)
        white = (255,255,255)
        game_over = False
        restart = False
        waiting = True
        level = 0
        paddle1_score = 0
        paddle2_score = 0
        draw_box()
        
    pygame.display.update()
