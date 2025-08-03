"""
Core ECS components for simplex-engine.
Defines reusable components for common game entity needs.
"""

from simplex.ecs.ecs import Component


class PositionComponent(Component):
    """Component for entity position in 3D space."""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__('position')
        self.x = x
        self.y = y  
        self.z = z
    
    @property
    def position(self):
        return (self.x, self.y, self.z)
    
    @position.setter
    def position(self, value):
        self.x, self.y, self.z = value


class VelocityComponent(Component):
    """Component for entity velocity in 3D space."""
    def __init__(self, vx=0.0, vy=0.0, vz=0.0):
        super().__init__('velocity')
        self.vx = vx
        self.vy = vy
        self.vz = vz
    
    @property
    def velocity(self):
        return (self.vx, self.vy, self.vz)
    
    @velocity.setter
    def velocity(self, value):
        self.vx, self.vy, self.vz = value


class RenderComponent(Component):
    """Component for entity rendering properties."""
    def __init__(self, primitive='cube', material=None, color=(1, 1, 1)):
        super().__init__('render')
        self.primitive = primitive
        self.material = material
        self.color = color
        self.visible = True


class CollisionComponent(Component):
    """Component for entity collision properties."""
    def __init__(self, width=10.0, height=10.0, depth=10.0, mass=1.0):
        super().__init__('collision')
        self.width = width
        self.height = height
        self.depth = depth
        self.mass = mass
        self.is_static = mass == 0.0


class InputComponent(Component):
    """Component for entities that respond to input."""
    def __init__(self, input_type='player'):
        super().__init__('input')
        self.input_type = input_type  # 'player', 'ai', etc.
        self.speed = 10.0


class ScoreComponent(Component):
    """Component for tracking score."""
    def __init__(self, score=0):
        super().__init__('score')
        self.score = score
