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
from pygame.locals import *
from pgu import gui
import pickle

class Editor(gui.Widget):
    def __init__(self,**params):
        gui.Widget.__init__(self,**params)
        self.back_name = "../simulador/background/back1.jpg"
        self.back = pygame.image.load(self.back_name)
        self.box = pygame.image.load("../simulador/img/box.png")
        self.box_matrix = [[0]*25 for x in range(19)]
        self.repaint()


    def event(self,e):
        if e.type == gui.MOUSEMOTION:
            x,y = e.pos
            if x< 0 or y < 0 or x >= 800 or y>600: 
                return
            if e.buttons[0]:
                self.box_matrix[y/32][x/32] = 1

            if e.buttons[2]:
                self.box_matrix[y/32][x/32] = 0
            self.repaint()

    def paint(self,s):
        overlay = pygame.Surface((800,600))
        overlay.blit(self.back,(0,0))
        for row in range(len(self.box_matrix)):
            for col in range(len(self.box_matrix[row])):
                if self.box_matrix[row][col] == 1:
                    overlay.blit(self.box, (col*32, row*32))
        
        s.blit(overlay,(0,0))

class App(gui.Desktop):
    def __init__(self,**params):
        gui.Desktop.__init__(self,**params)
        
        self.connect(gui.QUIT,self.quit,None)
        
        c = gui.Container(width=1000,height=600)
       
        self.fname = None
        
        self.open_d = gui.FileDialog()
        self.open_d.connect(gui.CHANGE, self.action_open, self.open_d)
        self.save_d = gui.FileDialog()
        self.save_d.connect(gui.CHANGE,self.action_save_close,self.save_d)
        
        menus = gui.Menus([
            ('Archivo/Nuevo',self.action_new,None),
            ('Archivo/Abrir',self.open_d.open,None),
            ('Archivo/Guardar',self.action_save,self.fname),
            ('Archivo/Guardar como...',self.save_d.open,None),
            ('Archivo/Salir',self.quit,None)
  
            ])
        c.add(menus,0,0)
        menus.rect.w,menus.rect.h = menus.resize()
        
        change_b = gui.Button("Cambiar Fondo")
        change_b.connect(gui.CLICK,self.action_open_background,None)
        c.add(change_b,0,100)


        self.editor = Editor(width=800,height=600,style={'border':1})
        
        c.add(self.editor, 200, 0)
        self.editor.resize()
        self.widget = c

    def action_new(self,dlg):
        self.fname = None
        self.editor.box_matrix = [[0]*25 for x in range(19)]
        self.editor.repaint()


    def action_save(self,name):
        if self.fname == None:
            self.save_d.open()
            return
        if self.fname[-1] == '/' or self.fname[-1] == '\\':
            self.fname += "sin_nombre"
        if self.fname.split(".")[-1] != "map":
            self.fname += ".map"
        back_string = pygame.image.tostring(self.editor.back, "RGB")
        pickle.dump( [self.editor.box_matrix, back_string, self.editor.back.get_size()], open( self.fname, "wb" ))
    
    def action_save_close(self,dlg):
        if dlg.value: 
            self.fname = dlg.value
            self.action_save(self.fname)

    def action_open(self,dlg):
        if dlg.value: 
            if not dlg.value.split(".")[-1] != ".map":
                return
            self.fname = dlg.value
            self.editor.box_matrix, img_str, size =  pickle.load( open( self.fname, "rb" ) )
            
            self.editor.back = pygame.image.fromstring(img_str, size, "RGB")
            
            self.editor.repaint()

    def action_open_background(self,dlg):
        self.change_dialog = gui.FileDialog()
        self.change_dialog.connect(gui.CHANGE,self.action_open_background_d,self.change_dialog)
        self.change_dialog.open()

    def action_open_background_d(self,dlg):
        img_formats = ["jpg", "jpeg", "png", "tif", "tiff", "bmp", "tga", "gif"]
        if dlg.value: 
            if not dlg.value.split(".")[-1] in img_formats:
                return
            self.editor.back = pygame.image.load(dlg.value)
            self.editor.repaint()

        
        
app = App()
app.run()
