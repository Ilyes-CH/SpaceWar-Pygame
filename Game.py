import pygame
import time
import os
import random

# initializing components
pygame.font.init()
pygame.mixer.init()

# configurations of the game
WIDTH, HEIGHT = 1000, 500
WHITE =(255,255,255)
FONT = pygame.font.SysFont('comiscans',30) 
STAR_WIDTH: int = 20
STAR_HEIGHT: int = 35
STAR_VEL :int = 5
player_x : int = 200
Player_width :int = 60
Player_height :int = 60
player_y : int = HEIGHT-Player_height
velocity : int = 5
# to configure window size
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Dodge')

BG = pygame.transform.scale(pygame.image.load(
    os.path.join('C:/Users/username/OneDrive/Bureau/SpaceWar-Pygame','bg.jpeg')),
                           (WIDTH,HEIGHT))


star_pic = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join('C:/Users/username/OneDrive/Bureau/SpaceWar-Pygame','bullet.png')
),(STAR_WIDTH,STAR_HEIGHT)),180)

ship = pygame.transform.scale(pygame.image.load(
    os.path.join('C:/Users/username/OneDrive/Bureau/SpaceWar-Pygame','spaceship_red.png')
    ),(Player_width,Player_height) )

#Music
music = pygame.mixer.music.load('space_music.mp3')
pygame.mixer.music.play(-1)
 


# drawing into screen
def draw(player,elapsedTime,stars,Lives):
# WIN.fill(WHITE)
    WIN.blit(BG,(0,0))
    WIN.blit(ship,(player.x,player.y))
# draw a font
    time_text = FONT.render(f"Time: {round(elapsedTime)}s",1,WHITE)
    WIN.blit(time_text,(10,10))
#Lives
    showLives(Lives) 
#draw stars
    for star in stars:
        WIN.blit(star_pic,(star.x,star.y))
        # pygame.draw.rect(WIN,WHITE,star)
    pygame.display.update()

# game mechanics
def movements(keys_pressed,player):
    if keys_pressed[pygame.K_LEFT] and player.x>0:
        player.x -=  velocity
    if keys_pressed[pygame.K_RIGHT] and player.x<WIDTH-Player_width:
        player.x +=  velocity
    if keys_pressed[pygame.K_UP] and player.y>0:
        player.y -=  velocity
    if keys_pressed[pygame.K_DOWN] and player.y <HEIGHT-Player_height:
        player.y += velocity

# Lives count

def showLives(Lives):

    for i in  Lives:
        live_text1= FONT.render(f'Lives: {i}',1,WHITE)
    WIN.blit(live_text1,(10,30))
    
    
    
# main game loop
def main():
    run = True
    hit = False
#handle time

    start_time = time.time()
    elapsed_time = 0
    
#Projectiles
    star_add_increment : int = 2000    
    star_count : int = 0 
    stars : list = []
    Lives=[1,2,3,4]
    
# creating the player's rectangle
    player = pygame.Rect(500, HEIGHT-Player_height, Player_width,Player_height)
    global velocity
    clock = pygame.time.Clock()
    
    while run:
    # fps
        star_count += clock.tick(60) 

        elapsed_time = time.time()-start_time
        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH) 
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH,STAR_HEIGHT)        
                stars.append(star)
            star_add_increment = max(200,star_add_increment - 50)
            star_count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys_pressed = pygame.key.get_pressed()
        movements(keys_pressed,player)
         
            
        for star in stars[:]:             
            star.y += STAR_VEL
            if star.y> HEIGHT:
                stars.remove(star)
                
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                Lives.pop()
                print(Lives)
                hit = True
                break

            
        if hit and len(Lives) == 0:
            Score = FONT.render(f"Your Score: {round(elapsed_time)}",1,WHITE)
            WIN.blit(Score,(WIDTH/2 - Score.get_width()/2 -5,HEIGHT/2 - Score.get_height()/2 -30))

            lost_text = FONT.render("You Lost!",1,WHITE)
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2,HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(player,elapsed_time,stars,Lives)

    pygame.quit()


    
if __name__ == '__main__':
    main()


