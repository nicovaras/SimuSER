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


from image_controller import *
import math
class RobotSprite():
    def __init__(self):
        self.robot_img_controller = ImageController("robot")
        self.led_img_controller = ImageController("robot_led_on")  
        self.current_controller = self.robot_img_controller

    def led_on(self):
        self.current_controller = self.led_img_controller

    def led_off(self):
        self.current_controller = self.robot_img_controller

    def rotate(self, angle):
        current_angle = math.degrees(angle % (2*math.pi))
        index = int(current_angle /10)
        self.robot_img_controller.set_index(index)
        self.led_img_controller.set_index(index)

    def center(self):
        return self.get_img().get_rect().center

    def get_img(self):
        return self.current_controller.current()