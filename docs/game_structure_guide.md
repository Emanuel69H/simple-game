# 🎮 Multi-Game Architecture

## 📁 Folder Structure for Multiple Games

```
game/
├── __init__.py
├── constants.py              # Shared constants
├── base_game.py              # Base game class (NEW)
│
├── multiplayer/
│   ├── __init__.py
│   └── client.py
│
├── dash_dash/                # Current game
│   ├── __init__.py
│   ├── game_logic.py         # Game-specific logic
│   ├── constants.py          # Game-specific constants
│   └── screens/
│       ├── __init__.py
│       └── game_screen.py    # Move current game_screen here
│
├── snake_game/               # Future game example
│   ├── __init__.py
│   ├── game_logic.py
│   ├── constants.py
│   └── screens/
│       ├── __init__.py
│       └── game_screen.py
│
└── pong/                     # Another future game
    ├── __init__.py
    ├── game_logic.py
    ├── constants.py
    └── screens/
        ├── __init__.py
        └── game_screen.py
```

---

## 🏗️ Base Game Class

Create `game/base_game.py`:

```python
"""
Base Game Class
All games should inherit from this.
"""

import pygame
from abc import ABC, abstractmethod


class BaseGame(ABC):
    """Abstract base class for all games."""
    
    def __init__(self, screen, config, client=None):
        """
        Initialize base game.
        
        Args:
            screen: pygame display surface
            config: ConfigManager instance
            client: NetworkClient instance (optional, for multiplayer)
        """
        self.screen = screen
        self.config = config
        self.client = client
        self.running = True
    
    @abstractmethod
    def handle_event(self, event):
        """Handle input events. Must be implemented by subclass."""
        pass
    
    @abstractmethod
    def update(self, dt):
        """Update game logic. Must be implemented by subclass."""
        pass
    
    @abstractmethod
    def draw(self):
        """Draw the game. Must be implemented by subclass."""
        pass
    
    def on_enter(self):
        """Called when game starts. Can be overridden."""
        pass
    
    def on_exit(self):
        """Called when game exits. Can be overridden."""
        pass
    
    @property
    @abstractmethod
    def game_name(self):
        """Return the name of the game. Must be implemented."""
        pass
    
    @property
    @abstractmethod
    def supports_multiplayer(self):
        """Return True if game supports multiplayer. Must be implemented."""
        pass
```

---

## 📝 Example: Dash Dash Implementation

Move current game to `game/dash_dash/`:

**game/dash_dash/game_logic.py:**
```python
"""
Dash Dash - Game Logic
"""

from game.base_game import BaseGame
from game.dash_dash.constants import *
from game.dash_dash.screens.game_screen import DashDashGameScreen


class DashDashGame(BaseGame):
    """Dash Dash multiplayer game."""
    
    @property
    def game_name(self):
        return "Dash Dash"
    
    @property
    def supports_multiplayer(self):
        return True
    
    def __init__(self, screen, config, client, is_host, back_callback):
        super().__init__(screen, config, client)
        self.is_host = is_host
        self.back_callback = back_callback
        self.game_screen = DashDashGameScreen(screen, config, client, is_host, back_callback)
    
    def handle_event(self, event):
        self.game_screen.handle_event(event)
    
    def update(self, dt):
        self.game_screen.update(dt)
    
    def draw(self):
        self.game_screen.draw()
    
    def on_exit(self):
        self.game_screen.on_exit()
```

---

## 🎯 Game Registry

Create `game/game_registry.py`:

```python
"""
Game Registry
Central registry for all available games.
"""

from game.dash_dash.game_logic import DashDashGame
# from game.snake_game.game_logic import SnakeGame  # Future
# from game.pong.game_logic import PongGame         # Future


# Registry of all available games
AVAILABLE_GAMES = {
    "dash_dash": {
        "name": "Dash Dash",
        "class": DashDashGame,
        "multiplayer": True,
        "singleplayer": False,
        "description": "Multiplayer movement game"
    },
    # Future games:
    # "snake": {
    #     "name": "Snake",
    #     "class": SnakeGame,
    #     "multiplayer": True,
    #     "singleplayer": True,
    #     "description": "Classic snake game"
    # },
}


def get_game(game_id):
    """Get game class by ID."""
    return AVAILABLE_GAMES.get(game_id)


def get_multiplayer_games():
    """Get list of games that support multiplayer."""
    return {k: v for k, v in AVAILABLE_GAMES.items() if v["multiplayer"]}


def get_singleplayer_games():
    """Get list of games that support singleplayer."""
    return {k: v for k, v in AVAILABLE_GAMES.items() if v["singleplayer"]}
```

---

## 🔧 Updated Main.py

```python
from game.game_registry import get_game

def _start_multiplayer_game(self, client, is_host):
    """Start multiplayer game."""
    # Get current game (for now, always dash_dash)
    game_info = get_game("dash_dash")
    
    if not game_info:
        print("Game not found!")
        return
    
    # Create game instance
    game_class = game_info["class"]
    game_screen = game_class(
        self.screen,
        self.config,
        client,
        is_host,
        lambda: self._exit_multiplayer_game()
    )
    
    # Add to screens and switch
    self.screens['game'] = game_screen
    self._change_screen('game')
```

---

## 🚀 Adding a New Game

### **Step 1: Create Game Folder**
```bash
mkdir game/new_game
mkdir game/new_game/screens
```

### **Step 2: Create Files**

**game/new_game/__init__.py:**
```python
"""New Game module."""
```

**game/new_game/constants.py:**
```python
"""Game-specific constants."""

PLAYER_SIZE = 30
GAME_SPEED = 10
# ... other constants
```

**game/new_game/game_logic.py:**
```python
from game.base_game import BaseGame

class NewGame(BaseGame):
    @property
    def game_name(self):
        return "New Game"
    
    @property
    def supports_multiplayer(self):
        return True
    
    # ... implement other methods
```

### **Step 3: Register Game**

Add to `game/game_registry.py`:
```python
from game.new_game.game_logic import NewGame

AVAILABLE_GAMES = {
    # ... existing games
    "new_game": {
        "name": "New Game",
        "class": NewGame,
        "multiplayer": True,
        "singleplayer": True,
        "description": "A cool new game"
    }
}
```

### **Step 4: Done!**

Game is now available and can be launched!

---

## 📋 Migration Plan (For Later)

When you're ready to restructure:

1. **Create new structure:**
   ```bash
   mkdir game/dash_dash
   mkdir game/dash_dash/screens
   ```

2. **Move files:**
   ```
   game/constants.py → game/dash_dash/constants.py
   gui/screens/game_screen.py → game/dash_dash/screens/game_screen.py
   ```

3. **Create new files:**
   - `game/base_game.py`
   - `game/game_registry.py`
   - `game/dash_dash/game_logic.py`

4. **Update imports** in main.py and other files

5. **Test** that everything still works

6. **Add new games** by copying the structure!

---

## 💡 Benefits

✅ **Easy to add games** - Just copy folder structure  
✅ **Clean separation** - Each game is self-contained  
✅ **Shared code** - Use base class and multiplayer client  
✅ **Flexible** - Games can be single/multiplayer  
✅ **Scalable** - Add unlimited games  

---

## 🎯 Future: Game Selection Menu

Eventually create a "Game Selection" screen:

```python
class GameSelectionMenu(BaseScreen):
    """Menu to choose which game to play."""
    
    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.games = get_multiplayer_games()  # or get_singleplayer_games()
        self._build_ui()
    
    def _build_ui(self):
        # Create button for each available game
        for game_id, game_info in self.games.items():
            button = Button(
                game_info["name"],
                rect,
                lambda gid=game_id: self._start_game(gid)
            )
            self.add_button(button)
```

This is the foundation for a multi-game system! 🎮
