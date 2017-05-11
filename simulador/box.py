import pygame
import settings
class Box:
    def __init__(self,pos):
        self.pos = pos
        self.box_img_grey = pygame.image.load(settings.get_full_file_path("img/box.png")).convert()
        self.box_img_team1 = pygame.image.load(settings.get_full_file_path("img/box1.png")).convert()
        self.box_img_team2 = pygame.image.load(settings.get_full_file_path("img/box2.png")).convert()
        self.color = 0

    def image(self):
        if self.color == 0:
            return self.box_img_grey
        elif self.color == 1:
            return self.box_img_team1
        elif self.color == 2:
            return self.box_img_team2
