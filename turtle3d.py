from vpython import *
import math

class Turtle3D:
    def __init__(self):
        self.visible = True
        self.position = vector(0, 0, 0)
        self.head = vector(0, 0, 0)
        self.rgb = vector(1, 0, 0)
        self.alpha = 0
        self.beta = 0
        scene.height = scene.width = 1000
    
    def color(self, red, green, blue):
        self.rgb = vector(red, green, blue) / 255
    
    def up(self, rotation):
        self.beta = (self.beta + rotation) % 360

    def down(self, rotation):
        self.beta = (self.beta - rotation) % 360

    def left(self, rotation):
        self.alpha = (self.alpha + rotation) % 360

    def right(self, rotation):
        self.alpha = (self.alpha - rotation) % 360
    
    def forward(self, size):
        self.head = computeHead(math.radians(self.alpha), math.radians(self.beta), size)
        if self.visible:
            cylinder(pos=self.position, axis=self.head, radius=0.1, color=self.rgb)
        self.position = self.position + self.head

    def backward(self, size):
        # TODO: implement
        pass

    def hide(self):
        self.visible = False
    
    def show(self):
        self.visible = True
    
    def home(self):
        self.position = vector(0, 0, 0)

def computeHead(alpha, beta, size):
    headX = math.cos(alpha) * math.cos(beta) * size
    headY = math.sin(beta) * size
    headZ = math.sin(alpha) * math.cos(beta) * size
    return vector(headX, headY, headZ)
