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
        self.render_font_at("Registers: " + self.register_print(), (5,570), surface)

    def draw_angle(self, surface):
        self.render_font_at("Angle: " + str(int(100*math.degrees(self.robot.theta))/100.0), (5,100), surface)
    
    def draw_motors(self, surface):
        self.render_font_at("Motors: " + str(self.robot.motors.left_power) + " " +str(self.robot.motors.right_power), (5,20), surface)
        self.render_font_at("Motor Time: " + str(self.robot.motors.remaining_time()), (5,40), surface)

    def draw_color_sensors(self, surface):
        xpos, ypos = 5, 60
        self.render_font_at("Color Sensor: ", (xpos, ypos), surface)

        for i in range(len(self.robot.sensor_manager.color_sensors)):
	        pygame.draw.rect(surface, (0,0,0), [xpos + 125 + 17*i, ypos + 7, 12, 12], 2)
	        pygame.draw.rect(surface, self.robot.sensor_manager.color_sensors[i].current_color, [xpos + 126 + 17*i, ypos + 8, 10, 10])
	        

    def draw_proximity(self, surface):
        string = "Proximity Sensor: " 
        for sensor in self.robot.sensor_manager.proximity_sensors:
            string += str(sensor.proximity) + " "
        self.render_font_at(string, (5,80), surface)

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
    
    def render_font_at(self, string, pos, surface):
        surface.blit(self.font.render(string, 1,(0,0,0)), (pos[0]-1,pos[1]-1))
        surface.blit(self.font.render(string, 1,(0,0,0)), (pos[0]+1,pos[1]+1))
        surface.blit(self.font.render(string, 1,(255,255,255)), pos)


