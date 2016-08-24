import pygame
import random
import Resource.AnimationCreator as ANIM
import GameManager

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

###### VARIABLES ##############

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

game_state = 1
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
    
    screen.fill((0x00, 0x00, 0x00))
    pygame.draw.rect(screen, (0x00, 0xFF, 0x00), [55, 50, 20, 25])
    
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
            spawnMonster(0)
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
            enemy.animation[0].blit(screen, (enemy.positionX, enemy.positionY))
            if enemy.timing[0] < (pygame.time.get_ticks() - enemy.start_time):
                enemy.current_state = 1
                enemy.animation[0].stop()
                enemy.animation[1].play()
                enemy.start_time = pygame.time.get_ticks()
        if enemy.current_state == 1: ### WAIT
            enemy.animation[1].blit(screen, (enemy.positionX, enemy.positionY))    
            if enemy.timing[1] < (pygame.time.get_ticks() - enemy.start_time): #### TIME OUT ####
                enemy.current_state = 2
                enemy.animation[1].stop()
                enemy.animation[2].play()
                enemy.start_time = pygame.time.get_ticks()
        if enemy.current_state == 2: ### ESCAPE 
            enemy.animation[2].blit(screen, (enemy.positionX, enemy.positionY))    
            if enemy.timing[2] < (pygame.time.get_ticks() - enemy.start_time): #### TIME OUT ####
                enemy.current_state = 4
                enemy.animation[2].stop()
                m_enemy_list.remove(enemy)
        if enemy.current_state == 3: ### DYING
            enemy.animation[3].blit(screen, (enemy.positionX, enemy.positionY)) 
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


def spawnMonster(code):
    global spawned_enemy
    global finish_spawn
    global finish_time_stamp
    spawned_enemy = spawned_enemy + 1
    if spawned_enemy == GameManager.instance.num_of_enemy:
        finish_spawn = True
        finish_time_stamp = pygame.time.get_ticks()
    if code == 0:
        posX = random.randint(0, SCREEN_WIDTH)
        posY = random.randint(0, SCREEN_HEIGHT)

        
        new_enemy = Enemy(
                          posX, 
                          posY, 
                          (ANIM.getBoltanim(), ANIM.getFlameanim(), ANIM.getSmokeanim(), ANIM.getExplosionanim()),
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

    attack_anim = AttackAnimation(pos, ANIM.getAttackanim1(), pygame.time.get_ticks(), 1250)
    attack_anim.animation.play()
    m_attack_animation_list.append(attack_anim)

    GameManager.instance.smash()

    hit = False

    for enemy in m_enemy_list:
        if enemy.current_state == 3:
            continue
        bounding_box = enemy.animation[enemy.current_state].getRect()
        is_within = checkClickWithinCircle((enemy.positionX + bounding_box.width / 2, enemy.positionY + bounding_box.height / 2), 
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
