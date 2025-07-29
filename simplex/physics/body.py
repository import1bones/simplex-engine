"""
Physics body classes for simplex-engine MVP-3.
Stub implementations for rigid and soft bodies.
"""

class RigidBody:
    def __init__(self, name, mass=1.0, position=(0,0,0), velocity=(0,0,0)):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
    def __repr__(self):
        return f"<RigidBody {self.name} pos={self.position} vel={self.velocity}>"

class SoftBody:
    def __init__(self, name, points=None):
        self.name = name
        self.points = points or []  # List of (x, y, z) tuples
    def __repr__(self):
        return f"<SoftBody {self.name} points={len(self.points)}>"
