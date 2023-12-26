import pygame as pg
from math import *
from classes.Renderer import Renderer

pg.init()
pg.font.init()

w = 1024
h = 720

screen = pg.display.set_mode((w,h))
pg.display.set_caption("3d renderer")
pg.display.set_icon(pg.surface.Surface((0,0)))

font = pg.font.SysFont('None', 24)
focalLen = 500
speed = 1.2

camPos = pg.Vector3(0,0,4)
roty = 0
rotx = 0

camLock = True
pg.mouse.set_visible(not camLock)
pg.event.set_grab(camLock)

pressedKeys = pg.key.get_pressed()
def getKeyDown(keyCode):
    return pressedKeys[keyCode]

def rotateY(point: pg.Vector3, roty):
    return pg.Vector3(point.x*cos(roty) - point.z*sin(roty), point.y, point.x*sin(roty) + point.z*cos(roty))

renderer = Renderer(w,h)

dt = 0.01
clock = pg.time.Clock()
mainLoop = True
while mainLoop:

    screen.fill((230,230,230))
    md = pg.mouse.get_rel()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            mainLoop = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                camLock = not camLock
                pg.mouse.set_visible(not camLock)
                pg.event.set_grab(camLock)
                md = (0,0)
            if event.key == pg.K_1:
                renderer.renderMode = 1
            if event.key == pg.K_2:
                renderer.renderMode = 2
            
    pressedKeys = pg.key.get_pressed()
    
    if getKeyDown(pg.K_w):
        #camPos.z += dt * speed
        right = rotateY(pg.Vector3(0,0,-1), roty)
        right.x *= -1
        camPos += right * speed * dt
    if getKeyDown(pg.K_s):
        right = rotateY(pg.Vector3(0,0,-1), roty)
        right.x *= -1
        camPos -= right * speed * dt
    if getKeyDown(pg.K_a):
        right = rotateY(pg.Vector3(1,0,0), roty)
        right.x *= -1
        camPos -= right * speed * dt
    if getKeyDown(pg.K_d):
        right = rotateY(pg.Vector3(1,0,0), roty)
        right.x *= -1
        camPos += right * speed * dt
    if getKeyDown(pg.K_LCTRL):
        camPos.y -= speed * dt
    if getKeyDown(pg.K_SPACE):
        camPos.y += speed * dt
    if getKeyDown(pg.K_LSHIFT):
        speed = 2.5
    else:
        speed = 1.2
    if not camLock:
        if getKeyDown(pg.K_LEFT):
            roty = (roty - (0.5*dt*speed)) % (pi*2)
        if getKeyDown(pg.K_RIGHT):
            roty = (roty + (0.5*dt*speed)) % (pi*2)

        if getKeyDown(pg.K_DOWN):
            rotx = (rotx - (0.5*dt*speed)) % (pi*2)
        if getKeyDown(pg.K_UP):
            rotx = (rotx + (0.5*dt*speed)) % (pi*2)

    if getKeyDown(pg.K_t):
        focalLen += 50 * dt * speed
    if getKeyDown(pg.K_g):
        focalLen -= 50 * dt * speed
    if getKeyDown(pg.K_r):
        focalLen = 500

    if camLock:
        roty = (roty + (0.1*dt*md[0])) % (pi*2)
        rotx = min(max((rotx - (0.1*dt*md[1])),-pi/2), pi/2)
        
    renderer.camPos = camPos
    renderer.camRotX = rotx
    renderer.camRotY = roty
    renderer.focalLen = focalLen

    frame = renderer.renderFrame()
    screen.blit(frame, (0,0))

    fovTextSurface = font.render("Focal length: " + str(focalLen), True, (0,0,0))
    posTextSurface = font.render("x: " + str(round(camPos.x,2)) + " y: " + str(round(camPos.y,2)) + " z: " + str(round(camPos.z,2)), True, (0,0,0))
    rotTextSurface = font.render("rotY: " + str(round(degrees(roty),1)) + "° rotx: " + str(round(degrees(rotx),1)) + "°", True, (0,0,0))
    fpsTextSurface = font.render("fps: " + str(round(1/dt, 1)), True, (0,0,0))
    camTextSurface = font.render("[TAB] Camlocked: " + ("True" if camLock else "False"), True, (0,0,0))
    renderModeTextSurface = font.render("Render mode: " + ("Color Map" if renderer.renderMode == 1 else "Depth Buffer"), True, (20,20,20))

    screen.blit(fovTextSurface, (0, 0))
    screen.blit(posTextSurface, (0, 28))
    screen.blit(rotTextSurface, (0, 56))
    screen.blit(camTextSurface, (0, 0 + 28 *3))
    screen.blit(renderModeTextSurface, (0, 0 + 28 *4))
    screen.blit(fpsTextSurface, (0, h-28))

    pg.display.update()
    dt = clock.tick(60)/1000
pg.quit()
