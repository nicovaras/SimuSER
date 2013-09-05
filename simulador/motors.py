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

import math
import settings
class Motors:
    def __init__(self):
        self.time = 0
        self.left_power = 0
        self.right_power = 0
        self.rotation_delta = 0
        self.speed = 0

    def remaining_time(self):
        return self.time

    def are_on(self):
        return self.time > 0

    def tick(self):
        self.time -= settings.motor_duration()
        self.time = max(0,self.time)

    def set_and_start(self, time, left, right):
        self.time = time
        self.left_power = left
        self.right_power = right
        self.compute_direction()

    def compute_direction(self):
        direction = float(self.left_power - self.right_power) 
        self.rotation_delta = direction*self.time/settings.rotation_constant()
        
        self.speed = (self.left_power + self.right_power)/2 * (settings.robot_speed()/100.0)

    def update_position_from(self, position, angle):
        normalized_angle = ((int((angle*57.2957795)/10))*10)/57.2957795
        print normalized_angle
        x,y= self.basic_rotation_with(normalized_angle)
        #x,y= self.apply_rotation_matrix_to(x,y)
        return position[0] + int(x), position[1] + int(y)

    def basic_rotation_with(self,angle):
        return (math.cos(angle) * self.speed, math.sin(angle) * self.speed)

    def apply_rotation_matrix_to(self,x,y):
        x = math.cos(self.rotation_delta) * x + math.sin(self.rotation_delta) * y 
        y = math.cos(self.rotation_delta) * y - math.sin(self.rotation_delta) * x
        return x,y