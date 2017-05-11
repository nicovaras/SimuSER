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

import argparse
import sys
from os import path


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return path.dirname(unicode(sys.executable, encoding))
    return path.dirname(unicode(__file__, encoding))

def get_full_file_path(filename):
    this_file_pathname = module_path()
    #this_file_dirname = path.dirname(this_file_pathname)
    full_file_pathname = path.join(this_file_pathname, filename)
    return full_file_pathname

def get_args():
    reload(sys)  # to enable `setdefaultencoding` again
    #sys.stdout = open("simulador_stdout.log", "w")
    sys.setdefaultencoding("UTF-8")

    parser = argparse.ArgumentParser(description='Simulador del robot.')
    parser.add_argument('-in', dest='bin', nargs=1, help='Archivo binario de input')
    parser.add_argument('-back', dest='background', nargs=1, help='Archivo background (piso)')
    parser.add_argument('-boxes', dest='boxes', nargs=1, help='Archivo de matriz de cajas')
    parser.add_argument('-map', dest='map', nargs=1, help='Archivo de mapa (fondo + cajas)')
    parser.add_argument('-robot_file', dest='robot_file', nargs=1, help='Archivo de robots')
    return parser.parse_args()

args = get_args()

def get_setting(setting):
    config_file = open(get_full_file_path("config.txt"),'r')
    for line in config_file:
        setting_line = [x.strip() for x in line.strip().split("=")]
        if len(setting_line) > 1:
            if setting_line[0] == setting:
                config_file.close()
                return setting_line[1].strip()
    raise Exception("No se encontro " + setting + " en config.txt")

def get_robot_file():
    if args.robot_file:
        return args.robot_file[0]
    else:
        return None

def source_file():
    if args.bin:
        return args.bin[0]
    else:
        return get_setting("binario_fuente")

def background():
    if args.background:
        return args.background[0]
    else:
        return get_setting("fondo")

def box_matrix():
    if args.boxes:
        return args.boxes[0]
    else:
        return get_setting("matriz_de_cajas")

def map_file():
    if args.map:
        return args.map[0]
    else:
        return None



def draw_trace():
    return get_setting("dibujar_recorrido") == 'true'

def initial_position():
    return [int(x.strip()) for x in get_setting("posicion_inicial").split(",")]

def screen_size():
    return [int(x.strip()) for x in get_setting("size_pantalla").split(",")]

def clock_speed():
    return int(get_setting("velocidad_clock"))

def robot_speed():
    return float(get_setting("velocidad_robot"))

def motor_duration():
    return float(get_setting("constante_duracion_motor"))

def rotation_constant():
    return float(get_setting("constante_angulo_rotacion"))

def max_proximity():
    return int(get_setting("maxima_distancia_proximity"))

def draw_proximity():
    return get_setting("dibujar_linea_proximidad") == 'true'

def print_debug():
    return get_setting("print_debug") == 'true'

def header_size():
    return int(get_setting("header_size"))

def initial_angle():
    return float(get_setting("angulo_inicial"))

def color_left():
    return int(get_setting("color_left"))

def color_mid():
    return int(get_setting("color_mid"))

def color_right():
    return int(get_setting("color_right"))

def proximity_sensor():
    return int(get_setting("proximity_sensor"))