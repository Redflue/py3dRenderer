import struct
import pygame as pg
import compushady as cps
import compushady.formats as cpsf

class Triangle:
    def __init__(self, p1:pg.Vector3, p2:pg.Vector3, p3:pg.Vector3, color = (255,0,0)) -> None:
        self.p1 = p1 # X in screen space
        self.p2 = p2 # Y in screen space
        self.p3 = p3 # Depth of point
        self.color = color

class TriangleBuffer:
    def __init__(self, size:int) -> None:
        self.pointBuffer = cps.Buffer(4*3*3*size, format=cpsf.R32_FLOAT)
        self.colorBuffer = cps.Buffer(4*4*size, format=cpsf.R8G8B8A8_UINT)

class TriangleBufferBuilder:
    def __init__(self, triangleBuffer: TriangleBuffer, initialOffset:int=0) -> None:
        self.triangleBuffer = triangleBuffer

        self.offset = initialOffset
        self.pointBufferUpload = cps.Buffer(self.triangleBuffer.pointBuffer.size, cps.HEAP_UPLOAD)
        self.colorBufferUpload = cps.Buffer(self.triangleBuffer.colorBuffer.size, cps.HEAP_UPLOAD)

    def packTriangle(self, tri:Triangle) -> None:

        pointOffset = self.offset*4*3*3
        colorOffset = self.offset*4*4

        #point 1
        self.pointBufferUpload.upload(struct.pack("f", tri.p1.x), pointOffset + (0*4))
        self.pointBufferUpload.upload(struct.pack("f", tri.p1.y), pointOffset + (1*4))
        self.pointBufferUpload.upload(struct.pack("f", tri.p1.z), pointOffset + (2*4))

        #point 2
        self.pointBufferUpload.upload(struct.pack("f", tri.p2.x), pointOffset + (3*4))
        self.pointBufferUpload.upload(struct.pack("f", tri.p2.y), pointOffset + (4*4))
        self.pointBufferUpload.upload(struct.pack("f", tri.p2.z), pointOffset + (5*4))

        #point 3
        self.pointBufferUpload.upload(struct.pack("f", tri.p3.x), pointOffset + (6*4))
        self.pointBufferUpload.upload(struct.pack("f", tri.p3.y), pointOffset + (7*4))
        self.pointBufferUpload.upload(struct.pack("f", tri.p3.z), pointOffset + (8*4))

        #color
        self.colorBufferUpload.upload(struct.pack("I", tri.color[0]), colorOffset + (0*4))
        self.colorBufferUpload.upload(struct.pack("I", tri.color[1]), colorOffset + (1*4))
        self.colorBufferUpload.upload(struct.pack("I", tri.color[2]), colorOffset + (2*4))
        self.colorBufferUpload.upload(struct.pack("I", 255), colorOffset + (3*4))

        self.offset += 1

    def finalizeBuild(self) -> None:
        self.pointBufferUpload.copy_to(self.triangleBuffer.pointBuffer)
        self.colorBufferUpload.copy_to(self.triangleBuffer.colorBuffer)