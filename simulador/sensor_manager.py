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

from color_sensors import *
from proximity_sensor import *
import settings
import math

class SensorManager():
    def __init__(self):
        self.color_sensors = [ColorSensor(0,-0.785),
                              ColorSensor(1,0.0),
                              ColorSensor(2,0.785)]
        self.proximity_sensors = [ProximitySensor(),ProximitySensor(-math.pi/2),ProximitySensor(math.pi/2)]
        self.sensor_ids = { 3: self.color_sensors[0],
                            4: self.color_sensors[1],
                            5: self.color_sensors[2],
                            1: self.proximity_sensors[0],
                            2: self.proximity_sensors[1],
                            0: self.proximity_sensors[2]}


    def sense_from(self, sensor_id):
        return self.sensor_ids[sensor_id].get_sensor_value()

    def sense_color_of(self, center, surface, theta):
        for color_sensor in self.color_sensors:
            color_sensor.sense_at(surface, center, theta)

    def sense_end_point(self, start, angle, boxes, robots):
        return [self.proximity_sensors[i].sense_end_point(start,angle,boxes,robots) for i in range(len(self.proximity_sensors))]
