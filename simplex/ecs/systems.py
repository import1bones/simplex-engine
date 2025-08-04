"""
Core ECS systems for simplex-engine.
Defines reusable systems for common game logic with proper component filtering.
"""

from simplex.ecs.ecs import System
from simplex.utils.logger import log


class MovementSystem(System):
    """System that applies velocity to position components."""
    
    def __init__(self, event_system=None, bounds=(800, 600)):
        super().__init__('movement')
        self.event_system = event_system
        self.bounds_width, self.bounds_height = bounds
        self.required_components = ['position', 'velocity']
    
    def _process_entities(self, entities):
        """Update positions based on velocities for entities with both components."""
        for entity in entities:
            position_comp = entity.get_component('position')
            velocity_comp = entity.get_component('velocity')
            collision_comp = entity.get_component('collision')
            
            if position_comp and velocity_comp:
                # Apply velocity to position
                position_comp.x += velocity_comp.vx
                position_comp.y += velocity_comp.vy
                position_comp.z += velocity_comp.vz
                
                # Boundary checking for paddles (entities with collision but not ball)
                if collision_comp and 'ball' not in entity.name.lower():
                    half_height = collision_comp.height / 2
                    # Keep paddles within bounds
                    if position_comp.y - half_height < 0:
                        position_comp.y = half_height
                        velocity_comp.vy = 0
                    elif position_comp.y + half_height > self.bounds_height:
                        position_comp.y = self.bounds_height - half_height  
                        velocity_comp.vy = 0
                
                log(f"MovementSystem: Updated {entity.name} position to ({position_comp.x:.1f}, {position_comp.y:.1f})", level="DEBUG")


class CollisionSystem(System):
    """System that handles collision detection and response."""
    
    def __init__(self, event_system=None, bounds=(800, 600)):
        super().__init__('collision')
        self.event_system = event_system
        self.bounds_width, self.bounds_height = bounds
        self.required_components = ['position', 'collision']
    
    def _process_entities(self, entities):
        """Check for collisions between entities and boundaries."""
        # Check boundary collisions
        for entity in entities:
            self._check_boundary_collision(entity)
        
        # Check entity-to-entity collisions  
        for i, entity_a in enumerate(entities):
            for entity_b in entities[i+1:]:
                if self._check_entity_collision(entity_a, entity_b):
                    self._handle_collision(entity_a, entity_b)
    
    def _check_boundary_collision(self, entity):
        """Check and handle collision with world boundaries."""
        position = entity.get_component('position')
        velocity = entity.get_component('velocity')
        collision = entity.get_component('collision')
        
        if not all([position, velocity, collision]):
            return
        
        # Get entity dimensions
        half_width = collision.width / 2
        half_height = collision.height / 2
        
        # Top/bottom boundaries with proper positioning
        if position.y - half_height <= 0:
            if velocity.vy < 0:  # Only reverse if moving towards boundary
                velocity.vy = -velocity.vy
                position.y = half_height  # Position just inside boundary
                
                if self.event_system:
                    self.event_system.emit('physics_collision', {
                        'entity': entity.name,
                        'type': 'boundary',
                        'side': 'top'
                    })
        elif position.y + half_height >= self.bounds_height:
            if velocity.vy > 0:  # Only reverse if moving towards boundary
                velocity.vy = -velocity.vy
                position.y = self.bounds_height - half_height  # Position just inside boundary
                
                if self.event_system:
                    self.event_system.emit('physics_collision', {
                        'entity': entity.name,
                        'type': 'boundary',
                        'side': 'bottom'
                    })
        
        # Left/right boundaries for scoring
        if position.x < 0 or position.x > self.bounds_width:
            if self.event_system:
                self.event_system.emit('physics_collision', {
                    'entity': entity.name,
                    'type': 'boundary',
                    'side': 'left' if position.x < 0 else 'right'
                })
    
    def _check_entity_collision(self, entity_a, entity_b):
        """Check if two entities are colliding."""
        pos_a = entity_a.get_component('position')
        pos_b = entity_b.get_component('position') 
        col_a = entity_a.get_component('collision')
        col_b = entity_b.get_component('collision')
        
        if not all([pos_a, pos_b, col_a, col_b]):
            return False
        
        # Simple AABB collision detection
        return (abs(pos_a.x - pos_b.x) < (col_a.width + col_b.width) / 2 and
                abs(pos_a.y - pos_b.y) < (col_a.height + col_b.height) / 2)
    
    def _handle_collision(self, entity_a, entity_b):
        """Handle collision between two entities."""
        if self.event_system:
            self.event_system.emit('physics_collision', {
                'entity_a': entity_a.name,
                'entity_b': entity_b.name,
                'type': 'entity'
            })
        
        log(f"CollisionSystem: Collision between {entity_a.name} and {entity_b.name}", level="INFO")


class InputSystem(System):
    """System that processes input for entities with input components."""
    
    def __init__(self, event_system=None):
        super().__init__('input')
        self.event_system = event_system
        self.input_state = {}
        self.required_components = ['input', 'velocity']
        
        # Register for input events
        if self.event_system:
            self.event_system.register('input', self._handle_input_event)
    
    def _handle_input_event(self, event):
        """Handle input events and store state."""
        if hasattr(event, 'type') and hasattr(event, 'key'):
            log(f"InputSystem: Received input event - {event.type} {event.key}", level="INFO")
            if event.type == 'KEYDOWN':
                self.input_state[event.key] = True
                log(f"InputSystem: Key {event.key} pressed, state: {self.input_state}", level="DEBUG")
            elif event.type == 'KEYUP':
                self.input_state[event.key] = False
                log(f"InputSystem: Key {event.key} released, state: {self.input_state}", level="DEBUG")
    
    def _process_entities(self, entities):
        """Apply input to entities with input and velocity components."""
        for entity in entities:
            input_comp = entity.get_component('input')
            velocity_comp = entity.get_component('velocity')
            
            if input_comp and velocity_comp:
                if input_comp.input_type == 'player':
                    self._handle_player_input(entity, velocity_comp, input_comp)
                elif input_comp.input_type == 'ai':
                    # AI needs access to all entities to find the ball
                    self._handle_ai_input(entity, velocity_comp, input_comp, entities)
    
    def _handle_player_input(self, entity, velocity_comp, input_comp):
        """Handle player input for movement."""
        speed = getattr(input_comp, 'speed', 5.0)
        
        # Reset vertical velocity first
        velocity_comp.vy = 0
        
        if self.input_state.get('UP'):
            velocity_comp.vy = -speed  # Negative Y is up in many coordinate systems
            log(f"InputSystem: Moving {entity.name} UP with velocity {velocity_comp.vy}", level="DEBUG")
        elif self.input_state.get('DOWN'):
            velocity_comp.vy = speed   # Positive Y is down
            log(f"InputSystem: Moving {entity.name} DOWN with velocity {velocity_comp.vy}", level="DEBUG")
    
    def _handle_ai_input(self, entity, velocity_comp, input_comp, all_entities):
        """Handle AI movement logic."""
        # Find ball entity from all entities in the ECS
        ball_entity = None
        for e in all_entities:
            if 'ball' in e.name.lower():
                ball_entity = e
                break
        
        # Reset AI velocity
        velocity_comp.vy = 0
        
        if ball_entity:
            ball_pos = ball_entity.get_component('position')
            ball_vel = ball_entity.get_component('velocity')
            ai_pos = entity.get_component('position')
            
            if ball_pos and ball_vel and ai_pos:
                speed = getattr(input_comp, 'speed', 5.0) * 0.9  # AI slightly slower than player
                
                # Only track ball if it's moving towards AI (positive X velocity)
                if ball_vel.vx > 0:
                    target_y = ball_pos.y
                else:
                    # When ball moving away, return to center
                    target_y = 300  # Center of 600px height
                
                # Move towards target with some deadzone to prevent jittering
                y_diff = target_y - ai_pos.y
                if abs(y_diff) > 15:  # Deadzone
                    if y_diff > 0:
                        velocity_comp.vy = speed
                    else:
                        velocity_comp.vy = -speed


class ScoringSystem(System):
    """System that handles scoring logic."""
    
    def __init__(self, event_system=None, bounds=(800, 600)):
        super().__init__('scoring')
        self.event_system = event_system
        self.bounds_width, self.bounds_height = bounds
        self.score = {'player': 0, 'ai': 0}
        self.required_components = ['position']  # Only need position to check for scoring
        
        # Register for score events
        if self.event_system:
            self.event_system.register('score', self._handle_score_event)
    
    def _process_entities(self, entities):
        """Check for scoring conditions among ball entities."""
        for entity in entities:
            if 'ball' in entity.name.lower():
                position_comp = entity.get_component('position')
                velocity_comp = entity.get_component('velocity')
                
                if position_comp:
                    # Check if ball went off left or right side
                    if position_comp.x < 0:
                        self._score('ai', entity, position_comp, velocity_comp)
                    elif position_comp.x > self.bounds_width:
                        self._score('player', entity, position_comp, velocity_comp)
    
    def _score(self, scorer, ball_entity, position_comp, velocity_comp):
        """Handle scoring."""
        self.score[scorer] += 1
        
        # Reset ball position
        position_comp.x = self.bounds_width / 2
        position_comp.y = self.bounds_height / 2
        
        # Reset ball velocity
        if velocity_comp:
            velocity_comp.vx = -6 if scorer == 'ai' else 6
            velocity_comp.vy = 4
        
        # Emit score event
        if self.event_system:
            self.event_system.emit('score', {
                'scorer': scorer,
                'score': self.score.copy()
            })
        
        log(f"ScoringSystem: {scorer} scores! Score: {self.score}", level="INFO")
    
    def _handle_score_event(self, event):
        """Handle score events for logging/display."""
        if isinstance(event, dict) and 'scorer' in event:
            print(f"[Score] {event['scorer'].title()} scores! Current score: {event.get('score', {})}")
    
    def _check_boundary_collision(self, entity):
        """Check and handle collision with world boundaries."""
        position = entity.get_component('position')
        velocity = entity.get_component('velocity')
        collision = entity.get_component('collision')
        
        if not all([position, velocity, collision]):
            return
        
        # Get entity dimensions
        half_width = collision.width / 2
        half_height = collision.height / 2
        
        # Top/bottom boundaries with proper positioning
        if position.y - half_height <= 0:
            if velocity.vy < 0:  # Only reverse if moving towards boundary
                velocity.vy = -velocity.vy
                position.y = half_height  # Position just inside boundary
                
                if self.event_system:
                    self.event_system.emit('physics_collision', {
                        'entity': entity.name,
                        'type': 'boundary',
                        'side': 'top'
                    })
        elif position.y + half_height >= self.bounds_height:
            if velocity.vy > 0:  # Only reverse if moving towards boundary
                velocity.vy = -velocity.vy
                position.y = self.bounds_height - half_height  # Position just inside boundary
                
                if self.event_system:
                    self.event_system.emit('physics_collision', {
                        'entity': entity.name,
                        'type': 'boundary',
                        'side': 'bottom'
                    })
    
    def _check_entity_collision(self, entity_a, entity_b):
        """Check if two entities are colliding."""
        pos_a = entity_a.get_component('position')
        pos_b = entity_b.get_component('position') 
        col_a = entity_a.get_component('collision')
        col_b = entity_b.get_component('collision')
        
        if not all([pos_a, pos_b, col_a, col_b]):
            return False
        
        # Simple AABB collision detection
        return (abs(pos_a.x - pos_b.x) < (col_a.width + col_b.width) / 2 and
                abs(pos_a.y - pos_b.y) < (col_a.height + col_b.height) / 2)
    
    def _handle_collision(self, entity_a, entity_b):
        """Handle collision between two entities."""
        if self.event_system:
            self.event_system.emit('physics_collision', {
                'entity_a': entity_a.name,
                'entity_b': entity_b.name,
                'type': 'entity'
            })
        
        log(f"CollisionSystem: Collision between {entity_a.name} and {entity_b.name}", level="INFO")


class InputSystem(System):
    """System that processes input for entities with input components."""
    
    def __init__(self, event_system=None):
        super().__init__('input')
        self.event_system = event_system
        self.input_state = {}
        
        # Register for input events
        if self.event_system:
            self.event_system.register('input', self._handle_input_event)
    
    def _handle_input_event(self, event):
        """Handle input events and store state."""
        if hasattr(event, 'type') and hasattr(event, 'key'):
            log(f"InputSystem: Received input event - {event.type} {event.key}", level="INFO")
            if event.type == 'KEYDOWN':
                self.input_state[event.key] = True
                log(f"InputSystem: Key {event.key} pressed, state: {self.input_state}", level="INFO")
            elif event.type == 'KEYUP':
                self.input_state[event.key] = False
                log(f"InputSystem: Key {event.key} released, state: {self.input_state}", level="INFO")
    
    def update(self, entities):
        """Apply input to entities with input components."""
        for entity in entities:
            input_comp = entity.get_component('input')
            velocity_comp = entity.get_component('velocity')
            
            if input_comp and velocity_comp:
                if input_comp.input_type == 'player':
                    self._handle_player_input(entity, velocity_comp, input_comp)
                elif input_comp.input_type == 'ai':
                    self._handle_ai_input(entity, velocity_comp, input_comp, entities)
    
    def _handle_player_input(self, entity, velocity_comp, input_comp):
        """Handle player input for movement."""
        speed = input_comp.speed
        
        # Reset vertical velocity first
        velocity_comp.vy = 0
        
        if self.input_state.get('UP'):
            velocity_comp.vy = -speed  # Negative Y is up in many coordinate systems
            log(f"InputSystem: Moving {entity.name} UP with velocity {velocity_comp.vy}", level="INFO")
        elif self.input_state.get('DOWN'):
            velocity_comp.vy = speed   # Positive Y is down
            log(f"InputSystem: Moving {entity.name} DOWN with velocity {velocity_comp.vy}", level="INFO")
    
    def _handle_ai_input(self, entity, velocity_comp, input_comp, all_entities):
        """Handle AI movement logic."""
        # Find ball entity
        ball_entity = None
        for e in all_entities:
            if 'ball' in e.name.lower():
                ball_entity = e
                break
        
        # Reset AI velocity
        velocity_comp.vy = 0
        
        if ball_entity:
            ball_pos = ball_entity.get_component('position')
            ball_vel = ball_entity.get_component('velocity')
            ai_pos = entity.get_component('position')
            
            if ball_pos and ball_vel and ai_pos:
                speed = input_comp.speed * 0.9  # AI slightly slower than player
                
                # Only track ball if it's moving towards AI (positive X velocity)
                if ball_vel.vx > 0:
                    target_y = ball_pos.y
                else:
                    # When ball moving away, return to center
                    target_y = 300  # Center of 600px height
                
                # Move towards target with some deadzone to prevent jittering
                y_diff = target_y - ai_pos.y
                if abs(y_diff) > 15:  # Deadzone
                    if y_diff > 0:
                        velocity_comp.vy = speed
                    else:
                        velocity_comp.vy = -speed


class ScoringSystem(System):
    """System that handles scoring logic."""
    
    def __init__(self, event_system=None, bounds=(800, 600)):
        super().__init__('scoring')
        self.event_system = event_system
        self.bounds_width, self.bounds_height = bounds
        self.score = {'player': 0, 'ai': 0}
        
        # Register for score events
        if self.event_system:
            self.event_system.register('score', self._handle_score_event)
    
    def update(self, entities):
        """Check for scoring conditions."""
        for entity in entities:
            if 'ball' in entity.name.lower():
                position_comp = entity.get_component('position')
                velocity_comp = entity.get_component('velocity')
                
                if position_comp:
                    # Check if ball went off left or right side
                    if position_comp.x < 0:
                        self._score('ai', entity, position_comp, velocity_comp)
                    elif position_comp.x > self.bounds_width:
                        self._score('player', entity, position_comp, velocity_comp)
    
    def _score(self, scorer, ball_entity, position_comp, velocity_comp):
        """Handle scoring."""
        self.score[scorer] += 1
        
        # Reset ball position
        position_comp.x = self.bounds_width / 2
        position_comp.y = self.bounds_height / 2
        
        # Reset ball velocity
        if velocity_comp:
            velocity_comp.vx = -6 if scorer == 'ai' else 6
            velocity_comp.vy = 4
        
        # Emit score event
        if self.event_system:
            self.event_system.emit('score', {
                'scorer': scorer,
                'score': self.score.copy()
            })
        
        log(f"ScoringSystem: {scorer} scores! Score: {self.score}", level="INFO")
    
    def _handle_score_event(self, event):
        """Handle score events for logging/display."""
        if isinstance(event, dict) and 'scorer' in event:
            print(f"[Score] {event['scorer'].title()} scores! Current score: {event.get('score', {})}")
