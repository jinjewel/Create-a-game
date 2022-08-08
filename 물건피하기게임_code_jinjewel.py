import pygame
import random

####################################################################
# 무조건 해야되는 것들

pygame.init()

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("똥 피하기")

clock = pygame.time.Clock()

############# 배경 설정  #############################################

background = pygame.image.load("C:/ohcoding/내가 만든 게임/pygame_basic/backgroung.png")

############ 캐릭터 설정 #############################################

character = pygame.image.load("C:/ohcoding/내가 만든 게임/pygame_basic/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height

to_x = 0
to_y = 0
character_speed = 1

############ 적(똥) 설정 #############################################

enemy = pygame.image.load("C:/ohcoding/내가 만든 게임/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0 # 나중에 떨어지는 걸로 수정

enemy_speed = 20

############ 폰트와 시간 정의 ###########################################

game_font = pygame.font.Font(None, 40)

total_time = 30
start_ticks = pygame.time.get_ticks()

############# 키보드 마우스 등 이벤트 처리 #######################################

running = True
while running:

    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed               

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

####### 캐릭터 움직임 정의 ######################################################

    character_x_pos += to_x * dt

    enemy_y_pos += enemy_speed

    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemy_width) 

####### 게임 내 충돌 처리 ######################################################

    if character_x_pos <= 0:
        character_x_pos = 0
    elif character_x_pos >= screen_width - character_width:
        character_x_pos = screen_width - character_width

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(enemy_rect):
        print('충돌했습니다. 종료합니다.')
        running = False

####### 이미지 그리기 ######################################################        

    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (50,50,50))
    screen.blit(timer,(5,5))

    if int(total_time - elapsed_time) <= 0:
        print('Time out')
        running = False



    pygame.display.update()

############ 게임 종료 ##################################################

pygame.time.delay(1000)

pygame.quit()