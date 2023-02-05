from inspect import signature
from itertools import count
from math import cos, sin
from msilib.schema import Signature
from turtle import TNavigator, distance
import pyxel
class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self,dx,dy):
        self.x=(self.x+dx)
        self.y=(self.y+dy)
    def draw(self):
        pyxel.circ(self.x,self.y,2,7)
class Enemy:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def draw(self):
        pyxel.rect(self.x,self.y, 2, 2,7)
class App:
    def __init__(self):
        pyxel.init(200, 150)
        pyxel.cls(0)
        self.player = Player(100,100)
        self.enemy = Enemy(170,40)
        pyxel.run(self.draw, self.update)
    def update(self):
        if pyxel.btn(pyxel.KEY_2):
             self.player.update(1,1)
        if pyxel.btn(pyxel.KEY_1):
             self.player.update(-1,1)
        if pyxel.btn(pyxel.KEY_5):
             self.player.update(1,-1)
        if pyxel.btn(pyxel.KEY_4):
             self.player.update(-1,-1)
        
    def draw(self):
        self.player.draw()
        self.enemy.draw()
App()