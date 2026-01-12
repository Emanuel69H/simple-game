"""
Game Constants
Shared constants between client and server.
"""

# Movement directions (bitwise flags for diagonal movement)
MOVE_NONE = 0
MOVE_UP = 1      # 0001
MOVE_DOWN = 2    # 0010
MOVE_LEFT = 4    # 0100
MOVE_RIGHT = 8   # 1000

# Diagonal combinations
MOVE_UP_LEFT = MOVE_UP | MOVE_LEFT       # 0101 = 5
MOVE_UP_RIGHT = MOVE_UP | MOVE_RIGHT     # 1001 = 9
MOVE_DOWN_LEFT = MOVE_DOWN | MOVE_LEFT   # 0110 = 6
MOVE_DOWN_RIGHT = MOVE_DOWN | MOVE_RIGHT # 1010 = 10

# Direction names (for debugging)
DIRECTION_NAMES = {
    MOVE_NONE: "None",
    MOVE_UP: "Up",
    MOVE_DOWN: "Down",
    MOVE_LEFT: "Left",
    MOVE_RIGHT: "Right",
    MOVE_UP_LEFT: "Up-Left",
    MOVE_UP_RIGHT: "Up-Right",
    MOVE_DOWN_LEFT: "Down-Left",
    MOVE_DOWN_RIGHT: "Down-Right"
}

# Game settings
PLAYER_SIZE = 40
PLAYER_SPEED = 5
PLAYER_SPEED_DIAGONAL = 3.5  # Slightly slower diagonal to balance
INITIAL_X = 400
INITIAL_Y = 300

# UI Layout
UI_TOP_HEIGHT = 120      # Height of top UI area (title + player list)
UI_BOTTOM_HEIGHT = 40    # Height of bottom UI area (controls)
UI_SIDE_MARGIN = 10      # Left/right margin

# Colors
COLOR_SELF = (0, 200, 255)       # Blue for own player
COLOR_OTHER = (200, 100, 50)     # Orange for other players
COLOR_BG = (30, 30, 30)          # Dark gray background
COLOR_UI_BG = (20, 20, 20)       # Darker gray for UI areas
COLOR_TEXT = (255, 255, 255)     # White text
COLOR_TEXT_DIM = (150, 150, 150) # Gray text
