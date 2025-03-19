import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from noise import pnoise2

# Function to generate terrain heightmap using Perlin noise
def generate_terrain(width, height, scale, offset, amplitude):
    terrain = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            terrain[x][y] = pnoise2(x / scale, (y + offset) / scale) * amplitude
    return terrain

# Initialize variables
width, height = 200, 200
scale = 10
offset = 1000
amplitude = 5  # Adjust this value to change the height of the hills
terrain = generate_terrain(width, height, scale, offset, amplitude)

# Update the draw_terrain function to pass the amplitude parameter
def draw_terrain():
    global offset, terrain
    offset -= 0.1  # Update the offset for movement
    terrain = generate_terrain(width, height, scale, offset, amplitude)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for x in range(len(terrain) - 1):
        for y in range(len(terrain[x]) - 1):
            glColor3f(0.6, 0.6, 0.6)  # Set color to light gray
            glVertex3f(x, terrain[x][y], y)
            glVertex3f(x + 1, terrain[x + 1][y], y)
            glVertex3f(x, terrain[x][y + 1], y + 1)
            glVertex3f(x + 1, terrain[x + 1][y + 1], y + 1)
            glVertex3f(x + 1, terrain[x + 1][y], y)
            glVertex3f(x + 1, terrain[x + 1][y + 1], y + 1)
    glEnd()
    glutSwapBuffers()

# Function to initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glEnable(GL_DEPTH_TEST)  # Enable depth testing


# Reshape function to handle window resizing
def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Move the camera closer to the landscape
    # Adjust the eye position (x, y, z) to make it look like the camera is flying over the terrain
    gluLookAt(50, 20, 80, 50, 0, 50, 0, 1, 0)  # Adjust these values


# Idle function to update and redraw terrain
def idle():
    glutPostRedisplay()  # Trigger redraw

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Terrain Visualization")  # Explicitly use a byte string
    init()
    glutDisplayFunc(draw_terrain)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)  # Set the idle function
    glutMainLoop()

if __name__ == "__main__":
    main()
