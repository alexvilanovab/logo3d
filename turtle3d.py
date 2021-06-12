from vpython import *
import math


class Turtle3D:
    '''Crea escenes 3D mitjançant gràfics tortuga tridimensionals.

    Parametres:
        - strokeColor (float, float, float): color del pinzell, espai rgb amb valors entre 0 i 1. (1, 0, 0) per defecte.
        - strokeWeight (float): tamany del pinzell. 0.1 per defecte.
        - backgroundColor (float, float, float): color de la finestra, espai rgb amb valors entre 0 i 1. (0, 0, 0) per defecte.
        - windowHeight (int): alçada de la finestra de l'escena en píxels. 1000 per defecte.
        - windowWidth (int): amplada de la finestra de l'escena en píxels. 1000 per defecte.
    '''
    def __init__(self,
                 strokeColor=(1, 0, 0),
                 strokeWeight=0.1,
                 backgroundColor=(0, 0, 0),
                 windowHeight=1000,
                 windowWidth=1000):
        self.visible = True
        self.position = vector(0, 0, 0)
        self.head = vector(0, 0, 0)
        self.alpha = 0
        self.beta = 0
        self.strokeColor = vector(*strokeColor)
        self.strokeWeight = strokeWeight
        scene.background = vector(*backgroundColor)
        scene.height = windowHeight
        scene.width = windowWidth

    def color(self, red, green, blue):
        '''Canvia el color del pinzell de la tortuga.

        Parametres:
            - red (int): quantitat de color vermell, entre 0 i 1
            - green (int): quantitat de color verd, entre 0 i 1
            - blue (int): quantitat de color blau, entre 0 i 1
        '''
        self.strokeColor = vector(red, green, blue)

    def up(self, rotation):
        '''Rota l'angle vertical del cap de la tortuga cap amunt.

        Parametres:
            - rotation (int): angle de rotació en graus sexagesimals.
        '''
        self.beta = (self.beta + rotation) % 360

    def down(self, rotation):
        '''Rota l'angle vertical del cap de la tortuga cap avall.

        Parametres:
            - rotation (int): angle de rotació en graus sexagesimals.
        '''
        self.beta = (self.beta - rotation) % 360

    def left(self, rotation):
        '''Rota l'angle horitzontal del cap de la tortuga cap a l'esquerra.

        Parametres:
            - rotation (int): angle de rotació en graus sexagesimals.
        '''
        self.alpha = (self.alpha + rotation) % 360

    def right(self, rotation):
        '''Rota l'angle horitzontal del cap de la tortuga cap a la dreta.

        Parametres:
            - rotation (int): angle de rotació en graus sexagesimals.
        '''
        self.alpha = (self.alpha - rotation) % 360

    def forward(self, size):
        '''Mou la tortuga endavant i pinta en cas d'estar visible.

        Parametres:
            - size (int): longitud del desplaçament.
        '''
        self.head = self.__computeHead(size)
        if self.visible:
            self.__draw()
        self.position = self.position + self.head

    def backward(self, size):
        '''Mou la tortuga endarrere i pinta en cas d'estar visible.

        Parametres:
            - size (int): longitud del desplaçament.
        '''
        self.head = self.__computeHead(size) * -1
        if self.visible:
            self.__draw()
        self.position = self.position + self.head

    def hide(self):
        '''Desactiva la tortuga, fa que no pinti al fer forward o backward.
        '''
        self.visible = False

    def show(self):
        '''Activa la tortuga, fa que pinti al fer forward o backward.
        '''
        self.visible = True

    def home(self):
        '''Mou la tortuga a les coordenades inicials (0, 0, 0).
        '''
        self.position = vector(0, 0, 0)

    def __computeHead(self, size):
        alpha = math.radians(self.alpha)
        beta = math.radians(self.beta)
        headX = math.cos(alpha) * math.cos(beta) * size
        headY = math.sin(beta) * size
        headZ = math.sin(alpha) * math.cos(beta) * size
        return vector(headX, headY, headZ)

    def __draw(self):
        cylinder(pos=self.position, axis=self.head, radius=self.strokeWeight, color=self.strokeColor)
        sphere(pos=self.position, radius=self.strokeWeight, color=self.strokeColor)
