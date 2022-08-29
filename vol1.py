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
class Enemy:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self):
        pyxel.rect(self.x,self.y, 2, 2,7)
class App:
    def __init__(self):
        pyxel.init(200, 150)
        pyxel.cls(0)
        self.enemy = Enemy(170,40)
        pyxel.run(self.update, self.draw)
    def update(self):
        if pyxel.btn(pyxel.KEY2):
            dx=1
            dy=1
        if pyxel.btn(pyxel.KEY1):
            dx=-1
            dy=1
        if pyxel.btn(pyxel.KEY5):
            dx=1
            dy=-1
        if pyxel.btn(pyxel.KEY4):
            dx=-1
            dy=-1
        self.enemy.update(dx,dy)
    def draw(self):
        pass
App()