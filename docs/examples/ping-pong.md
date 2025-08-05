# Ping Pong Game Example

**Perfect for beginners** - Learn Simplex Engine through building the classic Ping Pong game from scratch.

## 🎯 What You'll Learn

By building this Ping Pong game, you'll understand:

- **Entity-Component-System (ECS)** architecture in practice
- **Event-driven programming** for game communication
- **Input handling** for player controls
- **Physics simulation** with collision detection
- **AI implementation** for computer opponents
- **Game state management** and scoring systems
- **Audio integration** for sound effects
- **Debug visualization** for development

## 🎮 Game Features

Our Ping Pong implementation includes:

- **Two-player gameplay** with keyboard controls
- **AI opponent** with adjustable difficulty
- **Ball physics** with realistic bouncing
- **Scoring system** with win conditions
- **Sound effects** for paddle hits and scoring
- **Visual feedback** and smooth animations
- **Debug mode** for development assistance

## 🏗️ Architecture Overview

The game demonstrates core ECS principles:

### Entities
- **Ball** - The game ball that bounces around
- **Player Paddle** - Player-controlled paddle
- **AI Paddle** - Computer-controlled paddle
- **Boundaries** - Top and bottom walls
- **Score Display** - UI elements for scoring

### Components
- **Transform** - Position, rotation, scale
- **Velocity** - Movement speed and direction
- **Collider** - Collision boundaries
- **Renderable** - Visual representation
- **Player** - Player-specific data
- **AI** - AI behavior parameters
- **Score** - Scoring information

### Systems
- **MovementSystem** - Handles entity movement
- **CollisionSystem** - Detects and resolves collisions
- **InputSystem** - Processes player input
- **AISystem** - Controls computer opponent
- **ScoringSystem** - Manages score tracking
- **RenderSystem** - Draws entities to screen
- **AudioSystem** - Plays sound effects

## 🚀 Getting Started

### Prerequisites

Make sure you have Simplex Engine installed:

```bash
pip install simplex-engine
```

### Basic Project Structure

```
ping_pong/
├── main.py              # Entry point
├── components/          # Game components
│   ├── __init__.py
│   ├── transform.py
│   ├── velocity.py
│   ├── collider.py
│   ├── player.py
│   └── ai.py
├── systems/             # Game systems
│   ├── __init__.py
│   ├── movement.py
│   ├── collision.py
│   ├── input.py
│   ├── ai.py
│   └── scoring.py
├── assets/              # Game assets
│   ├── sounds/
│   └── sprites/
└── config.py           # Game configuration
```

## 📋 Step-by-Step Tutorial

### Step 1: Project Setup

Create the basic project structure and main entry point:

```python
# main.py
from simplex import Engine, EngineConfig
from simplex.backends.pygame import PygameBackend
import logging

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create engine configuration
    config = EngineConfig(
        window_title="Ping Pong Game",
        window_width=800,
        window_height=600,
        target_fps=60,
        backend_type="pygame"
    )
    
    # Create and start engine
    engine = Engine(config)
    engine.run()

if __name__ == "__main__":
    main()
```

### Step 2: Define Components

Create the component classes that will hold our game data:

```python
# components/transform.py
from dataclasses import dataclass
from simplex.ecs import Component

@dataclass
class Transform(Component):
    """Position, rotation, and scale of an entity."""
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
```

```python
# components/velocity.py
from dataclasses import dataclass
from simplex.ecs import Component

@dataclass
class Velocity(Component):
    """Movement velocity of an entity."""
    dx: float = 0.0
    dy: float = 0.0
    max_speed: float = 500.0
```

```python
# components/collider.py
from dataclasses import dataclass
from simplex.ecs import Component

@dataclass
class Collider(Component):
    """Collision detection boundaries."""
    width: float = 1.0
    height: float = 1.0
    is_solid: bool = True
```

```python
# components/player.py
from dataclasses import dataclass
from simplex.ecs import Component

@dataclass
class Player(Component):
    """Player-specific data."""
    player_id: int = 1
    score: int = 0
    input_up_key: str = "w"
    input_down_key: str = "s"
```

```python
# components/ai.py
from dataclasses import dataclass
from simplex.ecs import Component

@dataclass
class AI(Component):
    """AI behavior parameters."""
    difficulty: float = 0.5  # 0.0 to 1.0
    reaction_time: float = 0.1
    max_speed: float = 300.0
    target_entity: int = None  # Entity ID to track
```

### Step 3: Implement Systems

Create the systems that will process our component data:

```python
# systems/movement.py
from simplex.ecs import SystemBase
from components.transform import Transform
from components.velocity import Velocity

class MovementSystem(SystemBase):
    """Handles entity movement based on velocity."""
    
    def update(self, dt: float) -> None:
        entities = self.ecs.get_entities_with([Transform, Velocity])
        
        for entity in entities:
            transform = self.ecs.get_component(entity, Transform)
            velocity = self.ecs.get_component(entity, Velocity)
            
            # Update position based on velocity
            transform.x += velocity.dx * dt
            transform.y += velocity.dy * dt
            
            # Clamp velocity to max speed
            speed = (velocity.dx ** 2 + velocity.dy ** 2) ** 0.5
            if speed > velocity.max_speed:
                factor = velocity.max_speed / speed
                velocity.dx *= factor
                velocity.dy *= factor
```

```python
# systems/collision.py
from simplex.ecs import SystemBase
from simplex.events import Event
from components.transform import Transform
from components.velocity import Velocity
from components.collider import Collider

class CollisionEvent(Event):
    """Event fired when collision occurs."""
    def __init__(self, entity1: int, entity2: int):
        super().__init__()
        self.entity1 = entity1
        self.entity2 = entity2

class CollisionSystem(SystemBase):
    """Handles collision detection and response."""
    
    def update(self, dt: float) -> None:
        entities = self.ecs.get_entities_with([Transform, Collider])
        
        # Check all entity pairs for collisions
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if self._check_collision(entity1, entity2):
                    self._handle_collision(entity1, entity2)
    
    def _check_collision(self, entity1: int, entity2: int) -> bool:
        """Check if two entities are colliding."""
        t1 = self.ecs.get_component(entity1, Transform)
        c1 = self.ecs.get_component(entity1, Collider)
        t2 = self.ecs.get_component(entity2, Transform)
        c2 = self.ecs.get_component(entity2, Collider)
        
        # AABB collision detection
        return (t1.x < t2.x + c2.width and
                t1.x + c1.width > t2.x and
                t1.y < t2.y + c2.height and
                t1.y + c1.height > t2.y)
    
    def _handle_collision(self, entity1: int, entity2: int) -> None:
        """Handle collision response."""
        # Emit collision event
        event = CollisionEvent(entity1, entity2)
        self.event_manager.emit(event)
        
        # Handle ball-paddle collision
        ball_entity, paddle_entity = self._identify_collision_types(entity1, entity2)
        if ball_entity and paddle_entity:
            self._handle_ball_paddle_collision(ball_entity, paddle_entity)
    
    def _handle_ball_paddle_collision(self, ball: int, paddle: int) -> None:
        """Handle ball bouncing off paddle."""
        ball_velocity = self.ecs.get_component(ball, Velocity)
        
        # Reverse horizontal direction
        ball_velocity.dx = -ball_velocity.dx
        
        # Add some random vertical component
        import random
        ball_velocity.dy += random.uniform(-100, 100)
```

```python
# systems/input.py
from simplex.ecs import SystemBase
from simplex.input import InputManager
from components.transform import Transform
from components.velocity import Velocity
from components.player import Player

class InputSystem(SystemBase):
    """Handles player input for paddle control."""
    
    def __init__(self, input_manager: InputManager):
        super().__init__()
        self.input_manager = input_manager
    
    def update(self, dt: float) -> None:
        entities = self.ecs.get_entities_with([Transform, Velocity, Player])
        
        for entity in entities:
            player = self.ecs.get_component(entity, Player)
            velocity = self.ecs.get_component(entity, Velocity)
            
            # Handle player input
            velocity.dy = 0  # Reset vertical velocity
            
            if self.input_manager.is_key_pressed(player.input_up_key):
                velocity.dy = -velocity.max_speed
            elif self.input_manager.is_key_pressed(player.input_down_key):
                velocity.dy = velocity.max_speed
```

### Step 4: Create Game Entities

Set up the game world with entities:

```python
# game_setup.py
from simplex.ecs import ECS
from components.transform import Transform
from components.velocity import Velocity
from components.collider import Collider
from components.player import Player
from components.ai import AI

def create_game_entities(ecs: ECS) -> dict:
    """Create all game entities and return entity IDs."""
    entities = {}
    
    # Create ball
    ball = ecs.create_entity()
    ecs.add_component(ball, Transform(x=400, y=300))
    ecs.add_component(ball, Velocity(dx=200, dy=100, max_speed=400))
    ecs.add_component(ball, Collider(width=20, height=20))
    entities['ball'] = ball
    
    # Create player paddle
    player_paddle = ecs.create_entity()
    ecs.add_component(player_paddle, Transform(x=50, y=250))
    ecs.add_component(player_paddle, Velocity(max_speed=400))
    ecs.add_component(player_paddle, Collider(width=20, height=100))
    ecs.add_component(player_paddle, Player(
        player_id=1,
        input_up_key="w",
        input_down_key="s"
    ))
    entities['player'] = player_paddle
    
    # Create AI paddle
    ai_paddle = ecs.create_entity()
    ecs.add_component(ai_paddle, Transform(x=730, y=250))
    ecs.add_component(ai_paddle, Velocity(max_speed=300))
    ecs.add_component(ai_paddle, Collider(width=20, height=100))
    ecs.add_component(ai_paddle, AI(
        difficulty=0.7,
        target_entity=ball
    ))
    entities['ai'] = ai_paddle
    
    # Create boundaries
    top_boundary = ecs.create_entity()
    ecs.add_component(top_boundary, Transform(x=0, y=0))
    ecs.add_component(top_boundary, Collider(width=800, height=10))
    entities['top'] = top_boundary
    
    bottom_boundary = ecs.create_entity()
    ecs.add_component(bottom_boundary, Transform(x=0, y=590))
    ecs.add_component(bottom_boundary, Collider(width=800, height=10))
    entities['bottom'] = bottom_boundary
    
    return entities
```

### Step 5: Integrate with Engine

Connect everything to the main engine:

```python
# main.py (updated)
from simplex import Engine, EngineConfig
from simplex.backends.pygame import PygameBackend
from systems.movement import MovementSystem
from systems.collision import CollisionSystem
from systems.input import InputSystem
from game_setup import create_game_entities
import logging

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create engine configuration
    config = EngineConfig(
        window_title="Ping Pong Game",
        window_width=800,
        window_height=600,
        target_fps=60,
        backend_type="pygame"
    )
    
    # Create engine
    engine = Engine(config)
    
    # Get engine subsystems
    ecs = engine.ecs
    input_manager = engine.input_manager
    
    # Create and register systems
    movement_system = MovementSystem()
    collision_system = CollisionSystem()
    input_system = InputSystem(input_manager)
    
    ecs.add_system(movement_system)
    ecs.add_system(collision_system)
    ecs.add_system(input_system)
    
    # Create game entities
    entities = create_game_entities(ecs)
    
    # Start the game
    engine.run()

if __name__ == "__main__":
    main()
```

## 🎮 Controls

- **Player 1 (Left Paddle):**
  - `W` - Move up
  - `S` - Move down

- **Player 2 (Right Paddle):**
  - Controlled by AI (automatic)

## 🔧 Customization Options

### Adjusting Game Difficulty

```python
# Modify AI component difficulty
ai_component.difficulty = 0.8  # Harder AI (0.0 = easy, 1.0 = hard)
ai_component.reaction_time = 0.05  # Faster reaction
```

### Changing Ball Physics

```python
# Modify ball velocity and behavior
ball_velocity.max_speed = 600  # Faster ball
ball_velocity.dx = 300  # Initial horizontal speed
```

### Adding Visual Effects

```python
# Add particle system for ball trail
from components.particle_emitter import ParticleEmitter

particle_emitter = ParticleEmitter(
    particle_count=10,
    lifetime=0.5,
    color=(255, 255, 255)
)
ecs.add_component(ball, particle_emitter)
```

## 🐛 Debugging Tips

### Enable Debug Mode

```python
# Add debug visualization
config.debug_mode = True
config.show_collision_bounds = True
config.show_entity_info = True
```

### Common Issues and Solutions

#### Ball Gets Stuck
```python
# Add minimum speed enforcement
if abs(ball_velocity.dx) < 50:
    ball_velocity.dx = 50 if ball_velocity.dx >= 0 else -50
```

#### Paddle Goes Off Screen
```python
# Add boundary checking in MovementSystem
screen_height = 600
paddle_height = 100

if transform.y < 0:
    transform.y = 0
elif transform.y + paddle_height > screen_height:
    transform.y = screen_height - paddle_height
```

#### Performance Issues
```python
# Optimize collision detection
# Only check ball against paddles and boundaries
if self.ecs.has_component(entity, Ball):
    # Only check ball collisions
    paddle_entities = self.ecs.get_entities_with([Paddle, Transform, Collider])
    # Check against paddles and boundaries only
```

## 🚀 Extensions and Improvements

### Add More Features

1. **Power-ups**
   - Speed boost
   - Larger paddle
   - Multi-ball

2. **Better AI**
   - Prediction algorithms
   - Different AI personalities
   - Machine learning integration

3. **Visual Enhancements**
   - Particle effects
   - Screen shake on impacts
   - Animated sprites

4. **Audio Improvements**
   - Background music
   - Different sound effects
   - Spatial audio

5. **Multiplayer Support**
   - Network multiplayer
   - Tournament mode
   - Spectator mode

### Performance Optimizations

1. **Spatial Partitioning**
   - Quadtree for collision detection
   - Frustum culling for rendering
   - Level-of-detail system

2. **Object Pooling**
   - Reuse particle objects
   - Pool collision events
   - Cache component lookups

3. **System Optimization**
   - Parallel system execution
   - Component filtering
   - Batch processing

## 📚 Related Resources

### Next Steps
- [Breakout Game Example](./breakout.md) - Similar mechanics with destructible blocks
- [Advanced Physics Tutorial](../tutorials/10-physics.md) - More complex physics
- [AI Behavior Trees](../tutorials/advanced-ai.md) - Advanced AI patterns

### Concepts Demonstrated
- [Entity-Component-System](../core-concepts/ecs.md) - ECS architecture
- [Event System](../core-concepts/events.md) - Event-driven programming
- [Input Handling](../systems/input.md) - Processing user input
- [Physics Systems](../systems/physics.md) - Collision and movement

### Advanced Topics
- [Performance Optimization](../advanced/performance/) - Making games run smoothly
- [Multiplayer Networking](../advanced/networking/) - Network game development
- [AI and Pathfinding](../advanced/ai/) - Advanced AI techniques

## 🎯 Summary

Congratulations! You've built a complete Ping Pong game using Simplex Engine. This example demonstrated:

✅ **ECS Architecture** - Separating data (components) from logic (systems)  
✅ **Event-Driven Programming** - Decoupled communication between systems  
✅ **Input Handling** - Responsive player controls  
✅ **Physics Simulation** - Collision detection and movement  
✅ **AI Implementation** - Computer opponent behavior  
✅ **Game State Management** - Scoring and game flow  

You now have a solid foundation for building more complex games with Simplex Engine. Try extending this example with new features or move on to other tutorials to learn additional concepts!

---

**Have questions?** Check out our [Community Discussions](https://github.com/import1bones/simplex-engine/discussions) or [submit an issue](https://github.com/import1bones/simplex-engine/issues) if you encounter problems.
