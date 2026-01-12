# 🚀 Update Guide - New Features

## ✨ What's New

### **1. Number-based Movement System**
- ✅ Movement sent as numbers (0-4) instead of WASD booleans
- ✅ More efficient network traffic
- ✅ Easier to extend (can add more movement types)

```
0 = No movement
1 = Up (W / Arrow Up)
2 = Down (S / Arrow Down)  
3 = Left (A / Arrow Left)
4 = Right (D / Arrow Right)
```

### **2. Server Configuration**
- ✅ Config file: `server/server_config.yaml`
- ✅ Command-line arguments support
- ✅ Auto-creates default config
- ✅ Can save CLI args to config

### **3. Improved Game UI**
- ✅ Player list shows actual usernames
- ✅ "You" indicator next to your name
- ✅ Shows player count
- ✅ UI areas separated from play area
- ✅ No text overlapping game field

### **4. Snake-style Wrapping**
- ✅ Go off left edge → appear on right
- ✅ Go off top edge → appear on bottom
- ✅ Smooth wrapping behavior

---

## 📁 New Files to Add

```
game/constants.py           ← NEW (shared constants)
server/server_config.py     ← NEW (server config manager)
```

## 📝 Files to Update

```
server/game_server.py       ← REPLACE (config + number movement)
game/multiplayer/client.py  ← UPDATE (number movement)
gui/screens/game_screen.py  ← REPLACE (wrapping + better UI)
game/__init__.py            ← UPDATE
server/__init__.py          ← UPDATE
```

---

## 🔧 Setup Instructions

### **Step 1: Add New Files**

Create these files in your project:

1. **`game/constants.py`** - Copy from artifact
2. **`server/server_config.py`** - Copy from artifact

### **Step 2: Update Existing Files**

Replace/update these files:

1. **`server/game_server.py`**
2. **`game/multiplayer/client.py`** (only the `send_input` method)
3. **`gui/screens/game_screen.py`**
4. **`game/__init__.py`**
5. **`server/__init__.py`**

---

## 🎮 Testing

### **Test 1: Server with Config**

```bash
# Start with defaults (creates config file)
python server/game_server.py
```

**Expected output:**
```
╔════════════════════════════════════════╗
║       DASH DASH - GAME SERVER         ║
╔════════════════════════════════════════╗

Usage:
  python game_server.py                    # Use config/defaults
  python game_server.py -H 0.0.0.0 -p 5000 # Override settings
  python game_server.py -p 8080 --save     # Save to config

======================================================================
[STARTED] Dash Dash Game Server
======================================================================
  Host: 0.0.0.0
  Port: 50000
  Max Players: 8
  Config: server/server_config.yaml
======================================================================
Waiting for connections...
```

### **Test 2: Server with Custom Port**

```bash
# Use custom port
python server/game_server.py -p 8080

# Save custom settings
python server/game_server.py -p 8080 --save
```

### **Test 3: Game with New UI**

1. Start server
2. Start 2+ clients
3. Connect and join game
4. **Check UI:**
   - ✅ Top left shows "DASH DASH - HOST" or "CLIENT"
   - ✅ Player list shows actual usernames
   - ✅ Your name has "(You)" next to it
   - ✅ Player count shown
   - ✅ Bottom shows controls
   - ✅ No text in game field

### **Test 4: Snake Wrapping**

1. In game, move to left edge
2. Keep moving left
3. **Expected:** Player appears on right edge
4. Test all 4 edges

---

## 📊 Server Config File

After first run, check `server/server_config.yaml`:

```yaml
host: 0.0.0.0
max_players: 8
player_speed: 5
port: 50000
spawn_x: 400
spawn_y: 300
```

You can edit this file directly or use command-line arguments.

---

## 🎯 Command-Line Examples

```bash
# Default (reads from config)
python server/game_server.py

# Custom port
python server/game_server.py -p 8080

# Custom host and port
python server/game_server.py -H 127.0.0.1 -p 5000

# Set max players
python server/game_server.py -m 4

# Save settings to config
python server/game_server.py -p 8080 -m 4 --save

# Help
python server/game_server.py --help
```

---

## 🐛 Troubleshooting

### **Issue: Port already in use**

```
[ERROR] Failed to bind to 0.0.0.0:50000
[ERROR] [Errno 98] Address already in use
```

**Solution:**
```bash
# Use different port
python server/game_server.py -p 50001
```

### **Issue: Config file not found**

**Solution:** It will auto-create. Just make sure `server/` folder exists.

### **Issue: Players not wrapping**

**Check:**
- Are you using the updated `game_screen.py`?
- Is `game/constants.py` created?

### **Issue: Names not showing**

**Check:**
- Is username set in Settings menu?
- Is `game/constants.py` imported correctly?

---

## 📋 Feature Checklist

After updating, verify:

- [ ] Server starts with config file
- [ ] Server accepts `-p` argument
- [ ] Config file created in `server/`
- [ ] Player names show in game
- [ ] Your name has "(You)" indicator
- [ ] Player count displays correctly
- [ ] UI areas don't overlap game field
- [ ] Snake wrapping works on all edges
- [ ] Movement still smooth
- [ ] Multiple players see each other

---

## 🎨 UI Layout

```
┌────────────────────────────────────────┐
│ DASH DASH - HOST                       │ ← UI_TOP_HEIGHT (120px)
│ Players (2):                           │
│   • Player1 (You)                      │
│   • Player2                            │
├────────────────────────────────────────┤
│                                        │
│         [Game Play Area]               │ ← Play area
│                                        │   (wrapping enabled)
│                                        │
├────────────────────────────────────────┤
│ Controls: WASD / Arrows | ESC to exit │ ← UI_BOTTOM_HEIGHT (40px)
└────────────────────────────────────────┘
```

---

## 🚀 Next Features (After This Works)

1. **Lobby System**
   - Host creates lobby with name
   - Join shows list of lobbies
   - Lobby browser screen

2. **Better Player Spawning**
   - Random spawn positions
   - Avoid spawning on other players

3. **Game Boundaries Visual**
   - Show play area border
   - Different background color

4. **Player Colors**
   - Customizable player colors
   - More distinct colors for multiple players

5. **Collision Detection**
   - Players can't overlap
   - Add game mechanics

---

## 💡 Tips

**For Server:**
- Run on dedicated machine for best performance
- Use `0.0.0.0` to accept connections from any IP
- Use `127.0.0.1` for localhost-only testing

**For Testing:**
- Test with 2+ clients to see wrapping sync
- Try moving near edges to test wrapping
- Check that names update in real-time

**For Development:**
- Edit `game/constants.py` to change game parameters
- Edit `server/server_config.yaml` to change server defaults
- Use `--save` flag to persist CLI arguments

---

Let me know how it goes! 🎮
