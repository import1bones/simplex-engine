"""
Minimal Physics implementation for MVP.
"""

from .interface import PhysicsInterface
from simplex.utils.logger import log

class Physics(PhysicsInterface):
    """
    Physics system for simplex-engine with proper dependency injection.
    Handles physics simulation and integrates with external engines (e.g., pybullet).

    Advanced Features:
    - Rigid body simulation
    - Soft body simulation
    - Collision detection and response
    - Emits physics events (collision, trigger, etc.)
    - Extensible for custom physics objects and integration
    """
    def __init__(self, event_system=None, ecs=None):
        from .body import RigidBody, SoftBody
        
        self.event_system = event_system
        self.ecs = ecs  # Reference to ECS for entity-based physics
        self._initialized = False
        
        # Physics world state
        self.rigid_bodies = []  # List[RigidBody]
        self.soft_bodies = []   # List[SoftBody]
        self.config = {}
        
        log("Physics system created", level="INFO")
    
    def initialize(self, config=None):
        """Initialize physics system with configuration."""
        self.config = config or {}
        
        # Initialize physics engine backend
        backend = self.config.get("backend", "builtin")
        
        if backend == "bullet":
            self._initialize_bullet_physics()
        else:
            self._initialize_builtin_physics()
        
        self._initialized = True
        log(f"Physics initialized with {backend} backend", level="INFO")
    
    def _initialize_bullet_physics(self):
        """Initialize PyBullet physics backend."""
        try:
            import pybullet as p
            # Initialize bullet physics
            self.physics_client = p.connect(p.DIRECT)  # No GUI
            p.setGravity(0, -9.81, 0)  # Standard gravity
            log("PyBullet physics backend initialized", level="INFO")
        except ImportError:
            log("PyBullet not available, falling back to builtin physics", level="WARNING")
            self._initialize_builtin_physics()
    
    def _initialize_builtin_physics(self):
        """Initialize builtin physics backend."""
        # Simple physics simulation without external dependencies
        self.gravity = self.config.get("gravity", -9.81)
        self.physics_client = None
        log("Builtin physics backend initialized", level="INFO")

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
        if not self._initialized:
            log("Physics not initialized, skipping simulation", level="WARNING")
            return
            
        try:
            log("Simulating physics...", level="DEBUG")
            
            # Integrate with ECS for entity-based physics
            if self.ecs:
                self._simulate_ecs_physics()
            
            # Rigid body simulation
            for body in self.rigid_bodies:
                # body.simulate_step()  # Placeholder for RigidBody
                pass
                
            # Soft body simulation stub
            for body in self.soft_bodies:
                # body.simulate_step()  # Placeholder for SoftBody
                pass
                
            # Collision detection - enhanced for ECS integration
            collisions = self._detect_collisions()
            for a, b in collisions:
                log(f"Collision detected: {a} <-> {b}", level="INFO")
                self.step_collision_response(a, b)
                if self.event_system:
                    self.event_system.emit('physics_collision', {'a': a, 'b': b})
                    
        except Exception as e:
            log(f"Physics simulation error: {e}", level="ERROR")
            if self.event_system:
                self.event_system.emit('system_error', {'system': 'Physics', 'error': str(e)})
    
    def _simulate_ecs_physics(self):
        """Apply physics to ECS entities with physics components."""
        if not self.ecs:
            return
            
        # Get entities with physics-relevant components
        physics_entities = self.ecs.get_entities_with('position', 'velocity')
        
        for entity in physics_entities:
            position = entity.get_component('position')
            velocity = entity.get_component('velocity')
            mass_comp = entity.get_component('mass')
            
            if position and velocity:
                # Apply gravity if entity has mass
                if mass_comp and hasattr(mass_comp, 'mass') and mass_comp.mass > 0:
                    # Simple gravity application
                    gravity_force = self.gravity * mass_comp.mass
                    velocity.vy += gravity_force * 0.016  # Assuming 60 FPS
                
                # Apply basic physics integration (handled by MovementSystem)
                # This is just for physics-specific effects
                pass
    
    def shutdown(self):
        """Clean shutdown of physics system."""
        if self.physics_client:
            try:
                import pybullet as p
                p.disconnect(self.physics_client)
            except:
                pass
        
        self._initialized = False
        log("Physics system shutdown", level="INFO")
    
    def simulate_ecs(self, ecs_instance):
        """
        Run physics simulation integrated with ECS entities.
        This method processes entities with physics components.
        """
        try:
            log("Simulating ECS-integrated physics...", level="INFO")
            
            # Get entities with position and velocity components
            moving_entities = ecs_instance.get_entities_with('position', 'velocity')
            
            # Apply physics simulation to ECS entities
            for entity in moving_entities:
                position_comp = entity.get_component('position')
                velocity_comp = entity.get_component('velocity')
                collision_comp = entity.get_component('collision')
                
                if position_comp and velocity_comp:
                    # Simple physics integration (position += velocity)
                    position_comp.x += velocity_comp.vx
                    position_comp.y += velocity_comp.vy
                    position_comp.z += velocity_comp.vz
                    
                    # Apply basic physics constraints
                    if collision_comp and not collision_comp.is_static:
                        # Apply gravity, friction, etc. here if needed
                        pass
            
            # Emit physics update event
            if self.event_system:
                self.event_system.emit('physics_update', {'entities_processed': len(moving_entities)})
                
        except Exception as e:
            log(f"ECS physics simulation error: {e}", level="ERROR")

    def _detect_collisions(self):
        """Stub for collision detection. Returns list of (a, b) pairs."""
        # In a real engine, this would use bounding boxes, shapes, etc.
        return []
