import pygame as pg
import compushady as cps
import compushady.formats as cpsf
from compushady.shaders import hlsl

class ShaderManager:
    def __init__(self) -> None:
        self.shaderSources = {}
        self.shaders = {}

    def loadShaderFromPath(self, sourcePath:str, name:str, entryPoint:str = 'main'):
        with open(sourcePath) as file:
            string = file.read()
            self.shaderSources[name] = string
            self.shaders[name] = hlsl.compile(string, entryPoint)

    def getShader(self, name:str):
        return self.shaders[name]
