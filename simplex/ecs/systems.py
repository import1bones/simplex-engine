"""
Core ECS systems for simplex-engine.
Defines reusable systems for common game logic.
"""

from simplex.ecs.ecs import System
from simplex.utils.logger import log


class MovementSystem(System):
    """System that applies velocity to position components."""
    
    def __init__(self, event_system=None):
        super().__init__('movement')
        self.event_system = event_system
    
    def update(self, entities):
        """Update positions based on velocities."""
        for entity in entities:
            position_comp = entity.get_component('position')
            velocity_comp = entity.get_component('velocity')
            
            if position_comp and velocity_comp:
                # Apply velocity to position
                position_comp.x += velocity_comp.vx
                position_comp.y += velocity_comp.vy
                position_comp.z += velocity_comp.vz
                
                log(f"MovementSystem: Updated {entity.name} position to {position_comp.position}", level="DEBUG")


class CollisionSystem(System):
    """System that handles collision detection and response."""
    
    def __init__(self, event_system=None, bounds=(800, 600)):
        super().__init__('collision')
        self.event_system = event_system
        self.bounds_width, self.bounds_height = bounds
    
    def update(self, entities):
        """Check for collisions between entities and boundaries."""
        # Get entities with collision and position components
        collidables = []
        for entity in entities:
            if entity.get_component('collision') and entity.get_component('position'):
                collidables.append(entity)
        
        # Check boundary collisions
        for entity in collidables:
            self._check_boundary_collision(entity)
        
        # Check entity-to-entity collisions  
        for i, entity_a in enumerate(collidables):
            for entity_b in collidables[i+1:]:
                if self._check_entity_collision(entity_a, entity_b):
                    self._handle_collision(entity_a, entity_b)
    
    def _check_boundary_collision(self, entity):
        """Check and handle collision with world boundaries."""
        position = entity.get_component('position')
        velocity = entity.get_component('velocity')
        collision = entity.get_component('collision')
        
        if not all([position, velocity, collision]):
            return
        
        # Top/bottom boundaries
        if position.y <= 0 or position.y >= self.bounds_height:
            velocity.vy = -velocity.vy
            position.y = max(0, min(position.y, self.bounds_height))
            
            if self.event_system:
                self.event_system.emit('physics_collision', {
                    'entity': entity.name,
                    'type': 'boundary',
                    'side': 'top' if position.y >= self.bounds_height else 'bottom'
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
            if event.type == 'KEYDOWN':
                self.input_state[event.key] = True
            elif event.type == 'KEYUP':
                self.input_state[event.key] = False
    
    def update(self, entities):
        """Apply input to entities with input components."""
        for entity in entities:
            input_comp = entity.get_component('input')
            position_comp = entity.get_component('position')
            
            if input_comp and position_comp:
                if input_comp.input_type == 'player':
                    self._handle_player_input(entity, position_comp, input_comp)
                elif input_comp.input_type == 'ai':
                    self._handle_ai_input(entity, position_comp, input_comp, entities)
    
    def _handle_player_input(self, entity, position_comp, input_comp):
        """Handle player input for movement."""
        speed = input_comp.speed
        
        if self.input_state.get('UP') or self.input_state.get('w'):
            new_y = min(position_comp.y + speed, 600)
            position_comp.y = new_y
        elif self.input_state.get('DOWN') or self.input_state.get('s'):
            new_y = max(position_comp.y - speed, 0)
            position_comp.y = new_y
    
    def _handle_ai_input(self, entity, position_comp, input_comp, all_entities):
        """Handle AI movement logic."""
        # Find ball entity
        ball_entity = None
        for e in all_entities:
            if 'ball' in e.name.lower():
                ball_entity = e
                break
        
        if ball_entity:
            ball_pos = ball_entity.get_component('position')
            if ball_pos:
                speed = input_comp.speed * 0.8  # AI slightly slower
                if ball_pos.y > position_comp.y:
                    position_comp.y = min(position_comp.y + speed, 600)
                elif ball_pos.y < position_comp.y:
                    position_comp.y = max(position_comp.y - speed, 0)


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
