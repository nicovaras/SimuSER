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

#pasar registros, 
#click para saber como llegar
#ver que settings releer en cada paso y cuales dejar fijas
#No implementado todavia, solo pido un posible int_ptr
#constantes para leds, sensores

from instructions import *
from decoder import *
from motors import *
from sensor_manager import *
from robot_sprite import *
import math
import pygame
import settings
import instructions


class Robot:
    def __init__(self):
        self.code = Decoder().code_from(settings.source_file())
        self.IP = self.header_size()
        self.motors = Motors()
        self.position = settings.initial_position()
        self.registers = [0] * 256
        self.stack = [] #[ip1,ip2,ip3....]
        self.memory = {}
        self.done = False
        self.theta = settings.initial_angle()
        self.sensor_manager = SensorManager()
        self.sprite = RobotSprite()

    def next_instruction(self):
        if self.done:
            return

        if self.motors.are_on():
            self.motors.tick()
            return
       
        self.IP = self.execute_instruction()

        if self.IP >= len(self.code):
            self.done = True

    def execute_instruction(self):
        IP = self.IP
        next_IP = IP + 4
        
        instruction = self.code[IP]
        byte_1 = self.code[IP+1]
        byte_2 = self.code[IP+2]
        byte_3 = self.code[IP+3]

        if instruction == MOV_V16_IMM16:
            self.registers[byte_1] = (byte_3<<8) + byte_2

        elif instruction == MOV_V16d_V16s:
            self.registers[byte_1] = self.registers[byte_2]

        elif instruction == LOAD_V16_IMM16:
            self.registers[byte_1] = self.memory.get((byte_3<<8) + byte_2,0)

        elif instruction == LOAD_V16d_V16s:
            self.registers[byte_1] = self.memory.get(byte_2,0)

        elif instruction == STORE_IMM16_V16:
            self.memory[(byte_3<<8) + byte_2] = self.registers[byte_1]

        elif instruction == STORE_V16_IMM16:
            self.memory[self.registers[byte_1]] = (byte_3<<8) + byte_2

        elif instruction == STORE_V16d_V16s:
            self.memory[self.registers[byte_1]] = self.registers[byte_2]

        elif instruction == INC_V16:
            self.registers[byte_1] += 1

        elif instruction == DEC_V16:
            self.registers[byte_1] -= 1

        elif instruction == ADD_V16_IMM16:
            self.registers[byte_1] += (byte_3<<8) + byte_2

        elif instruction == ADD_V16d_V16s:
            self.registers[byte_1] += self.registers[byte_2]

        elif instruction == SUB_V16_IMM16:
            self.registers[byte_1] -= (byte_3<<8) + byte_2

        elif instruction == SUB_V16d_V16s:
            self.registers[byte_1] -= self.registers[byte_2]

        elif instruction == MUL_V16_IMM16:
            self.registers[byte_1] *= (byte_3<<8) + byte_2

        elif instruction == MUL_V16d_V16s:
            self.registers[byte_1] *= self.registers[byte_2]

        elif instruction == DIV_V16_IMM16:
            self.registers[byte_1] /= (byte_3<<8) + byte_2

        elif instruction == DIV_V16d_V16s:
            self.registers[byte_1] /= self.registers[byte_2]

        elif instruction == JMP_PTR:
            next_IP = ((byte_3<<16) + (byte_2<<8) + byte_1)*4 + self.header_size()

        elif instruction == SKIPZ_V16:
            if self.registers[byte_1] == 0:
                next_IP += 4

        elif instruction == SKIPE_V16_IMM16:
            if self.registers[byte_1] == (byte_3<<8) + byte_2:
                next_IP += 4

        elif instruction == SKIPE_V16d_V16s:
            if self.registers[byte_1] == self.registers[byte_2]:
                next_IP += 4

        elif instruction == SKIPNE_V16_IMM16:
            if self.registers[byte_1] != (byte_3<<8) + byte_2:
                next_IP += 4

        elif instruction == SKIPNE_V16d_V16s:
            if self.registers[byte_1] != self.registers[byte_2]:
                next_IP += 4

        elif instruction == SKIPG_V16_IMM16:
            if self.registers[byte_1] > (byte_3<<8) + byte_2:
                next_IP += 4

        elif instruction == SKIPG_V16d_V16s:
            if self.registers[byte_2] > self.registers[byte_1]:
                next_IP += 4
        
        elif instruction == SKIPL_V16_IMM16:
            if self.registers[byte_1] < (byte_3<<8) + byte_2:
                next_IP += 4
        
        elif instruction == SKIPL_V16d_V16s:
            if self.registers[byte_2] < self.registers[byte_1]:
                next_IP += 4
        
        elif instruction == SKIPGE_V16_IMM16:
            if self.registers[byte_1] >= (byte_3<<8) + byte_2:
                next_IP += 4

        elif instruction == SKIPGE_V16d_V16s:
            if self.registers[byte_2] >= self.registers[byte_1]:
                next_IP += 4
        
        elif instruction == SKIPLE_V16_IMM16:
            if self.registers[byte_1] <= (byte_3<<8) + byte_2:
                next_IP += 4

        elif instruction == SKIPLE_V16d_V16s:
            if self.registers[byte_2] <= self.registers[byte_1]:
                next_IP += 4

        elif instruction == SENSE_V16_ID8:
            self.registers[byte_1] = self.sensor_manager.sense_from(byte_2)

        elif instruction == MOTOR_IMM8_P8_P8:
            self.motors.set_and_start(byte_1,self.complement(byte_2),self.complement(byte_3))

        elif instruction == LED_ID8_ST8:
            if byte_2 == 0xff:
                self.sprite.led_on()
            else:
                self.sprite.led_off()

        elif instruction == IRET:
            next_IP = self.stack.pop()

        elif instruction == IRETN:
            next_IP = self.stack.pop()
            next_IP += 4

        elif instruction == CALL_PTR:
            self.stack.append(IP)
            next_IP = ((byte_3<<16) + (byte_2<<8) + byte_1)*4 + self.header_size()

        elif instruction == RET:
            next_IP = self.stack.pop()
            next_IP += 4

        elif instruction == NOP:
            pass
            
        elif instruction == HALT:
            self.done = True

        return next_IP


    def update_position(self, boxes):
        if self.motors.are_on():
            previous_position = self.position
            self.position = self.motors.update_position_from(self.position, self.theta)
            if self.collides_with(boxes):
                self.position = previous_position
            
            self.theta += self.motors.rotation_delta
            self.theta = self.theta % 6.28
            self.sprite.rotate(self.theta)

        return self.position

    def collides_with(self,boxes):
        boxlist = [pygame.Rect(box[0],box[1],32,32) for box in boxes]
        robot_rect = pygame.Rect(self.position, (32,32))
        return robot_rect.collidelist(boxlist) != -1 

    def sense_color_of(self, surface):
        self.sensor_manager.sense_color_of(self.get_center(),surface,self.theta)

    def proximity_line(self,boxes):        #Sacar de esta clase
        start = self.get_center()
        end = self.sensor_manager.sense_end_point(start,self.theta,boxes)
        return start, end

    def header_size(self):
        return settings.header_size()

    def handle_interruption(self,interruption_ptr):
        self.stack.append(self.IP)
        next_IP = interruption_ptr

    def complement(self,value):
        #por ahora solo de a 1 byte
        if value > 256:
            raise Exception("Complemento por ahora solo de a 1 byte")
        if value > 127:
            return value - 256
        else:
            return value
            
    def get_center(self):
        center = self.sprite.center()
        return int(self.position[0]) + center[0] , int(self.position[1]) + center[1]

    def set_code(self, input_file):
         self.code = Decoder().code_from(input_file)