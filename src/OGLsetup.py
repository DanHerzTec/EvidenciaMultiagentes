# src/OGLsetup.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FOVY, ZNEAR, ZFAR,
    EYE_X, EYE_Y, EYE_Z,
    CENTER_X, CENTER_Y, CENTER_Z,
    UP_X, UP_Y, UP_Z,
    DIM_BOARD, CAMERA_SPEED,
    TEXTURE_FILES
)
from src.textures.textures import init_textures, textures

# Variables de cámara que modificaremos (inicializadas con los valores de constants)
eye_x = EYE_X
eye_y = EYE_Y
eye_z = EYE_Z

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # Eje X (rojo)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(-500, 0, 0)
    glVertex3f( 500, 0, 0)
    glEnd()
    # Eje Y (verde)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, -500, 0)
    glVertex3f(0,  500, 0)
    glEnd()
    # Eje Z (azul)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, -500)
    glVertex3f(0, 0,  500)
    glEnd()
    glLineWidth(1.0)

def Init():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Ejemplo organizado")

    # Proyección en perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, SCREEN_WIDTH / SCREEN_HEIGHT, ZNEAR, ZFAR)

    # Vista/cámara
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    # Configuración general de OpenGL
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Habilitar texturas 2D
    glEnable(GL_TEXTURE_2D)

    # Inicializar texturas (p.ej. “textura1.bmp”, etc.)
    init_textures(TEXTURE_FILES)

def PlanoTexturizado():
    """
    Dibuja el plano con la textura[0] (si existe),
    usando DIM_BOARD para definir el tamaño.
    """
    if len(textures) == 0:
        # En caso de no haber texturas cargadas, dibujar un color simple
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(-DIM_BOARD, 0, -DIM_BOARD)
        glVertex3f(-DIM_BOARD, 0,  DIM_BOARD)
        glVertex3f( DIM_BOARD, 0,  DIM_BOARD)
        glVertex3f( DIM_BOARD, 0, -DIM_BOARD)
        glEnd()
        return

    # Usar la primera textura como “pasto”, por ejemplo
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glColor3f(1.0, 1.0, 1.0)  # para no teñir la textura

    glBegin(GL_QUADS)
    # Asignar coords de textura (u,v) y coords de vértice (x,y,z)
    glTexCoord2f(0.0, 0.0); glVertex3f(-DIM_BOARD, 0, -DIM_BOARD)
    glTexCoord2f(0.0, 1.0); glVertex3f(-DIM_BOARD, 0,  DIM_BOARD)
    glTexCoord2f(1.0, 1.0); glVertex3f( DIM_BOARD, 0,  DIM_BOARD)
    glTexCoord2f(1.0, 0.0); glVertex3f( DIM_BOARD, 0, -DIM_BOARD)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)
    
def draw_sky():
    """Dibuja un fondo azul grande detrás de la escena"""
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-500, -500, -500)  # Esquina inferior izquierda extendida
    glTexCoord2f(0.0, 1.0); glVertex3f(500, -500, -500)   # Esquina inferior derecha extendida
    glTexCoord2f(1.0, 1.0); glVertex3f(500, 500, -500)    # Esquina superior derecha
    glTexCoord2f(1.0, 0.0); glVertex3f(-500, 500, -500)   # Esquina superior izquierda
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Ejes de referencia
    draw_sky()
    Axis()
    # Dibuja el plano con textura
    PlanoTexturizado()
    

def run():
    global eye_x, eye_y, eye_z

    done = False
    Init()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Teclas para mover la cámara
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            eye_z -= CAMERA_SPEED
        if keys[pygame.K_s]:
            eye_z += CAMERA_SPEED
        if keys[pygame.K_a]:
            eye_x -= CAMERA_SPEED
        if keys[pygame.K_d]:
            eye_x += CAMERA_SPEED
        if keys[pygame.K_q]:
            eye_y += CAMERA_SPEED
        if keys[pygame.K_e]:
            eye_y -= CAMERA_SPEED

        # Actualizar la cámara
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_x, eye_y, eye_z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

        display()
        pygame.display.flip()
        pygame.time.wait(5)

    pygame.quit()
    print("Posición final de la cámara:", eye_x, eye_y, eye_z)
