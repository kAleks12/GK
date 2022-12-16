#!/usr/bin/env python3
import sys
from math import cos, pi, sin

from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *

viewer = [0.0, 0.0, 10.0]

pix2angle_h = 1.0
pix2angle_w = 1.0
pix2scale = 1.0

theta = 0.0
phi = 0.0
camera_default_scale = 10
camera_scale = camera_default_scale

model_default_scale = 1.0
model_scale = model_default_scale

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

mouse_x_pos_old = 0
mouse_y_pos_old = 0

delta_x = 0
delta_y = 0

mode = 1


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


# drawing functions
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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta, phi
    global model_scale, camera_scale
    global viewer

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if camera_scale < 0.05:
        camera_scale = 0.05
    if camera_scale > 50:
        camera_scale = 50

    if model_scale < 0.05:
        model_scale = 0.05
    if model_scale > 5:
        model_scale = 5

    if mode == 1:
        viewer[0] = camera_scale * cos(theta * (pi / 180)) * cos(phi * (pi / 180))
        viewer[1] = camera_scale * sin(phi * (pi / 180))
        viewer[2] = camera_scale * sin(theta * (pi / 180)) * cos(phi * (pi / 180))

        if 90 < abs(phi) < 270:
            gluLookAt(viewer[0], viewer[1], viewer[2],
                      0.0, 0.0, 0.0,
                      0.0, -1.0, 0.0)
        else:
            gluLookAt(viewer[0], viewer[1], viewer[2],
                      0.0, 0.0, 0.0,
                      0.0, 1.0, 0.0)
    else:
        viewer = [0, 0, 10]
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
        glScalef(model_scale, model_scale, model_scale)

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle_h, pix2angle_w
    global pix2scale

    pix2angle_w = 360.0 / width
    pix2angle_h = 360.0 / height
    pix2scale = 10 / height

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global model_scale, camera_scale, mode

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_R and action == GLFW_PRESS:
        model_scale = model_default_scale
        camera_scale = camera_default_scale

    if key == GLFW_KEY_M and action == GLFW_PRESS:
        mode = -mode


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old
    global theta, phi
    global model_scale, camera_scale

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

    print(phi)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle_w
        phi += delta_y * pix2angle_h

    if right_mouse_button_pressed:
        if mode == 1:
            camera_scale += delta_y * pix2scale
        else:
            model_scale -= delta_y * pix2scale


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
