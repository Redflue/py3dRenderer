import pygame as pg
from math import *

pg.init()
pg.font.init()

w = 800
h = 600

screen = pg.display.set_mode((w,h))
pg.display.set_caption("3d renderer")
pg.display.set_icon(pg.surface.Surface((0,0)))

font = pg.font.SysFont('None', 24)
focalLen = 500
speed = 1.2

points = []
points.append(pg.Vector3(0,0,0))    #0
points.append(pg.Vector3(1,1,1))    #1
points.append(pg.Vector3(-1,-1,1))  #2
points.append(pg.Vector3(1,-1,1))   #3
points.append(pg.Vector3(-1,1,1))   #4
points.append(pg.Vector3(1,1,-1))   #5
points.append(pg.Vector3(-1,-1,-1)) #6
points.append(pg.Vector3(1,-1,-1))  #7
points.append(pg.Vector3(-1,1,-1))  #8

lines = []
lines.append((1,3))
lines.append((1,4))
lines.append((4,2))
lines.append((3,2))
#-----------------#
lines.append((5,7))
lines.append((5,8))
lines.append((6,7))
lines.append((6,8))
#-----------------#
lines.append((1,5))
lines.append((2,6))
lines.append((3,7))
lines.append((4,8))

tris = []
tris.append(((1,3,2),(255,0,0)))
tris.append(((1,4,2),(255,0,0)))

tris.append(((5,7,6),(0,255,0)))
tris.append(((5,8,6),(0,255,0)))

tris.append(((4,8,6),(0,0,255)))
tris.append(((4,2,6),(0,0,255)))

tris.append(((2,3,7),(0,255,255)))
tris.append(((2,6,7),(0,255,255)))

tris.append(((5,1,3),(255,0,255)))
tris.append(((5,7,3),(255,0,255)))

tris.append(((8,4,1),(255,255,0)))
tris.append(((8,5,1),(255,255,0)))

renderTris = []


roty = 0

def getKeyDown(keyCode = 0):
    return pg.key.get_pressed()[keyCode]

camPos = pg.Vector3(0,0,4)

def moveLocal(point: pg.Vector3):
    return pg.Vector3(point.x - camPos.x, point.y - camPos.y, point.z - camPos.z)

def screenLocal(point: pg.Vector3) -> pg.Vector2 :
    if point.z == 0:
        z = 1
    else:
        z = point.z
    return pg.Vector2(focalLen * (point.x/z) + w/2, focalLen * (point.y/z) + h/2)

def rotateY(point: pg.Vector3, rot=roty):
    return pg.Vector3(point.x*cos(roty) - point.z*sin(roty), point.y, point.x*sin(roty) + point.z*cos(roty))

rotx = 0
def rotateX(point: pg.Vector3, rot=rotx):
    return pg.Vector3(point.x, point.z*sin(rotx) + point.y*cos(rotx), point.z*cos(rotx) - point.y*sin(rotx))


dt = 0.01
clock = pg.time.Clock()
mainLoop = True
while mainLoop:

    screen.fill((230,230,230))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            mainLoop = False
        if event.type == pg.KEYDOWN:
            pass

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

    renderTris.clear()
    for t in tris:
        color = t[1]
        indices = t[0]

        p1 = points[indices[0]]
        p2 = points[indices[1]]
        p3 = points[indices[2]]

        p1 = rotateX(rotateY(moveLocal(p1)))
        p2 = rotateX(rotateY(moveLocal(p2)))
        p3 = rotateX(rotateY(moveLocal(p3)))

        center = (p1 + p2 + p3)/3
        depth = center.magnitude()

        if p1.z < 0 and p2.z < 0 and p3.z < 0:
            renderTris.append(((screenLocal(p1),screenLocal(p2),screenLocal(p3)),color,depth))

        #    pg.draw.polygon(screen, color, [screenLocal(p1),screenLocal(p2),screenLocal(p3)])

    renderTris.sort(reverse=True,key=lambda t:t[2])

    for t in renderTris:
        pg.draw.polygon(screen, t[1], [t[0][0],t[0][1],t[0][2]])

    for l in lines:
        p1 = points[l[0]]
        p2 = points[l[1]]

        local1 = rotateX(rotateY(moveLocal(p1)))
        local2 = rotateX(rotateY(moveLocal(p2)))

        if local1.z < 0 and local2.z < 0:
            #pg.draw.aaline(screen, (40,40,40), screenLocal(local1), screenLocal(local2))
            pass
            #pg.draw.line(screen, (40,40,40), screenLocal(local1), screenLocal(local2))

    pindex = 0
    for p in points:
        localMove = rotateX(rotateY(moveLocal(p)))
        if localMove.z < 0:
            coords = screenLocal(localMove)
            textNum = font.render(str(pindex), True, (0,0,0))
            #screen.blit(textNum, coords)
            pindex += 1
            #pg.draw.circle(screen, (255,255,255), coords, 5)

    fovTextSurface = font.render("Focal length: " + str(focalLen), True, (0,0,0))
    posTextSurface = font.render("x: " + str(round(camPos.x,2)) + " y: " + str(round(camPos.y,2)) + " z: " + str(round(camPos.z,2)), True, (0,0,0))
    rotTextSurface = font.render("rotY: " + str(round(degrees(roty),1)) + "° rotx: " + str(round(degrees(rotx),1)) + "°", True, (0,0,0))
    fpsTextSurface = font.render("fps: " + str(round(1/dt, 1)), True, (0,0,0))

    screen.blit(fovTextSurface, (0, 0))
    screen.blit(posTextSurface, (0, 28))
    screen.blit(rotTextSurface, (0, 56))
    screen.blit(fpsTextSurface, (0, h-28))

    pg.display.update()
    dt = clock.tick(60)/1000
pg.quit()
