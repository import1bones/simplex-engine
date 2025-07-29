"""
Material and Shader system for simplex-engine MVP-3.
Allows user extensibility for custom materials and shaders.
"""

class Shader:
    def __init__(self, name, source=None):
        self.name = name
        self.source = source  # GLSL/HLSL or other shader code
    def __repr__(self):
        return f"<Shader {self.name}>"

class Material:
    def __init__(self, name, shader=None, properties=None):
        self.name = name
        self.shader = shader
        self.properties = properties or {}
    def __repr__(self):
        return f"<Material {self.name} shader={self.shader}>"
