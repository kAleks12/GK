# !/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 20.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

r = 12.0

theta_light = 0.0
phi_light = 0.0

light_index = 0
color = 0
attr_type = 0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.5, 0.5, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 15.0, 1.0]

light_ambient_2 = [0.0, 0.0, 0.0, 1.0]
light_diffuse_2 = [0.0, 0.0, 0.0, 1.0]
light_specular_2 = [1.0, 1.0, 1.0, 1.0]
light_position_2 = [0.0, 0.0, -15.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

light_source = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def light_1():
    light_position[0] = math.cos(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * r
    light_position[1] = math.sin(phi_light * math.pi / 180) * r
    light_position[2] = math.sin(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * r

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)


def light_2():
    light_position_2[0] = -math.cos(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * r
    light_position_2[1] = -math.sin(phi_light * math.pi / 180) * r
    light_position_2[2] = -math.sin(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * r

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_2)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_2)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)


def print_light(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 1.0, 10, 10)
    gluDeleteQuadric(quadric)
    glPopMatrix()


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global theta_light
    global phi_light

    check_colors(light_ambient_2)
    check_colors(light_diffuse_2)
    check_colors(light_diffuse)
    check_colors(light_diffuse)

    light_1()
    light_2()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        theta_light += delta_x * pix2angle
        phi_light += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    print_light(light_position[0], light_position[1], light_position[2])
    print_light(light_position_2[0], light_position_2[1], light_position_2[2])

    glFlush()


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
    global color
    global attr_type
    global light_source

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    # switching lights
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        light_source = (light_source + 1) % 2
        print("LIGHT ", light_source, "selected")

    # switching attributes
    if key == GLFW_KEY_T and action == GLFW_PRESS:
        attr_type = (attr_type + 1) % 2

        if type == 0:
            print("Now changing ambient attr")
        else:
            print("Now changing diffuse attr")

    # red color
    if key == GLFW_KEY_R and action == GLFW_PRESS:
        color = 0
        print("Now changing red element")

    # green color
    if key == GLFW_KEY_G and action == GLFW_PRESS:
        color = 1
        print("Now changing green element")

    # blue color
    if key == GLFW_KEY_B and action == GLFW_PRESS:
        color = 2
        print("Now changing blue element")

    if key == GLFW_KEY_INSERT and action == GLFW_PRESS:
        if light_source == 0:
            if attr_type == 0:
                light_ambient[color] += 0.1
            else:
                light_diffuse[color] += 0.1
        else:
            if attr_type == 0:
                light_ambient_2[color] += 0.1
            else:
                light_diffuse_2[color] += 0.1
        print("Incremented!")

    if key == GLFW_KEY_DELETE and action == GLFW_PRESS:
        if light_source == 0:
            if attr_type == 0:
                light_ambient[color] -= 0.1
            else:
                light_diffuse[color] -= 0.1
        else:
            if attr_type == 0:
                light_ambient_2[color] -= 0.1
            else:
                light_diffuse_2[color] -= 0.1

        print("Decremented!")

    if key == GLFW_KEY_I and action == GLFW_PRESS:
        if light_source == 0:
            print("Selected LIGHT 0")
            print(f'Ambient -> R: {light_ambient[0]} G: {light_ambient[1]} B: {light_ambient[2]} ', end='')
            print(f'| Diffuse R: {light_diffuse[0]} G: {light_diffuse[1]} B: {light_diffuse[2]}')
        else:
            print("Selected LIGHT 1")
            print(f'Ambient -> R: {light_ambient_2[0]} G: {light_ambient_2[1]} B: {light_ambient_2[2]} ', end='')
            print(f'| Diffuse R: {light_diffuse_2[0]} G: {light_diffuse_2[1]} B: {light_diffuse_2[2]}')


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

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


def check_colors(array: list):
    if array[0] < 0:
        array[0] = 0
    if array[1] < 0:
        array[1] = 0
    if array[2] < 0:
        array[2] = 0
    if array[0] > 1:
        array[0] = 1
    if array[1] > 1:
        array[1] = 1
    if array[2] > 1:
        array[2] = 1


if __name__ == '__main__':
    main()
