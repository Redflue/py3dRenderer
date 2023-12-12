import pygame as pg
import compushady as cps
import compushady.formats as cpsf
from compushady.shaders import hlsl

pg.init()

w = 500
h = 500
screen = pg.display.set_mode((w,h))

def isInTriangle(a,b,c,p):
    w1 = (a.x*(c.y-a.y)+(p.y-a.y)*(c.x-a.x)-p.x*(c.y-a.y))/((b.y-a.y)*(c.x-a.x)-(b.x-a.x)*(c.y-a.y))
    w2 = (p.y-a.y-w1*(b.y-a.y))/(c.y-a.y)
    w3 = 1-(w1+w2)
    return ((w1 >= 0 and w2 >= 0 and w1+w2 <= 1),(w1,w2,w3))

def drawTriangle(a,b,c):
    a = pg.Vector2(a)
    b = pg.Vector2(b)
    c = pg.Vector2(c)

    mn = pg.Vector2(min(a.x,b.x,c.x),min(a.y,b.y,c.y))
    mx = pg.Vector2(max(a.x,b.x,c.x),max(a.y,b.y,c.y))

    dv = mx-mn
    a-=mn
    b-=mn
    c-=mn

    surf = pg.Surface((dv.x,dv.y), pg.SRCALPHA)
    surf.fill((0,0,255,50))
    pixels:pg.PixelArray = pg.PixelArray(surf)

    for x in range(int(dv.x)):
        for y in range(int(dv.y)):
            p = pg.Vector2(x,y)
            result = isInTriangle(a,b,c,p)
            if result[0]:
                pixels[x,y] = (result[1][0]*255,result[1][1]*255,result[1][2]*255)

    pixels.close()

    screen.blit(surf, mn)
    #pg.draw.lines(screen,(100,0,0), True, [a+mn,b+mn,c+mn], 2)

screen.fill((0,0,0))
drawTriangle((50,250),(250, 15),(400,350))

loop = True
while loop:
    
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            loop = False
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                loop = False

    

    pg.display.update()

pg.quit()