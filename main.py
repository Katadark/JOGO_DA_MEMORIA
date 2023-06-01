#oficial

from typing import Any

import pygame, cv2, random, os


class Tile(pygame.sprite.Sprite):
      def __init__(self, filename, x, y):
        super().__init__()
        
        self.name = filename.split('.')[0]
        
        #selecionando a pasta game que contem as imagens da carta
        self.original_image = pygame.image.load('images/cartas/' + filename)

        self.back_image = pygame.image.load('images/cartas/' + filename)
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())
        
        self.image = self.back_image
        self.react = self.image.get_rect(topleft = (x, y))
        self.shown = False
        
      def update(self):
        self.image = self.original_image if self.shown else self.back_image
        
      def show(self):
        self.shown = True
      def hide(self):
        self.shown = False
        
        

class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False  
        
        #cards
        self.all_cartas = [f for f in os.listdir('images/cartas') if os.path.join('images/cartas', f)]
        
        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280
        
        self.tiles_group = pygame.sprite.Group()
        
        
        #lançamento e cronometragem 
        self.flipped = []
        self.frame_count = 0
        self.block_game = False
        
        
        #criando o primeiro vídeo
        self.generate_level(self.level)
        
        #adicionando icones e inicializando video
        self.is_video_playing = True
        self.play = pygame.image.load('images/play.png').convert_alpha()
        self.stop = pygame.image.load('images/stop.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright = (WINDOW_WIDTH - 50, 10))
        self.get_video()
    
        
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
        if self.is_video_playing:
           self.sucess, self.img = self.cap.read()
           
        self.user_imput(event_list)
        self.draw()
        self.check_level_complete(event_list)
        
    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []
                                          
                                          
        
        
        
    def generate_level(self, level):
      self.cartas = self.select_random_cartas(self.level)
      self.level_complete = False
      self.rows = self.level + 1
      self.cols = 4
      self.generate_tileset(self.cartas)
      
      
    def generate_tileset(self, cartas):
      self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows
      
      TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
      LEFT_MARING = RIGHT_MARGIN = (self.width - TILES_WIDTH// 2)
      #tiles = []
      self.tiles_group.empty()
      
      
      for i in range(len(cartas)):
        x = LEFT_MARING + ((self.img_width + self.padding) * (i % self.cols))
        y = self.margin_top + (i// self.rows * (self.img_height + self.padding))
        tile = Tile(cartas[i], x,y)
        self.tiles_group.add(tile)
        
    
    def select_random_cartas(self, level):
       cartas = random.sample(self.all_cartas, (self.level + self.level + 2))
       cartas_copy = cartas.copy()
       cartas.extend(cartas_copy)
       random.shuffle(cartas)
       return cartas 
      
      
    
        
       #eventos do mouse com o video
    def user_imput(self, event_list):
       for event in event_list:
         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
              if self.is_music_playing:
                 self.is_music_playing = False
                 self.music_toggle = self.sound_off
                 pygame.mixer.music.pause()
              else:
                self.is_music_playing = True
                self.music_toggle = self.sound_on
                pygame.mixer.music.unpause()
                
            if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
              if self.is_video_playing:
                  self.is_video_playing = False
                  self.video_toggle = self.stop
              else:
                self.is_video_playing = True
                self.video_toggle = self.play
                
         if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 6:
                        self.level = 1
                    self.generate_level(self.level)
                
                   
      
      
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
        
        
        if self.is_video_playing:
          if  self.sucess:
             screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))
          else:
             self.get_video()
             
        else:
          screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))
        
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
        
        #colocando as cartas na tela
        self.tiles_group.draw(screen)
        self.tiles_group.update() 
        
        if self.level_complete:
           screen.blit(next_text, next_rect)
   
      #inserindo video de fundo
    def get_video(self):
      self.cap = cv2.VideoCapture('videos/bgvideo.mp4')
      self.sucess, self.img = self.cap.read()
      self.shape = self.img.shape[1::-1]
  
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
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
         
    game.update(event_list)
    
    
    pygame.display.update()
    clock.tick(FPS)     


pygame.quit()
