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

class ColorSensor(object):
    def __init__(self, index, delta_angle, target_color = (0,0,0), ):
        self.current_color = (0,0,0)
        self.index = index
        self.target_color = target_color
        self.delta_angle = delta_angle

    def get_sensor_value(self):
        if self.current_color[0] < 25 and self.current_color[1] < 25 and self.current_color[2] < 25:
            return 255
        else:
            return 0

    def sense_at(self, surface, center, angle):
        sensor_position = self.sensor_position_from(center, angle + self.delta_angle)    
        try:
            self.current_color = surface.get_at(sensor_position)
        except Exception:
            self.current_color = (0,0,0)


    def sensor_position_from(self, center, angle):
        sensor_position = center[0] + math.cos(angle)*16, center[1] + math.sin(angle)*16
        return int(sensor_position[0]), int(sensor_position[1])

    def get_current_color(self):
        return self.current_color
        

