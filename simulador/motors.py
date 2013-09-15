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
        self.R = 0.003865148*settings.motor_duration()
        self.l = 55
        self.v = 0
        self.rotation_delta = 0

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
        self.v = (self.R/2.0)*(self.left_power + self.right_power)
        self.rotation_delta = -(self.R/self.l)*(self.right_power - self.left_power)

    def update_position_from(self, position, angle):
        return position[0]+self.v*math.cos(angle),position[1]+self.v*math.sin(angle)