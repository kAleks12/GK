#!/usr/bin/env python3
import math
import sys
import random

from glfw.GLFW import *
from OpenGL.GL import *


n = 20
colors = [[[random.random(), random.random(), random.random()] for _ in range(n)] for _ in range(n)]


def print_egg_points():
    points = calculate_egg_points()

    for i in range(n):
        for j in range(n):
            glColor3f(1, 1, 1)
            glBegin(GL_POINTS)

            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])

            glEnd()


def print_egg_lines():
    points = calculate_egg_points()

    for i in range(n):
        for j in range(n):
            if i == n - 1:
                next_i = 0
            else:
                next_i = i + 1

            if j == n - 1:
                next_j = 0
            else:
                next_j = j + 1

            glColor3f(1, 1, 1)
            glBegin(GL_LINES)

            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glVertex3f(points[next_i][j][0], points[next_i][j][1], points[next_i][j][2])

            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glVertex3f(points[i][next_j][0], points[i][next_j][1], points[i][next_j][2])

            glEnd()


def print_egg_triangles():
    points = calculate_egg_points()

    for i in range(n - 1):
        for j in range(n - 1):
            glBegin(GL_TRIANGLES)

            # drawing first triangle
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])

            glColor3f(colors[i + 1][j][0], colors[i + 1][j][1], colors[i + 1][j][2])
            glVertex3f(points[i + 1][j][0], points[i + 1][j][1], points[i + 1][j][2])

            glColor3f(colors[i][j + 1][0], colors[i][j + 1][1], colors[i][j + 1][2])
            glVertex3f(points[i][j + 1][0], points[i][j + 1][1], points[i][j + 1][2])

            # drawing sub triangle
            glColor3f(colors[i + 1][j + 1][0], colors[i + 1][j + 1][1], colors[i + 1][j + 1][2])
            glVertex3f(points[i + 1][j + 1][0], points[i + 1][j + 1][1], points[i + 1][j + 1][2])

            glColor3f(colors[i + 1][j][0], colors[i + 1][j][1], colors[i + 1][j][2])
            glVertex3f(points[i + 1][j][0], points[i + 1][j][1], points[i + 1][j][2])

            glColor3f(colors[i][j + 1][0], colors[i][j + 1][1], colors[i][j + 1][2])
            glVertex3f(points[i][j + 1][0], points[i][j + 1][1], points[i][j + 1][2])

            glEnd()


def print_egg_triangle_strips():
    points = calculate_egg_points()

    for i in range(n - 1):
        glBegin(GL_TRIANGLE_STRIP)

        # draw initial vertex
        glColor3f(1, 1, 1)
        glVertex3f(points[i][0][0], points[i][0][1], points[i][0][2])

        glColor3f(1, 1, 1)
        glVertex3f(points[i + 1][0][0], points[i + 1][0][1], points[i + 1][0][2])

        glColor3f(colors[i][1][0], colors[i][1][1], colors[i][1][2])
        glVertex3f(points[i][1][0], points[i][1][1], points[i][1][2])

        for j in range(1, n):
            # drawing next triangle vertex
            if j % 2 == 1:
                glColor3f(colors[i + 1][j][0], colors[i + 1][j][1], colors[i + 1][j][2])
                glVertex3f(points[i + 1][j][0], points[i + 1][j][1], points[i + 1][j][2])
            else:
                glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
                glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])

        # draw last missing triangle vertex
        glColor3f(1, 1, 1)
        glVertex3f(points[i][n - 1][0], points[i][n - 1][1], points[i][n - 1][2])

        glEnd()


def calculate_egg_points():
    points = [[[0.0] * 3 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        u = 1 / (n - 1) * i
        for j in range(n):
            v = 1 / (n - 1) * j

            points[i][j][1] = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            points[i][j][0] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) \
                              * math.cos(math.pi * v)
            points[i][j][2] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) \
                              * math.sin(math.pi * v)

    return points


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / math.pi)
    axes()

    # print_egg_points()
    # print_egg_lines()
    # print_egg_triangles()
    print_egg_triangle_strips()
    glFlush()


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
