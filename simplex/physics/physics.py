"""
Minimal Physics implementation for MVP.
"""

from .interface import PhysicsInterface
from simplex.utils.logger import log

class Physics(PhysicsInterface):
    """
    Physics system for simplex-engine MVP.
    Handles physics simulation and integrates with external engines (e.g., pybullet).

    Advanced Features:
    - Rigid body simulation
    - Soft body simulation
    - Collision detection and response
    - Emits physics events (collision, trigger, etc.)
    - Extensible for custom physics objects and integration
    """
    def __init__(self, event_system=None):
        from .body import RigidBody, SoftBody
        self.rigid_bodies = []  # List[RigidBody]
        self.soft_bodies = []   # List[SoftBody]
        self.event_system = event_system

    def add_rigid_body(self, body):
        self.rigid_bodies.append(body)
        log(f"Rigid body added: {body}", level="INFO")

    def add_soft_body(self, body):
        self.soft_bodies.append(body)
        log(f"Soft body added: {body}", level="INFO")

    def step_collision_response(self, a, b):
        """Stub for collision response between two bodies."""
        log(f"Collision response: {a} <-> {b}", level="DEBUG")

    def simulate(self) -> None:
        """
        Run physics simulation step.
        Handles rigid/soft body simulation, collision detection, and emits events.
        """
        try:
            log("Simulating physics...", level="INFO")
            # Rigid body simulation stub
            for body in self.rigid_bodies:
                # body.simulate_step()  # Placeholder for RigidBody
                pass
            # Soft body simulation stub
            for body in self.soft_bodies:
                # body.simulate_step()  # Placeholder for SoftBody
                pass
            # Collision detection stub
            collisions = self._detect_collisions()
            for a, b in collisions:
                log(f"Collision detected: {a} <-> {b}", level="INFO")
                self.step_collision_response(a, b)
                if self.event_system:
                    self.event_system.emit('physics_collision', {'a': a, 'b': b})
        except Exception as e:
            log(f"Physics simulation error: {e}", level="ERROR")

    def _detect_collisions(self):
        """Stub for collision detection. Returns list of (a, b) pairs."""
        # In a real engine, this would use bounding boxes, shapes, etc.
        return []
