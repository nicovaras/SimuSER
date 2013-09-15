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


'''
    Referencias
    
    R16     Celda de variables de 16 bits (hay 256 celdas)
    IMM8    Numero entero de 8 bits sin signo
    IMM16   Numero entero de 16 bits sin signo
    PTR     Posicion del programa (24 bits sin signo)
    ID8     Identificador de sensor/led de 8 bits
    P8      Numero entero de 8 bits con signo (127 > P8 > -128)
    S8      Estado (8 bits sin signo)
'''

# Operaciones con datos 

MOV_R16_IMM16   = 0x01    # Mueve IMM16 a R16 
MOV_R16d_R16s   = 0x02    # Mueve R16s a R16d 
LOAD_R16_IMM16  = 0x03    # Mueve el contenido de IMM16 en memoria a R16 
LOAD_R16d_R16s  = 0x04    # Mueve el contenido de R16s en memoria a R16d 
STORE_IMM16_R16 = 0x05    # Mueve el contenido de R16 a IMM16 en memoria 
STORE_R16_IMM16 = 0x06    # Mueve IMM16 a R16 en memoria 
STORE_R16d_R16s = 0x07    # Mueve el contenido de R16s a R16d en memoria 

# Operaciones aritmeticas 

INC_R16         = 0x10    # Incrementa en uno el valor de R16 
DEC_R16         = 0x11    # Decrementa en uno el valor de R16 
ADD_R16_IMM16   = 0x12    # Suma IMM16 a R16 
ADD_R16d_R16s   = 0x13    # Suma R16s a R16d 
SUB_R16_IMM16   = 0x14    # Resta IMM16 a R16 
SUB_R16d_R16s   = 0x15    # Resta R16s a R16d 
MUL_R16_IMM16   = 0x16    # Multiplica R16 por IMM16 y lo guarda en R16 
MUL_R16d_R16s   = 0x17    # Multiplica R16s por R16d y lo guarda en R16d 
DIV_R16_IMM16   = 0x18    # Divide R16 por IMM16 y lo guarda en R16 
DIV_R16d_R16s   = 0x19    # Divide R16s por R16d y lo guarda en R16d 

# Saltos 

JMP_PTR             = 0x20    # Continua la ejecucion en PTR 
SKIPZ_R16           = 0x21    # Saltea la proxima instruccion si R16 es cero 
SKIPE_R16_IMM16     = 0x22    # Saltea la proxima instruccion si R16 es = IMM16 
SKIPE_R16d_R16s     = 0x23    # Saltea la proxima instruccion si R16s es = R16d 
SKIPNE_R16_IMM16    = 0x24    # Saltea la proxima instruccion si R16 es <> IMM16 
SKIPNE_R16d_R16s    = 0x25    # Saltea la proxima instruccion si R16s es <> R16d 
SKIPG_R16_IMM16     = 0x26    # Saltea la proxima instruccion si R16 es > IMM16 
SKIPG_R16d_R16s     = 0x27    # Saltea la proxima instruccion si R16s es > R16d 
SKIPL_R16_IMM16     = 0x28    # Saltea la proxima instruccion si R16 es < IMM16 
SKIPL_R16d_R16s     = 0x29    # Saltea la proxima instruccion si R16s es < R16d 
SKIPGE_R16_IMM16    = 0x2A    # Saltea la proxima instruccion si R16 es >= IMM16 
SKIPGE_R16d_R16s    = 0x2B    # Saltea la proxima instruccion si R16s es >= R16d 
SKIPLE_R16_IMM16    = 0x2C    # Saltea la proxima instruccion si R16 es <= IMM16 
SKIPLE_R16d_R16s    = 0x2D    # Saltea la proxima instruccion si R16s es <= R16d 

# Input/Output 

SENSE_R16_ID8       = 0x30    # Escribe el valor de ID8 en R16 
MOTOR_IMM8_P8_P8    = 0x31    # Prende los motores durante IMM8 cseg. Utiliza las potencias para los motores izquierdo y derecho 
MOTOR_IMM8_R8i_R8d  = 0x33
MOTOR_R8t_R8i_R8d   = 0x34
LED_ID8_ST8         = 0x32    # Pone al led ID8 en estado ST8 

# Interrupciones 

IRET    = 0x40    # Vuelve de la interrupcion y continua ejecutando la instruccion 
IRETN   = 0x41    # Vuelve de la interrupcion y continua ejecutando desde la proxima instruccion 

# Funciones 

CALL_PTR    = 0x50    # Continua la ejecucion a partir de PTR, guardando el contexto actual 
RET         = 0x51    # Continua la ejecucion usando el contexto anterior 

# Otras Operaciones 

NOP     = 0x90    # No operacion 
HALT    = 0x91    # Finaliza la ejecucion 