
import pygame as pg
import classes.TriangleBuffers as TriangleBuffers
from math import *
import compushady as cps
import compushady.formats as cpsf

from classes.ShaderManager import ShaderManager

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

triangleOffset = pg.Vector3(4,0.5,-2)
points.append(pg.Vector3(1,0,1) + triangleOffset)       #9
points.append(pg.Vector3(-1,0,1) + triangleOffset)      #10
points.append(pg.Vector3(-.5,0,-1) + triangleOffset)    #11
points.append(pg.Vector3(0.5,1,0.7) + triangleOffset) 	#12
points.append(pg.Vector3(-1,0.5,0.25) + triangleOffset) #13
points.append(pg.Vector3(0,-1,0.5) + triangleOffset) 	#14

points.append(pg.Vector3(-20,-25,-20))	#15
points.append(pg.Vector3(20,-25,-20))	#16
points.append(pg.Vector3(-20,-25,20))	#17
points.append(pg.Vector3(20,-25,20))		#18

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

tris.append(((9,10,11), (255,200,0)))
tris.append(((12,13,14), (150,100,255)))

tris.append(((15,16,17),(100,100,100)))
tris.append(((16,18,17),(100,100,100)))

class RenderMode:
    color = 1
    depth = 2

class Renderer:
    def __init__(self, w, h) -> None:
        self.focalLen = 500
        self.camPos = pg.Vector3(0,0,0)
        self.camRotX = 0
        self.camRotY = 0
        self.w = w
        self.h = h

        self.shaderManager = ShaderManager()
        self.loadRendererShaders()

        self.colorMap = cps.Texture2D(w,h,cpsf.R8G8B8A8_UINT)
        self.depthMap = cps.Texture2D(w,h,cpsf.R32_FLOAT)

        self.colorReadbackBuffer = cps.Buffer(self.colorMap.size, cps.HEAP_READBACK)
        self.renderMode = RenderMode.color

        self.clearShader = cps.Compute(self.shaderManager.getShader("clear"), uav=[self.colorMap, self.depthMap])

    def loadRendererShaders(self):
        self.shaderManager.loadShaderFromPath("./shaders/clearDepth&ColorBuffer.hlsl", "clear")
        self.shaderManager.loadShaderFromPath("./shaders/renderTriangleBuffer.hlsl", "render")
        self.shaderManager.loadShaderFromPath("./shaders/renderTriangleDepthBuffer.hlsl", "renderDepth")

    def moveLocal(self, point: pg.Vector3):
        return pg.Vector3(point.x - self.camPos.x, point.y - self.camPos.y, point.z - self.camPos.z)

    def screenLocal(self, point: pg.Vector3) -> pg.Vector3 :
        if point.z == 0:
            z = 1.0
        else:
            z = point.z
        return pg.Vector3(self.focalLen * (point.x/z) + self.w/2, self.focalLen * (point.y/z) + self.h/2, abs(point.z))
    
    def rotateY(self, point: pg.Vector3, rot=0):
        return pg.Vector3(point.x*cos(rot) - point.z*sin(rot), point.y, point.x*sin(rot) + point.z*cos(rot))

    def rotateX(self, point: pg.Vector3, rot=0):
        return pg.Vector3(point.x, point.z*sin(rot) + point.y*cos(rot), point.z*cos(rot) - point.y*sin(rot))
    
    def makeTriangleBuffer(self, tris=tris, points=points):
        buffer = TriangleBuffers.TriangleBuffer(len(tris))
        bufferBuilder = TriangleBuffers.TriangleBufferBuilder(buffer)
        for t in tris:
            color = t[1]
            indices = t[0]

            p1 = points[indices[0]]
            p2 = points[indices[1]]
            p3 = points[indices[2]]

            p1 = self.rotateX(self.rotateY(self.moveLocal(p1), self.camRotY), self.camRotX)
            p2 = self.rotateX(self.rotateY(self.moveLocal(p2), self.camRotY), self.camRotX)
            p3 = self.rotateX(self.rotateY(self.moveLocal(p3), self.camRotY), self.camRotX)

            if p1.z < 0 and p2.z < 0 and p3.z < 0:
                #renderTris.append(((screenLocal(p1),screenLocal(p2),screenLocal(p3)),color,depth))
                tri = TriangleBuffers.Triangle(
                    self.screenLocal(p1),
                    self.screenLocal(p2),
                    self.screenLocal(p3),
                    color
                )
                bufferBuilder.packTriangle(tri)
        bufferBuilder.finalizeBuild()
        return buffer
    
    def renderFrame(self):
        triBuffer = self.makeTriangleBuffer(tris, points)

        self.clearShader.dispatch(self.w//8, self.h//8, 1)

        #compute = cps.Compute(self.shaderManager.getShader("render"), srv=[triBuffer.pointBuffer, triBuffer.colorBuffer], uav=[self.colorMap, self.depthMap])
        if self.renderMode == RenderMode.color:
            compute = cps.Compute(self.shaderManager.getShader("render"), srv=[triBuffer.pointBuffer, triBuffer.colorBuffer], uav=[self.colorMap, self.depthMap])
        else:
            compute = cps.Compute(self.shaderManager.getShader("renderDepth"), srv=[triBuffer.pointBuffer, triBuffer.colorBuffer], uav=[self.colorMap, self.depthMap])
        compute.dispatch(self.w//8, self.h//8, 1)

        self.colorMap.copy_to(self.colorReadbackBuffer)

        frameImage = pg.image.frombuffer(self.colorReadbackBuffer.readback(), (self.colorMap.width, self.colorMap.height), "RGBA")
        return frameImage

        



    
    