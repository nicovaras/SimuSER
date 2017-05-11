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
import math
class ProximitySensor():
    def __init__(self, direction = 0):
        self.proximity = 255
        self.direction = direction

    def get_sensor_value(self):
        return self.proximity

    def sense_end_point(self, start, angle, boxes, robots):
        max_proximity = 80 #settings.max_proximity() #pasar a __init__
        end_point = start[0] + math.cos(angle+self.direction)*max_proximity,start[1] + math.sin(angle+self.direction)*max_proximity

        distance = 255
        self.proximity = distance
        for i in range(0,max_proximity,4):
            point = start[0] + math.cos(angle+self.direction)*i ,start[1] + math.sin(angle+self.direction)*i
            if self.collides_with_box(boxes,point) or self.collides_with_robot(robots,point):
                end_point = point
                self.proximity = i
                break
              
        return end_point
    
    def collides_with_robot(self,robots,point):
        for robot in robots:
            pos = robot.position
            if point[0] >= pos[0] and point[0] <= pos[0]+32 and point[1] >= pos[1] and point[1] <= pos[1]+32:
                return True
        return False

    def collides_with_box(self,boxes,point):
        for box in boxes:
            if point[0] >= box.pos[0] and point[0] <= box.pos[0]+32 and point[1] >= box.pos[1] and point[1] <= box.pos[1]+32:
                return True
        return False
