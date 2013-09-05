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
    
    V16     Celda de variables de 16 bits (hay 256 celdas)
    IMM8    Numero entero de 8 bits sin signo
    IMM16   Numero entero de 16 bits sin signo
    PTR     Posicion del programa (24 bits sin signo)
    ID8     Identificador de sensor/led de 8 bits
    P8      Numero entero de 8 bits con signo (127 > P8 > -128)
    S8      Estado (8 bits sin signo)
'''

# Operaciones con datos 

MOV_V16_IMM16   = 0x01    # Mueve IMM16 a V16 
MOV_V16d_V16s   = 0x02    # Mueve V16s a V16d 
LOAD_V16_IMM16  = 0x03    # Mueve el contenido de IMM16 en memoria a V16 
LOAD_V16d_V16s  = 0x04    # Mueve el contenido de V16s en memoria a V16d 
STORE_IMM16_V16 = 0x05    # Mueve el contenido de V16 a IMM16 en memoria 
STORE_V16_IMM16 = 0x06    # Mueve IMM16 a V16 en memoria 
STORE_V16d_V16s = 0x07    # Mueve el contenido de V16s a V16d en memoria 

# Operaciones aritmeticas 

INC_V16         = 0x10    # Incrementa en uno el valor de V16 
DEC_V16         = 0x11    # Decrementa en uno el valor de V16 
ADD_V16_IMM16   = 0x12    # Suma IMM16 a V16 
ADD_V16d_V16s   = 0x13    # Suma V16s a V16d 
SUB_V16_IMM16   = 0x14    # Resta IMM16 a V16 
SUB_V16d_V16s   = 0x15    # Resta V16s a V16d 
MUL_V16_IMM16   = 0x16    # Multiplica V16 por IMM16 y lo guarda en V16 
MUL_V16d_V16s   = 0x17    # Multiplica V16s por V16d y lo guarda en V16d 
DIV_V16_IMM16   = 0x18    # Divide V16 por IMM16 y lo guarda en V16 
DIV_V16d_V16s   = 0x19    # Divide V16s por V16d y lo guarda en V16d 

# Saltos 

JMP_PTR             = 0x20    # Continua la ejecucion en PTR 
SKIPZ_V16           = 0x21    # Saltea la proxima instruccion si V16 es cero 
SKIPE_V16_IMM16     = 0x22    # Saltea la proxima instruccion si V16 es = IMM16 
SKIPE_V16d_V16s     = 0x23    # Saltea la proxima instruccion si V16s es = V16d 
SKIPNE_V16_IMM16    = 0x24    # Saltea la proxima instruccion si V16 es <> IMM16 
SKIPNE_V16d_V16s    = 0x25    # Saltea la proxima instruccion si V16s es <> V16d 
SKIPG_V16_IMM16     = 0x26    # Saltea la proxima instruccion si V16 es > IMM16 
SKIPG_V16d_V16s     = 0x27    # Saltea la proxima instruccion si V16s es > V16d 
SKIPL_V16_IMM16     = 0x28    # Saltea la proxima instruccion si V16 es < IMM16 
SKIPL_V16d_V16s     = 0x29    # Saltea la proxima instruccion si V16s es < V16d 
SKIPGE_V16_IMM16    = 0x2A    # Saltea la proxima instruccion si V16 es >= IMM16 
SKIPGE_V16d_V16s    = 0x2B    # Saltea la proxima instruccion si V16s es >= V16d 
SKIPLE_V16_IMM16    = 0x2C    # Saltea la proxima instruccion si V16 es <= IMM16 
SKIPLE_V16d_V16s    = 0x2D    # Saltea la proxima instruccion si V16s es <= V16d 

# Input/Output 

SENSE_V16_ID8       = 0x30    # Escribe el valor de ID8 en V16 
MOTOR_IMM8_P8_P8    = 0x31    # Prende los motores durante IMM8 cseg. Utiliza las potencias para los motores izquierdo y derecho 
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