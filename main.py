#oficial

import pygame, cv2, random, os


class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False  
        
        
        #inciciando o video 
        self.is_video_playing = True
        self.play = pygame.image.load('images/play.png').convert_alpha()
        self.stop = pygame.image.load('images/stop.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright = (WINDOW_WIDTH - 50, 10))
    
        
        #iniciando a musica:
        self.is_music_playing = True
        self.sound_on = pygame.image.load('images/speaker.png').convert_alpha()
        self.sound_off = pygame.image.load('images/mute.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright = (WINDOW_WIDTH - 10, 10))
        #COLOCANDO A MÚSICA:
        pygame.mixer.music.load('sounds/bgmusic.mp3')
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play()
        
    
    def update(self,event_list): 
        self.draw()
      
    def draw(self):
        screen.fill(BLACK)
    
        #FONTS
        title_font =  pygame.font.Font('fonts/Little Alien.ttf', 44)
        content_font = pygame.font.Font('fonts/Little Alien.ttf', 24)
        
        #TEXT
        title_text = title_font.render('Memory Game', True, WHITE)
        title_rect = title_text.get_rect(midtop = (WINDOW_WIDTH // 2, 10))
        
        level_text = content_font.render('Nível ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop = (WINDOW_WIDTH //2, 80))
        
        #AQUI COLOCAMOS A INSTRUÇÃO EM PORTUGUÊS E INGLÊS
        info_text = content_font.render('Selecione 2 de cada: ', True, WHITE)
        info_rect = info_text.get_rect(midtop = (WINDOW_WIDTH //2, 120))
        
        if not self.level == 5:
          next_text = content_font.render('Nível completo. Pressione espaço para o próximo nível', True, WHITE)
        else: 
          next_text = content_font.render('Parabéns você venceu. Pressione espaço para jogar novamente.', True, WHITE)
        next_rect = next_text.get_rect(midbottom = (WINDOW_WIDTH //2, WINDOW_HEIGHT - 40))  
          
        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH - 90, 0, 100, 50))
        screen.blit(self.music_toggle, self.music_toggle_rect)
        screen.blit(self.video_toggle, self.video_toggle_rect)
        
        if self.level_complete:
           screen.blit(next_text, next_rect)
    
pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT  = 860
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory Game')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()


game =Game()

running = True
while running:
    game_list = pygame.event.get()
    for event in game_list:
        if event.type == pygame.QUIT:
            running = False
         
    game.update(game_list)
    
    
    pygame.display.update()
    clock.tick(FPS)     


pygame.quit()