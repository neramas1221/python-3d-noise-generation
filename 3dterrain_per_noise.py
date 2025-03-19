import sys
import numpy as np
from noise import pnoise2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Terrain parameters
cols, rows = 100, 100
scl = 1
terrain = np.zeros((cols, rows))
move = 0

def map_value(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)

def generate_terrain():
    global move
    move += 0.1
    yoff = move
    for y in range(rows):
        xoff = 0
        for x in range(cols):
            terrain[x][y] = map_value(pnoise2(xoff, yoff), 0, 1, -5, 5)
            xoff += 0.2
        yoff += 0.2

def init_gl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    # gluLookAt(50, -30, 50, 50, 50, 0, 0, 0, 1)


def draw_terrain():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(50, 30, 75, 50, 50, 0, 0, 0, 1)
    # gluLookAt(25, 15, 25, 25, 25, 0, 0, 0, 1)
    generate_terrain()
    glColor3f(0.5, 0.5, 0.0)
    glBegin(GL_LINES)
    for y in range(rows - 1):
        for x in range(cols):
            x1, y1, z1 = x * scl, y * scl, terrain[x][y]
            x2, y2, z2 = x * scl, (y + 1) * scl, terrain[x][y + 1]
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
    glEnd()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL Terrain Visualization")
    glutDisplayFunc(draw_terrain)
    glutIdleFunc(draw_terrain)
    init_gl()
    glutMainLoop()

if __name__ == "__main__":
    main()
