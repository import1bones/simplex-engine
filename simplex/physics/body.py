"""
Physics body classes for simplex-engine MVP-3.
Stub implementations for rigid and soft bodies.
"""


class RigidBody:
    def __init__(self, name, mass=1.0, position=(0, 0, 0), velocity=(0, 0, 0)):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def apply_impulse(self, impulse):
        # For static paddles (mass=0), move position directly
        if self.mass == 0:
            x, y, z = self.position
            dx, dy, dz = impulse
            self.position = (x + dx, y + dy, z + dz)
        else:
            # For dynamic bodies, add to velocity
            vx, vy, vz = self.velocity
            dx, dy, dz = impulse
            self.velocity = (vx + dx, vy + dy, vz + dz)

    def __repr__(self):
        return f"<RigidBody {self.name} pos={self.position} vel={self.velocity}>"


class SoftBody:
    def __init__(self, name, points=None):
        self.name = name
        self.points = points or []  # List of (x, y, z) tuples

    def __repr__(self):
        return f"<SoftBody {self.name} points={len(self.points)}>"
