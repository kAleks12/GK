#!/usr/bin/env python3
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

colors = [[random.random(), random.random(), random.random()] for _ in range(3)]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # print_rectangle(0.0, 1.0, 30, 30, [0, 0, 0.5])
    # print_funny_rectangle(0.0, 0.0, 30, 30, 0.1)
    print_carpet(0, 0, 100, 100, 4)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def print_rectangle(origin_x, origin_y, width, height, color: [3]):
    glColor3f(color[0], color[1], color[2])

    glBegin(GL_TRIANGLES)
    glVertex2f(origin_x + width, origin_y + height)
    glVertex2f(origin_x + width, origin_y - height)
    glVertex2f(origin_x - width, origin_y - height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(origin_x - width, origin_y + height)
    glVertex2f(origin_x - width, origin_y - height)
    glVertex2f(origin_x + width, origin_y + height)
    glEnd()


def print_funny_rectangle(origin_x, origin_y, length_a, length_b, deformation):
    length_a = length_a * deformation
    length_b = length_b * deformation

    glBegin(GL_TRIANGLES)
    glColor3f(colors[0][0], colors[0][1], colors[0][2])
    glVertex2f(origin_x + length_a, origin_y + length_b)

    glColor3f(colors[1][0], colors[1][1], colors[1][2])
    glVertex2f(origin_x + length_a, origin_y - length_b)

    glColor3f(colors[2][0], colors[2][1], colors[2][2])
    glVertex2f(origin_x - length_a, origin_y - length_b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(colors[1][0], colors[1][1], colors[1][2])
    glVertex2f(origin_x - length_a, origin_y + length_b)

    glColor3f(colors[2][0], colors[2][1], colors[2][2])
    glVertex2f(origin_x - length_a, origin_y - length_b)

    glColor3f(colors[0][0], colors[0][1], colors[0][2])
    glVertex2f(origin_x + length_a, origin_y + length_b)
    glEnd()


def print_carpet(x, y, width, height, depth):
    print_rectangle(x, y, width, height, [1, 1, 1])
    # print_fancy_rectange(x, y, width, height, 1)
    print_carpet_part(x, y, width, height, depth)


def print_carpet_part(x, y, width, height, depth):
    print_rectangle(x, y, width / 3, height / 3, [0.5, 0.5, 0.5])

    if depth > 1:
        newWidth = width / 3
        newHeight = height / 3
        newDepth = depth - 1
        print_carpet_part(x - 2 * newWidth, y + 2 * newHeight, newWidth, newHeight, newDepth)
        print_carpet_part(x, y + 2 * newHeight, newWidth, newHeight, newDepth)
        print_carpet_part(x + 2 * newWidth, y + 2 * newHeight, newWidth, newHeight, newDepth)
        print_carpet_part(x + 2 * newWidth, y, newWidth, newHeight, newDepth)
        print_carpet_part(x + 2 * newWidth, y - 2 * newHeight, newWidth, newHeight, newDepth)
        print_carpet_part(x, y - 2 * newHeight, newWidth, newHeight, newDepth)
        print_carpet_part(x - 2 * newWidth, y - 2 * newHeight, newWidth, newHeight, newDepth)
        print_carpet_part(x - 2 * newWidth, y, newWidth, newHeight, newDepth)


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()