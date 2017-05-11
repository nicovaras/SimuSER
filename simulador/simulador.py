# This file is part of SimuSER.

# SimuSER is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SimuSER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SimuSER.  If not, see <http://www.gnu.org/licenses/>.

# Copyright 2013 Federico Raimondo, Leandro Nunez, Nicolas Rosner,
# Mariano Moscato, Diego Fernandez Slezak, Ignacio Kovacs, Nicolas Varaschin

# Department of Computer Sciences, FCEyN, University of Buenos Aires

#from version import svnversion
import pygame
from pygame.locals import *
import box_background
import robot
import debug_info
import settings
import pickle

# print "This sim SimuSER version", svnversion
class SimuSER:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('SerSim')
        self.show_debug = settings.print_debug()
        self.show_proximity = settings.draw_proximity()
        self.show_robot_trace = settings.draw_trace()
        self.show_collision_box = False
        self.show_ids = False
        self.start()
        
    def start(self):
        self.screen_size = settings.screen_size()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.background = pygame.Surface(self.screen_size).convert()
        self.box_background, self.terrain = self.load_backgrounds()
        self.robot_trace_background = pygame.Surface(self.screen_size, pygame.SRCALPHA, 32).convert_alpha()
        self.robots = self.load_robots()
        self.debug = debug_info.DebugInfo(self.robots[0])
        self.turbo_multiplier = 1

    def load_robots(self):
        robots = [robot.Robot()]
        robot_file = settings.get_robot_file()
        if robot_file:
            robots = []
            with open(robot_file) as f:
                data = f.read().split()
                for i in range(0,len(data),4):
                    r = robot.Robot()
                    r.set_code(data[i].strip())
                    r.position = tuple([int(x) for x in data[i+1].split(',')])
                    r.theta = float(data[i+2])
                    r.id = i/4 +1 
                    r.change_team(int(data[i+3]))
                    robots.append(r)
            self.show_ids = True
        return robots

    def load_backgrounds(self):
        if settings.map_file():
            box_matrix, img_str, size =  pickle.load( open( settings.get_full_file_path(settings.map_file()), "rb" ) )
            return box_background.BoxBackground(box_matrix), pygame.image.fromstring(img_str, size, "RGB")
        else:
            return box_background.BoxBackground(), pygame.image.load(settings.get_full_file_path(settings.background())).convert()

    #Public#

    def main_loop(self):
        done = False
        while not done:
            self.draw_backgrounds()
            for robot in self.robots:
                if self.show_robot_trace:
                    self.background.blit(self.robot_trace_background,(0,0))
            self.tick_clock()
            for robot in self.robots:
                for i in range(self.turbo_multiplier):
                    self.run_robot(robot)
                    robot.update_position(self.box_background.boxes)
                    self.draw_robot(robot)

            for event in pygame.event.get():
                self.handle_event(event)

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    #Private#

    def draw_robot(self, robot):
        pygame.draw.circle(self.robot_trace_background, (0,0,0),(int(robot.position[0])+16,int(robot.position[1])+16) , 4)
       
        self.background.blit(robot.sprite.get_img(), robot.position)
        if self.show_collision_box:
            pygame.draw.rect(self.background, (0,0,0), robot.get_collision_rect())
        if self.show_ids:
            self.background.blit(pygame.font.SysFont("Arial",22,True).render(str(robot.id), 1,(0,0,0)), (robot.position[0]+10,robot.position[1]+7))
            self.background.blit(pygame.font.SysFont("Arial",22,True).render(str(robot.id), 1,(0,0,0)), (robot.position[0]+13,robot.position[1]+10))
            self.background.blit(pygame.font.SysFont("Arial",22).render(str(robot.id), 1,(255,255,255)),(robot.position[0]+11,robot.position[1]+8))

    def handle_event(self, event):
        if event.type == QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise SystemExit
            if event.key == pygame.K_F1:
                self.show_debug = (not self.show_debug)
            if event.key == pygame.K_F2:
                self.show_proximity = (not self.show_proximity)
            if event.key == pygame.K_F3:
                self.show_robot_trace = (not self.show_robot_trace)
            if event.key == pygame.K_F4:
                self.show_collision_box = (not self.show_collision_box)
            if event.key == pygame.K_SPACE:
                self.turbo_multiplier = 10
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self.start()
            if event.key == pygame.K_SPACE:
                self.turbo_multiplier = 1


    def draw_backgrounds(self):
        self.draw_floor()
        self.box_background.draw_boxes_in(self.background)

    def draw_floor(self):
        self.background.blit(self.terrain,(0,0))

    def run_robot(self, robot):
        if self.show_debug:
            self.print_debug()
        self.draw_box_score()
        self.calculate_proximity(robot)
        robot.sense_color_of(self.terrain)        
        robot.next_instruction()

    def draw_box_score(self):
        score1 = str(len(filter(lambda x: x.color == 1, self.box_background.boxes)))
        score2 = str(len(filter(lambda x: x.color == 2, self.box_background.boxes)))
        font = pygame.font.SysFont("Arial",100)
        pos = (50,400)
        self.background.blit(font.render(score1, 1,(0,0,0)), (pos[0]-1,pos[1]-1))
        self.background.blit(font.render(score1, 1,(0,0,0)), (pos[0]+1,pos[1]+1))
        self.background.blit(font.render(score1, 1,(200,0,0)), pos)
        pos = (680,400)
        self.background.blit(font.render(score2, 1,(0,0,0)), (pos[0]-1,pos[1]-1))
        self.background.blit(font.render(score2, 1,(0,0,0)), (pos[0]+1,pos[1]+1))
        self.background.blit(font.render(score2, 1,(0,200,0)), pos)


    def print_debug(self):
        self.debug.draw_debug_info_in(self.background)
        self.debug.print_instructions()

    def tick_clock(self):
        self.clock.tick(settings.clock_speed())

    def calculate_proximity(self, robot):
        index = self.robots.index(robot)
        lines = robot.proximity_lines(self.box_background.boxes,self.robots[:index]+self.robots[index+1:])
        for (start,end) in lines:
            pygame.draw.line(self.background, (0,0,0), start,end, 3*self.show_proximity)

SimuSER().main_loop()
