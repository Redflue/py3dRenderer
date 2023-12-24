from re import A
import pygame as pg
from sympy import true

pg.init()
font = pg.font.SysFont("None", 24)

w = 500
h = 500
screen = pg.display.set_mode((w,h))

def isInTriangle(a,b,c,p):
    w1 = (a.x*(c.y-a.y)+(mp.y-a.y)*(c.x-a.x)-mp.x*(c.y-a.y))/((b.y-a.y)*(c.x-a.x)-(b.x-a.x)*(c.y-a.y))
    w2 = (mp.y-a.y-w1*(b.y-a.y))/(c.y-a.y)
    w3 = 1-(w1+w2)
    return ((w1 >= 0 and w2 >= 0 and w1+w2 <= 1),(w1,w2,w3))

a = pg.Vector2(50,250)
b = pg.Vector2(250,15)
c = pg.Vector2(400,350)



loop = True
while loop:

    screen.fill((0,0,0))
    pg.draw.lines(screen, (255,255,255), True, [a,b,c], 2)

    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            loop = False
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                loop = False

    mp = pg.Vector2(pg.mouse.get_pos())

    #is in triangle?
    inTriangle = False

    w1 = (a.x*(c.y-a.y)+(mp.y-a.y)*(c.x-a.x)-mp.x*(c.y-a.y))/((b.y-a.y)*(c.x-a.x)-(b.x-a.x)*(c.y-a.y))
    w2 = (mp.y-a.y-w1*(b.y-a.y))/(c.y-a.y)
    w3 = 1-(w1+w2)

    p2 = a+w1*(b-a)
    pg.draw.line(screen, (255,0,0), a, a+w1*(b-a), 4)
    pg.draw.line(screen, (0,0,255), p2, p2+(w2*(c-a)), 4)

    if w1 >= 0 and w2 >= 0 and w1+w2 <= 1:
        inTriangle = True

    #end of: is in triangle?

    pg.draw.circle(screen,((0,255,0) if inTriangle else (255,0,0)), mp, 5)

    w1surf = font.render("w1 = " + str(round(w1,2)),True,(255,255,255))
    w2surf = font.render("w2 = " + str(round(w2,2)),True,(255,255,255))
    w3surf = font.render("w3 = " + str(round(w3,2)),True,(255,255,255))

    screen.blit(w1surf, (4,28*0+4))
    screen.blit(w2surf, (4,28*1+4))
    screen.blit(w3surf, (4,28*2+4))

    pg.display.update()

pg.quit()