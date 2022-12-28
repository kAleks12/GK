#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

is_wall_one_visible = True
is_wall_two_visible = True
is_wall_three_visible = True
is_wall_four_visible = True

images = []
currIndex = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    load_textures()


def load_textures():
    images.append(Image.open("tekstura.tga"))
    images.append(Image.open("tosia.tga"))

    curr_image = images[0]
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, curr_image.size[0], curr_image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, curr_image.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    print_pyramid()
    glFlush()


def print_fixed_triangle():
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0.0, 5.0, 0.0)
    glEnd()


def print_fixed_rectangle():
    glBegin(GL_TRIANGLES)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5, -5, 0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(5, 5, 0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5, -5, 0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(5, 5, 0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5, 5, 0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5, -5, 0)
    glEnd()


def print_pyramid(x=0, y=0, z=0, length=5):
    print_triangle([x, y, z], [0.0, 0.0],
                   [x, y + length, z], [0.0, 1.0],
                   [x + length, y + length, z], [1.0, 1.0])

    print_triangle([x, y, z], [0.0, 0.0],
                   [x + length, y + length, z], [1.0, 1.0],
                   [x + length, y, z], [1.0, 0.0])

    if is_wall_one_visible:
        print_triangle([x, y, z], [0.0, 0.0],
                       [x + length, y, z], [1.0, 0.0],
                       [x + length / 2, y + length / 2, length / 2], [0.5, 0.5])

    if is_wall_two_visible:
        print_triangle([x + length, y, z], [1.0, 0.0],
                       [x + length, y + length, z], [1.0, 1.0],
                       [x + length / 2, y + length / 2, length / 2], [0.5, 0.5])

    if is_wall_three_visible:
        print_triangle([x + length, y + length, z], [1.0, 1.0],
                       [x, y + length, z], [0.0, 1.0],
                       [x + length / 2, y + length / 2, length / 2], [0.5, 0.5])

    if is_wall_four_visible:
        print_triangle([x, y, 0.0], [0.0, 0.0],
                       [x + length / 2, y + length / 2, length / 2], [0.5, 0.5],
                       [x, y + length, z], [0.0, 1.0])


def print_triangle(point_1, texture_point_1, point_2, texture_point_2, point_3, texture_point_3):
    glBegin(GL_TRIANGLES)
    glTexCoord2f(texture_point_1[0], texture_point_1[1])
    glVertex3f(point_1[0], point_1[1], point_1[2])

    glTexCoord2f(texture_point_2[0], texture_point_2[1])
    glVertex3f(point_2[0], point_2[1], point_2[2])

    glTexCoord2f(texture_point_3[0], texture_point_3[1])
    glVertex3f(point_3[0], point_3[1], point_3[2])
    glEnd()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

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
    global is_wall_one_visible
    global is_wall_two_visible
    global is_wall_three_visible
    global is_wall_four_visible
    global currIndex

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_F1 and action == GLFW_PRESS:
        is_wall_one_visible = not is_wall_one_visible
    if key == GLFW_KEY_F2 and action == GLFW_PRESS:
        is_wall_two_visible = not is_wall_two_visible
    if key == GLFW_KEY_F3 and action == GLFW_PRESS:
        is_wall_three_visible = not is_wall_three_visible
    if key == GLFW_KEY_F4 and action == GLFW_PRESS:
        is_wall_four_visible = not is_wall_four_visible

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        currIndex = (currIndex + 1) % len(images)
        curr_image = images[currIndex]

        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, curr_image.size[0], curr_image.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, curr_image.tobytes("raw", "RGB", 0, -1)
        )


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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
