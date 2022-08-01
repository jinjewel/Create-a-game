import os
import pygame

####################################################

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("jingame2")

clock = pygame.time.Clock()
######################################################

# 사용자 게임 초기화

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

# 배경만들기

background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 놓기 위해

# 캐릭터 만들기

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width /2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향

character_to_x = 0

# 캐릭터 이동 속도

character_speed = 10

# 무기 만들기

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능

weapons = []

# 무기 이동 속도

weapon_speed = 5

# 공만들기 (4개 크기 따로 처리)

ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# 공 크기에 따른 최초의 속도

ball_speed_y = [-18, -15, -12, -9]

# 공들

balls = []

# 최초 발생하는 큰 공 추가

balls.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3, # x축 이동방향 -3이면 왼쪽으로 3이면 오른쪽으로
    "to_y" : -6, # y축 이동방향
    "init_spd_y" : ball_speed_y[0] }) # y의 최초 속도 
    
# 사라질 무기, 공 저장 변수

weapon_to_remove = -1
ball_to_remove = -1

# Font 정의

game_font = pygame.font.Font(None, 40)

# 시간 정의

total_time = 100
start_time = pygame.time.get_ticks() 

# 게임 종료 메세지

game_result = "Game Dver"

running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정

# 2. 이벤트 처리 (키보드, 마우스 등)

    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)   
                weapon_y_pos = character_y_pos    
                weapons.append([weapon_x_pos, weapon_y_pos]) 

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = (screen_width - character_width)

    # 무기 위치 조정

    weapons = [ [w[0], w[1]-weapon_speed] for w in weapons ]

    # 천장에 닿은 무기 없애기

    weapons = [ [w[0], w[1]] for w in weapons if w[1]>0 ]

    # 공 위치 정의

    for ball_idx, ball_val in enumerate(balls):
        ball_x_pos = ball_val["pos_x"]
        ball_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로 벽에 닿았을때 반대쪽으로 위치 변경

        if ball_x_pos < 0 or ball_x_pos > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로, 바닥에 닿았을때 위치및 속도 변경

        if ball_y_pos >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5   

        ball_val["pos_x"] += ball_val["to_x"]    
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 이미지 간의 충돌 처리

    # 캐릭터 rect정보 가져오기

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 처리

        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 무기와 공의 충돌 처리

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # 가장 작은 공이 아니라면 다음 단계 공으로 나눠주기

                if ball_img_idx < 3:
                    
                    # 현재 공 크기 정보를 가지고 옴

                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나누어진 공 정보
                    
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    
                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx+1,
                        "to_x" : -3, # x축 이동방향 -3이면 왼쪽으로 3이면 오른쪽으로  
                        "to_y" : -6, # y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] }) # y의 최초 속도 

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width/2) - (small_ball_width/2),
                        "pos_y" : ball_pos_y + (ball_height/2) - (small_ball_height/2),
                        "img_idx" : ball_img_idx+1,
                        "to_x" : 3, # x축 이동방향 -3이면 왼쪽으로 3이면 오른쪽으로
                        "to_y" : -6, # y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] }) # y의 최초 속도 

                break # 2중 for 문에서 첫 번째 for 문 벗어나기
        else: 
            continue
        break # 2중 for 문에서 두 번째 for 문 벗어나기

    # 충돌된 공 또는 무기 없애기
                
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료

    if len(balls) == 0:
        game_result = "Mession Complete "  
        running = False 


    # 5. 화면에 이미지 그리기
    
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계신

    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer,(10,10))

    # 만약 시간이 초과 했다면

    if int(total_time - elapsed_time) <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update() # 게임화면 다시 그리기
 
# 게임 오버 메세지 
msg = game_font.render(game_result, True, (255,255,0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 게임 종료 딜레이

pygame.time.delay(2000)

pygame.quit()
