import pygame
import random
import Resource.AnimationCreator as ANIM
import GameManager

playButton = pygame.image.load('Resource/playButton.png')

###### TYPES ##################

#struct Enemy{
# posX, posY
# animation (start | mid | end)
# timing [ ENTRANCE | END ] -> state length
# start_time_tamp
# current_state : 0 start | 1 mid | 2 end | 3 die | 4: DELETED
#}
#Enemy = namedtuple("Enemy", "positionX positionY animation timing start_time current_state")

class Enemy:
    def __init__(self, ppositionX, ppositionY, panimation, ptiming, pstart_time, pcurrent_state, pradius):
        self.positionX = ppositionX
        self.positionY = ppositionY
        self.animation = panimation
        self.timing = ptiming
        self.start_time = pstart_time
        self.current_state = pcurrent_state
        self.radius= pradius
        
    positionX = 0
    positionY = 0 
    animation = 0
    timing = 0
    start_time = 0
    current_state = 0
    radius = 0


##########################################################



class AttackAnimation:
    def __init__(self, pposition, panimation, pstart_time, pduration):
        self.position = pposition
        self.animation = panimation
        self.start_time = pstart_time
        self.duration = pduration
    position = 0   # (posX, posY)
    animation = 0  # animation to render
    start_time = 0 # start time (timestamp)
    duration = 0   # animation duration

m_enemy_list = []
m_attack_animation_list = []


###### CONSTANT ##############

base_time_stamp = 0

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

SHOW_HIT_ATTACK_COUNT = True
TIME_FROM_LAST_MONSTER_SPAWN_TO_END_GAME = 5000 #ms

###### MISC ###################

background = pygame.transform.scale(pygame.image.load('Resource/back.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)) 


###### VARIABLES ##############

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

game_state = 0
# 0: PREGAME 
# 1: PLAYING
# 2: ENDGAME
##############################

spawned_enemy = 0
finish_spawn = False
finish_time_stamp = 0

def initGame():    
    pygame.display.set_caption("My gamme")

def testfunc():
    print "hehhehe"
    
def render():
    ##################### INIT SCREEN #########################################
    screen.fill((0x00, 0x00, 0x00))
    pygame.draw.rect(screen, (0x00, 0xFF, 0x00), [55, 50, 20, 25])
    
    brect = background.get_rect().size
    screen.blit(background,( SCREEN_WIDTH / 2 - brect[0] / 2,SCREEN_HEIGHT / 2 - brect[1] / 2))

    ###########################################################################
    if game_state == 0: ### SPLASH
        rect = playButton.get_rect().size
        screen.blit(playButton,( SCREEN_WIDTH / 2 - rect[0] / 2,SCREEN_HEIGHT / 2 - rect[1] / 2))


    if game_state == 1:

        ##### GAME UI #########################################################

        ##### HIT CALCULATION #################################################

        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("Hit = " + str(GameManager.instance.hit_count) + " / " + str(GameManager.instance.attack_count),True,(0xFF, 0xFF, 0xFF))

        screen.blit(text, [0, 0])
        

        ##### SCHEDULE ANIMATIONS | EVENTS ####################################

        schedule()

    if game_state == 2:
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("END GAME",True,(0xFF, 0xFF, 0xFF))

        hit_count = font.render("Hit   : " + str(GameManager.instance.hit_count),True,(0xFF, 0xFF, 0xFF))
        attack_count = font.render("Attack: " + str(GameManager.instance.attack_count),True,(0xFF, 0xFF, 0xFF))

        screen.blit(text, [0, 0])
        screen.blit(hit_count, [SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.4])
        screen.blit(attack_count, [SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.6])

    pygame.display.flip()
    
def schedule():
    ################ DEFINITIONS ##########################################
    
    global base_time_stamp
    global finish_time_stamp
    global game_state
    
    if finish_spawn == False:
        ################ SPAWN CALCULATION ################################
        elapse_time_from_last_spawn = pygame.time.get_ticks() - base_time_stamp
        spawn_rate = GameManager.instance.SPAWN_RATE * elapse_time_from_last_spawn / 10.0
        rate = random.randint(GameManager.instance.DELAY_SPAWN, 100)
        
        if rate <= spawn_rate:
            x = random.randint(0,2)
            spawnMonster(x)
            base_time_stamp = pygame.time.get_ticks()
    else:
        ################ TIMING TO ENDGAME ################################
        if (pygame.time.get_ticks() - finish_time_stamp) > TIME_FROM_LAST_MONSTER_SPAWN_TO_END_GAME:
            game_state = 2

    #print '------------------------'
    #print spawn_rate
    #print rate
    #print '------------------------'

    ################ HANDLE ###############################################
    ####### ENEMY ############
    for enemy in m_enemy_list:
        if enemy.current_state == 0: ### SPAWN

            rect = enemy.animation[0].getRect()
            enemy.animation[0].blit(screen, (enemy.positionX - rect.width / 2, enemy.positionY - rect.height / 2))
            if enemy.timing[0] < (pygame.time.get_ticks() - enemy.start_time):
                enemy.current_state = 1
                enemy.animation[0].stop()
                enemy.animation[1].play()
                enemy.start_time = pygame.time.get_ticks()
        if enemy.current_state == 1: ### WAIT
            rect = enemy.animation[1].getRect()
            enemy.animation[1].blit(screen, (enemy.positionX - rect.width / 2, enemy.positionY - rect.height / 2))  
            if enemy.timing[1] < (pygame.time.get_ticks() - enemy.start_time): #### TIME OUT ####
                enemy.current_state = 2
                enemy.animation[1].stop()
                enemy.animation[2].play()
                enemy.start_time = pygame.time.get_ticks()
        if enemy.current_state == 2: ### ESCAPE 
            rect = enemy.animation[2].getRect()
            enemy.animation[2].blit(screen, (enemy.positionX - rect.width / 2, enemy.positionY - rect.height / 2))  
            if enemy.timing[2] < (pygame.time.get_ticks() - enemy.start_time): #### TIME OUT ####
                enemy.current_state = 4
                enemy.animation[2].stop()
                m_enemy_list.remove(enemy)
        if enemy.current_state == 3: ### DYING
            rect = enemy.animation[3].getRect()
            enemy.animation[3].blit(screen, (enemy.positionX - rect.width / 2, enemy.positionY - rect.height / 2))
            if enemy.timing[3] < (pygame.time.get_ticks() - enemy.start_time): #### TIME OUT ####
                enemy.current_state = 4
                enemy.animation[2].stop()
                m_enemy_list.remove(enemy)
    ##### ATTACK ANIMATION ####
    for attack_animation in m_attack_animation_list:
        bounding_box = attack_animation.animation.getRect()
        attack_animation.animation.blit(screen, (attack_animation.position[0] - bounding_box.width / 2, attack_animation.position[1] - bounding_box.height / 2))
        if (pygame.time.get_ticks() - attack_animation.start_time) > attack_animation.duration:
            attack_animation.animation.stop()
            m_attack_animation_list.remove(attack_animation)

BOUNDING_SPAWN_AREA = 50

def spawnMonster(code):
    global spawned_enemy
    global finish_spawn
    global finish_time_stamp
    spawned_enemy = spawned_enemy + 1
    if spawned_enemy == GameManager.instance.num_of_enemy:
        finish_spawn = True
        finish_time_stamp = pygame.time.get_ticks()

    posX = random.randint(0 + BOUNDING_SPAWN_AREA, SCREEN_WIDTH - BOUNDING_SPAWN_AREA)
    posY = random.randint(0 + BOUNDING_SPAWN_AREA, SCREEN_HEIGHT - BOUNDING_SPAWN_AREA)

    if code == 0:
        new_enemy = Enemy(
                          posX, 
                          posY, 
                          (ANIM.getBoltanim(), ANIM.getGengaranim(), ANIM.getSmokeanim(), ANIM.getExplosionanim()),
                          (900, 2000, 900, 2000),
                          pygame.time.get_ticks(),
                          0,
                          30 )
        new_enemy.animation[0].play()
        m_enemy_list.append(new_enemy)
    
    if code == 1:
        new_enemy = Enemy(
                          posX, 
                          posY, 
                          (ANIM.getBoltanim(), ANIM.getPsyduckanim(), ANIM.getSmokeanim(), ANIM.getExplosionanim()),
                          (900, 2000, 900, 2000),
                          pygame.time.get_ticks(),
                          0,
                          30 )
        new_enemy.animation[0].play()
        m_enemy_list.append(new_enemy)

    if code == 2:
        new_enemy = Enemy(
                          posX, 
                          posY, 
                          (ANIM.getBoltanim(), ANIM.getDusknoiranim(), ANIM.getSmokeanim(), ANIM.getExplosionanim()),
                          (900, 2000, 900, 2000),
                          pygame.time.get_ticks(),
                          0,
                          30 )
        new_enemy.animation[0].play()
        m_enemy_list.append(new_enemy)
def checkClickWithinCircle(center_point, radius, click_position):
    if ((center_point[0] - click_position[0]) * (center_point[0] - click_position[0]) + (center_point[1] - click_position[1]) * (center_point[1] - click_position[1])) < (radius * radius) : #within
        return True
    return False
def click(pos):
    global game_state
    if game_state == 0:
        game_state = 1
        return

    attack_anim = AttackAnimation(pos, ANIM.getAttackanim1(), pygame.time.get_ticks(), 1250)
    attack_anim.animation.play()
    m_attack_animation_list.append(attack_anim)

    GameManager.instance.smash()

    hit = False

    for enemy in m_enemy_list:
        if enemy.current_state == 3:
            continue
        bounding_box = enemy.animation[enemy.current_state].getRect()
        is_within = checkClickWithinCircle((enemy.positionX, enemy.positionY ), 
                                            bounding_box.width / 2, 
                                            pos)
        if is_within == True:
            enemy.animation[3].play()
            enemy.animation[enemy.current_state].stop()
            enemy.current_state = 3
            enemy.start_time = pygame.time.get_ticks()
            hit = True
    if hit == True:
        GameManager.instance.hitEnemy()
