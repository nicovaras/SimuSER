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
        self.screen_size = settings.screen_size()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.background = pygame.Surface(self.screen_size).convert()
        self.box_background, self.terrain = self.load_backgrounds()
        self.robots = [robot.Robot()]
        self.debug = debug_info.DebugInfo(self.robots[0])

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
                self.run_robot(robot)
                self.draw_robot(robot)

            for event in pygame.event.get():
                self.handle_event(event)

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    #Private#

    def draw_robot(self, robot):
        if settings.draw_trace():
            pygame.draw.circle(self.terrain, (0,0,0),(robot.position[0]+16,robot.position[1]+16) , 4)
        self.background.blit(robot.sprite.get_img(), robot.update_position(self.box_background.boxes))

    def handle_event(self, event):
        if event.type == QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise SystemExit

    def draw_backgrounds(self):
        self.draw_floor()
        self.box_background.draw_boxes_in(self.background)

    def draw_floor(self):
        self.background.blit(self.terrain,(0,0))

    def run_robot(self, robot):
        self.tick_clock()

        if settings.print_debug():
            self.print_debug()
        
        self.calculate_proximity(robot)
        robot.sense_color_of(self.terrain)        
        robot.next_instruction()

    def print_debug(self):
        self.debug.draw_debug_info_in(self.background)
        self.debug.print_instructions()

    def tick_clock(self):
        self.clock.tick(settings.clock_speed())

    def calculate_proximity(self, robot):
        start,end = robot.proximity_line(self.box_background.boxes)
        pygame.draw.line(self.background, (0,0,0), start,end, settings.draw_proximity())

SimuSER().main_loop()
