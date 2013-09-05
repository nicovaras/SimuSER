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

import settings
import pygame

class BoxBackground:
    def __init__(self, matrix = None):
        if matrix:
            self.boxes = self.load_boxes_from(matrix)
        else:
            self.boxes = self.load_boxes_from_file()
        self.box_img = pygame.image.load(settings.get_full_file_path("img/box.png")).convert()

    #Public#
    def draw_boxes_in(self, background):
        for box_position in self.boxes:
            background.blit(self.box_img, box_position)

    #Private#
    def load_boxes_from(self,matrix):
        self.boxes = []
        for i in range(19):
            for j in range(25):
                if matrix[i][j] == 1:
                    self.boxes.append((j*32,i*32))
        return self.boxes

    def load_boxes_from_file(self):
        #Los mapas son grids de 19*25 (que multiplicado por 32 da aprox 800*600)
        self.boxes = []
        self.box_map = open(settings.get_full_file_path(settings.box_matrix()), "r")
        for i in range(19):
            line = self.box_map.readline()
            for j in range(25):
                if line[j] == '1':
                    self.boxes.append((j*32,i*32))
        return self.boxes