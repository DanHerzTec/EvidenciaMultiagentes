# src/textures.py

import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *  # Si lo requieres
from OpenGL.GLU import *

# Arreglo global para almacenar los IDs de textura en OpenGL
textures = []

def init_textures(file_list):
    """
    Carga cada archivo en 'file_list' como una textura y lo guarda en 'textures'.
    Retorna la lista de IDs de textura (aunque 'textures' ya lo hace globalmente).
    """
    global textures
    for path in file_list:
        tex_id = load_texture(path)
        textures.append(tex_id)
    return textures

def load_texture(filepath):
    """
    Carga un archivo de imagen (bmp, png, etc.) con Pygame,
    crea y configura una textura OpenGL, y retorna su ID.
    """
    # Genera un ID de textura
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Ajusta parámetros de la textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # Carga la imagen con pygame
    image = pygame.image.load(filepath).convert_alpha()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA", 1)

    # Subirla como textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    # Desvincular la textura
    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id
