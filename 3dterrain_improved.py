import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from noise import pnoise2


def map_value(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min

    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)


def generate_terrain(width, height):
    terrain = np.zeros((width, height))
    scale = 3
    global move
    move -= 0.5
    yoff = move
    for x in range(width):
        xoff = 0
        for y in range(height):
            terrain[x][y] = map_value(pnoise2(xoff / scale, yoff / scale), 0, 1, -5, 5)
            xoff += 0.2
        yoff += 0.2
    return terrain


def draw_terrain():
    global terrain
    terrain = generate_terrain(width, height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for x in range(len(terrain) -1):
        for y in range(len(terrain[x]) -1):
            glColor3f(0.6, 0.6, 0.6)
            glVertex3f(x, terrain[x][y], y)
            glVertex3f(x + 1, terrain[x + 1][y], y)
            glVertex3f(x, terrain[x][y + 1], y + 1)
            glVertex3f(x + 1, terrain[x + 1][y + 1], y + 1)
            glVertex3f(x + 1, terrain[x + 1][y], y)
            glVertex3f(x + 1, terrain[x + 1][y + 1], y + 1)
    glEnd()
    glutSwapBuffers()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    # Camera persision
    gluLookAt(50, 20, 80, 50, 0, 50, 0, 1, 0)


def idle():
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Terrain Visulization")
    init()
    glutDisplayFunc(draw_terrain)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutMainLoop()


width, height = 200, 200
move = 1000
terrain = generate_terrain(width, height)

if __name__ == "__main__":
    main()