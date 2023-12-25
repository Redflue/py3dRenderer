import pygame as pg
import compushady as cps
import compushady.formats as cpsf
from compushady.shaders import hlsl

w = 500
h = 500
screen = pg.display.set_mode((w,h))

texture = cps.Texture2D(500-32,500-32,cpsf.R8G8B8A8_UINT)

shaderSource = open("./shaders/testShader.hlsl").read()
shader = hlsl.compile(shaderSource)

compute = cps.Compute(shader,uav=[texture])
compute.dispatch(texture.width//2, texture.height//2, 1)

readBuffer = cps.Buffer(texture.size, cps.HEAP_READBACK)
texture.copy_to(readBuffer)

surf = pg.image.frombuffer(readBuffer.readback2d(0,texture.width,texture.height,4), (texture.width, texture.height), "RGBA")

loop = True
while loop:

    screen.blit(surf, (16,16))
    
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            loop = False
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                loop = False

    pg.display.update()

pg.quit()