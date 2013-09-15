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

import pygame
import settings
import instructions
import math

class DebugInfo():
    def __init__(self, robot):
        self.robot = robot
        self.font =  pygame.font.SysFont("Arial",20)

    def draw_debug_info_in(self, surface):
        self.draw_registers(surface)
        self.draw_motors(surface)
        self.draw_color_sensors(surface)
        self.draw_proximity(surface)
        self.draw_angle(surface)

    def draw_registers(self, surface):
        register_text = self.font.render("Registers: " + self.register_print(), 1,(0,0,0))
        surface.blit(register_text, (5,570))

    def draw_angle(self, surface):
        angle_text = self.font.render("Angle: " + str(math.degrees(self.robot.theta)) , 1,(0,0,0))
        surface.blit(angle_text, (5,100))
    
    def draw_motors(self, surface):
        motor_text = self.font.render("Motors: " + str(self.robot.motors.left_power) + " " +str(self.robot.motors.right_power), 1,(0,0,0))
        surface.blit(motor_text, (5,20))
        motor_text = self.font.render("Motor Time: " + str(self.robot.motors.remaining_time()), 1,(0,0,0))
        surface.blit(motor_text, (5,40))

    def draw_color_sensors(self, surface):
        color_text = self.font.render("Color Sensor: ", 1,(0,0,0))
        surface.blit(color_text, (5,60))

        for i in range(len(self.robot.sensor_manager.color_sensors)):
	        pygame.draw.rect(surface, (0,0,0), [105 + 15*i, 63, 10, 10], 2)
	        pygame.draw.rect(surface, self.robot.sensor_manager.color_sensors[i].current_color, [106 + 15*i, 64, 9, 9])
	        

    def draw_proximity(self, surface):
        color_text = self.font.render("Proximity Sensor: " + str(self.robot.sensor_manager.proximity_sensors[0].proximity), 1,(0,0,0))
        surface.blit(color_text, (5,80))

    def register_print(self):
        reg_str = ""
        for reg,val in enumerate(self.robot.registers):
            if val != 0:
                reg_str += "reg_"+str(reg)+" = "+str(val)+", "
        for mem,val in self.robot.memory.items():
            reg_str += "mem_"+str(mem)+" = "+str(val)+", "
        return reg_str

    def print_instructions(self):
        if self.robot.done or self.robot.motors.are_on():
            return
        instruction_name = [i[0] for i in instructions.__dict__.items() if i[1] == self.robot.code[self.robot.IP]]
        if instruction_name != []:
            instruction_name = instruction_name[0]
        else:
            instruction_name = "UNKNOWN"
        
        code = self.robot.code
        IP = self.robot.IP   
        print instruction_name, code[IP+1], code[IP+2], code[IP+3]

