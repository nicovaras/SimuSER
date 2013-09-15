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

#Controla las diferentes rotaciones, los nombres de las iamgenes deberian
#ser de la forma "name-index.extension"

import pygame
import settings
class ImageController:
    def __init__(self,name,ext = "png",current_index = 0, max_index = 36):
        self.name = name
        self.ext = ext
        self.current_index = current_index
        self.imgs = self.load_images(name,ext,max_index)
        self.max_index = max_index

    def load_images(self,name,ext,max_index):
        imgs = []
        for i in range(0,max_index):
            img = pygame.image.load(settings.get_full_file_path("img/"+name+"-"+str(i)+"."+ext)).convert_alpha()
            imgs.append(img)
        return imgs

    def current(self):
        return self.imgs[self.current_index]

    def set_index(self,i):
        self.current_index = (i-27) %self.max_index