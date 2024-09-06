## voxelamming

This Python library converts Python code into JSON format and sends it to the Voxelamming app using WebSockets, allowing users to create 3D voxel models by writing Python scripts.

## What's Voxelamming?

<p align="center"><img src="https://creativival.github.io/voxelamming/image/voxelamming_icon.png" alt="Voxelamming Logo" width="200"/></p>

Voxelamming is an AR programming learning app. Even programming beginners can learn programming visually and enjoyably. Voxelamming supports iPhones and iPads with iOS 16 or later, and Apple Vision Pro.

## Resources

* **Homepage:** https://creativival.github.io/voxelamming_python
* **Samples:** https://github.com/creativival/voxelamming/tree/main/sample/python

## Installation

```bash
pip install voxelamming
```

## Usage

### Modeling

```python
from voxelamming import Voxelamming

# Set your room name. This should match the room name displayed in your Voxelamming app. 
room_name = "1000"

# Create a Voxelamming instance
voxelamming = Voxelamming(room_name)

# Define Python code to create a voxel model
voxelamming.set_box_size(0.5)
voxelamming.set_build_interval(0.01)
voxelamming.transform(0, 0, 0, pitch=0, yaw=0, roll=0)
voxelamming.animate(0, 0, 10, pitch=0, yaw=30, roll=0, scale=2, interval= 10)

for i in range(100):
  voxelamming.create_box(-1, i, 0, r=0, g=1, b=1)
  voxelamming.create_box(0, i, 0, r=1, g=0, b=0)
  voxelamming.create_box(1, i, 0, r=1, g=1, b=0)
  voxelamming.create_box(2, i, 0, r=0, g=1, b=1)

for i in range(50):
  voxelamming.remove_box(0, i * 2 + 1, 0)
  voxelamming.remove_box(1, i * 2, 0)

# Send the Python code to the Voxelamming app
voxelamming.send_data()
```

### Game Mode

```python
import pyxel
import time
import random
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # Use this when developing locally


class Player:
    name = 'spaceship_8x8'
    dot_data = (
        '-1 -1 -1 8 8 -1 -1 -1 -1 -1 3 7 7 3 -1 -1 -1 -1 -1 7 7 -1 -1 -1 -1 -1 7 7 7 7 -1 -1 -1 7 7 7 7 7 7 -1 3 7'
        ' 7 7 7 7 7 3 -1 8 8 7 7 8 8 -1 -1 -1 -1 8 8 -1 -1 -1'
    )

    def __init__(self, x, y, speed):
        self.direction = 0
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 8
        self.speed = speed

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed


class Enemy:
    name = 'enemy_8x8'
    dot_data = (
        '-1 -1 3 -1 -1 3 -1 -1 -1 3 -1 3 3 -1 3 -1 3 -1 3 3 3 3 -1 3 3 3 3 3 3 3 3 3 3 3 -1 3 3 -1 3 3 3 3 3 3 3 3'
        ' 3 3 -1 3 3 -1 -1 3 3 -1 3 -1 -1 -1 -1 -1 -1 3'
    )

    def __init__(self, x, y):
        self.direction = 0
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8


class Missile:
    def __init__(self, x, y, color_id, direction=0, width=1, height=1):
        self.x = x
        self.y = y
        self.direction = direction
        self.color_id = color_id
        self.width = width
        self.height = height


class App:
    def __init__(self):
        # Pyxel settings
        self.window_width = 160  # The width of the AR window becomes the value multiplied by self.dot_size (in centimeters)
        self.window_height = 120  # The height of the AR window becomes the value multiplied by self.dot_size (in centimeters)
        self.score = 0
        self.game_over = False
        self.game_clear = False

        # Player settings
        self.player = Player(self.window_width // 2, self.window_height - 10, 2)
        self.missiles = []
        self.player_missile_speed = 2

        # Enemy settings
        self.enemy_rows = 3
        self.enemy_cols = 6
        self.enemy_speed = 1
        self.enemy_direction = 1
        self.enemies = []
        self.enemy_missiles = []
        self.enemy_missile_speed = 2

        # Initialize enemies
        for row in range(self.enemy_rows):
            for col in range(self.enemy_cols):
                enemy_x = col * 16 + 20
                enemy_y = row * 12 + 20
                enemy = Enemy(enemy_x, enemy_y)
                self.enemies.append(enemy)

        # Voxelamming settings (executed before Pyxel initialization)
        self.dot_size = 1  # The size of the sprite dots displayed in the AR space (in centimeters)
        self.window_angle = 80  # Tilt angle of the AR window (in degrees)
        self.vox = Voxelamming('1000')
        self.init_voxelamming()

        # Pyxel initialization
        pyxel.init(self.window_width, self.window_height, title="Pyxel Invader Game", fps=30)
        pyxel.mouse(True)
        pyxel.load("invader_game.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            # Show cursor
            pyxel.mouse(True)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        # Hide cursor
        pyxel.mouse(False)

        # Player controls
        self.player.update()

        if pyxel.btnp(pyxel.KEY_SPACE):
            missile_x = self.player.x + self.player_missile_speed
            missile_y = self.player.y
            missile_clor_id = 10  # Blue
            missile_direction = 0
            missile_width = 2
            missile_height = 4
            self.missiles.append(
                Missile(missile_x, missile_y, missile_clor_id, missile_direction, missile_width, missile_height))

        # Move missiles
        for missile in self.missiles[:]:
            missile.y -= 2
            if missile.y < 0:
                self.missiles.remove(missile)

        # Move enemies
        move_down = False
        for enemy in self.enemies:
            enemy.x += self.enemy_speed * self.enemy_direction

        for enemy in self.enemies:
            if enemy.x > pyxel.width - 8 or enemy.x < 0:
                self.enemy_direction *= -1
                move_down = True
                break  # Change direction immediately when reaching the edge

        if move_down:
            for enemy in self.enemies:
                enemy.y += 8

                # Game over if the enemy reaches the bottom of the screen
                if enemy.y > pyxel.height - 16:
                    self.game_over = True

        # Enemy missile firing
        if random.random() < 0.03 and self.enemies:
            shooting_enemy = random.choice(self.enemies)
            missile_x = shooting_enemy.x + 4
            missile_y = shooting_enemy.y + 8
            missile_clor_id = 8  # Red
            missile_direction = 0
            missile_width = 2
            missile_height = 4
            self.enemy_missiles.append(
                Missile(missile_x, missile_y, missile_clor_id, missile_direction, missile_width, missile_height))

        # Move enemy missiles
        for missile in self.enemy_missiles[:]:
            missile.y += self.enemy_missile_speed
            if missile.y > pyxel.height * 2:
                self.enemy_missiles.remove(missile)

        # Collision detection between missiles and enemies
        for missile in self.missiles[:]:
            for enemy in self.enemies[:]:
                if (enemy.x < missile.x < enemy.x + 16 and
                        enemy.y < missile.y < enemy.y + 12):
                    self.missiles.remove(missile)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

        # Collision detection between player and enemy missiles
        for missile in self.enemy_missiles[:]:
            if (self.player.x < missile.x < self.player.x + 8 and
                    self.player.y < missile.y < self.player.y + 8):
                self.game_over = True

        # Collision detection between player and enemies
        for enemy in self.enemies:
            if (self.player.x < enemy.x < self.player.x + 8 and
                    self.player.y < enemy.y < self.player.y + 8):
                self.game_over = True

        # Check for game clear
        if not self.enemies:
            self.game_clear = True

        # Update Voxelamming
        self.update_voxelamming()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 4, f"Score: {self.score}", 7)

        if self.game_clear:
            pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2, "GAME CLEAR!", pyxel.frame_count % 16)
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 + 8, "Click to start",
                       pyxel.frame_count % 16)
        elif self.game_over:
            pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 + 8, "Click to start",
                       pyxel.frame_count % 16)
        else:
            # Draw player
            pyxel.blt(self.player.x, self.player.y, self.player.img, self.player.u, self.player.v, self.player.w,
                      self.player.h, 0)

            # Draw enemies
            for enemy in self.enemies:
                pyxel.blt(enemy.x, enemy.y, enemy.img, enemy.u, enemy.v, enemy.w, enemy.h, 0)

            # Draw missiles
            for missile in self.missiles:
                pyxel.rect(missile.x, missile.y, missile.width, missile.height, missile.color_id)

            # Draw enemy missiles
            for missile in self.enemy_missiles:
                pyxel.rect(missile.x, missile.y, missile.width, missile.height, missile.color_id)

    def reset_game(self):
        self.score = 0  # Reset score
        self.game_over = False
        self.game_clear = False

        # Player settings
        self.player = Player(self.window_width // 2, self.window_height - 10, 2)
        self.missiles = []

        # Enemy settings
        self.enemy_rows = 3
        self.enemy_cols = 6
        self.enemy_speed = 1
        self.enemy_direction = 1
        self.enemies = []
        self.enemy_missiles = []
        self.enemy_missile_speed = 2

        # Initialize enemies
        for row in range(self.enemy_rows):
            for col in range(self.enemy_cols):
                enemy_x = col * 16 + 20
                enemy_y = row * 12 + 20
                enemy = Enemy(enemy_x, enemy_y)
                self.enemies.append(enemy)

    def init_voxelamming(self):

        # Initialize Voxelamming
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0,
                                 alpha=0.8)
        self.vox.set_game_score(self.score)

        # Display the player's sprite
        vox_x, vox_y = self.convert_sprite_position_to_voxelamming(self.player.x, self.player.y)
        self.vox.create_sprite(self.player.name, self.player.dot_data, vox_x, vox_y, self.player.direction, 1)

        # Since there are multiple enemies, create a template and display it in multiple locations
        self.vox.create_sprite(Enemy.name, Enemy.dot_data)
        for enemy in self.enemies:
            vox_x, vox_y = self.convert_sprite_position_to_voxelamming(enemy.x, enemy.y)
            self.vox.move_sprite(enemy.name, vox_x, vox_y, enemy.direction, 1)

        self.vox.send_data()
        self.vox.clear_data()

    def update_voxelamming(self):
        # Send sprite information every 0.1 seconds
        if pyxel.frame_count % 3 == 0 or self.game_clear or self.game_over:  # Default Pyxel FPS is 30
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1,
                                     blue=0, alpha=0.5)
            self.vox.set_game_score(self.score, -66, 57)

            # Move sprites
            vox_x, vox_y = self.convert_sprite_position_to_voxelamming(self.player.x, self.player.y)
            self.vox.move_sprite(self.player.name, vox_x, vox_y, self.player.direction, 1)

            # Enemy movement is displayed as templates in multiple locations
            for enemy in self.enemies:
                vox_x, vox_y = self.convert_sprite_position_to_voxelamming(enemy.x, enemy.y)
                self.vox.move_sprite_clone(enemy.name, vox_x, vox_y, enemy.direction, 1)

            # Missiles are displayed as dots
            for missile in self.missiles + self.enemy_missiles:
                vox_x, vox_y = self.convert_dot_position_to_voxelamming(missile.x, missile.y, missile.width, missile.height)
                self.vox.display_dot(vox_x, vox_y, missile.direction, missile.color_id, missile.width,
                                     missile.height)

            # Change the screen to blue and display the game clear
            if self.game_clear:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=0, green=0,
                                         blue=1, alpha=0.8)
                self.vox.set_command('gameClear')

            # Change the screen to red and display game over
            if self.game_over:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=0,
                                         blue=0, alpha=0.8)
                self.vox.set_command('gameOver')

            self.vox.send_data()

            # Wait for 1 second after game clear or game over, then send data again
            if self.game_clear or self.game_over:
                time.sleep(1)
                self.vox.send_data()

            self.vox.clear_data()

    def convert_sprite_position_to_voxelamming(self, x, y):
        return x - self.window_width // 2 + 4, self.window_height // 2 - (y + 4)

    def convert_dot_position_to_voxelamming(self, x, y, width=1, height=1):
        return x - self.window_width // 2 + width / 2, self.window_height // 2 - (y + height / 2)


if __name__ == "__main__":
    App()
```

This code snippet demonstrates a simple example where a red voxel is created at a specific location. You can use various functions provided by the `Voxelamming` class to build more complex models.

#### Method description
| Modeling Method name                                                                                | Description | Arguments |
|--------------------------------------------------------------------------------------------|---|---|
| `set_room_name(room_name)`                                                                 | Sets the room name for communicating with the device. | `room_name`: Room name (string) |
| `set_box_size(size)`                                                                       | Sets the size of the voxel (default: 1.0). | `size`: Size (float) |
| `set_build_interval(interval)`                                                             | Sets the placement interval of the voxels (default: 0.01 seconds). | `interval`: Interval (float) |
| `change_shape(shape)`                                                                      | Changes the shape of the voxel. | `shape`: Shape ("box", "sphere", "plane") |
| `change_material(is_metallic, roughness)`                                                  | Changes the material of the voxel. | `is_metallic`: Whether to make it metallic (boolean), `roughness`: Roughness (float) |
| `create_box(x, y, z, r, g, b, alpha)`                                                      | Places a voxel. | `x`, `y`, `z`: Position (float), `r`, `g`, `b`, `alpha`: Color (float, 0-1) |
| `create_box(x, y, z, texture)`                                                             | Places a voxel with texture. | `x`, `y`, `z`: Position (float), `texture`: Texture name (string) |
| `remove_box(x, y, z)`                                                                      | Removes a voxel. | `x`, `y`, `z`: Position (float) |
| `write_sentence(sentence, x, y, z, r, g, b, alpha)`                                        | Draws a string with voxels. | `sentence`: String (string), `x`, `y`, `z`: Position (float), `r`, `g`, `b`, `alpha`: Color (float, 0-1) |
| `set_light(x, y, z, r, g, b, alpha, intensity, interval, light_type)`                      | Places a light. | `x`, `y`, `z`: Position (float), `r`, `g`, `b`, `alpha`: Color (float, 0-1), `intensity`: Intensity (float), `interval`: Blinking interval (float), `light_type`: Type of light ("point", "spot", "directional") |
| `set_command(command)`                                                                     | Executes a command. | `command`: Command ("axis", "japaneseCastle", "float", "liteRender") |
| `draw_line(x1, y1, z1, x2, y2, z2, r, g, b, alpha)`                                        | Draws a line between two points. | `x1`, `y1`, `z1`: Starting point (float), `x2`, `y2`, `z2`: Ending point (float), `r`, `g`, `b`, `alpha`: Color (float, 0-1) |
| `create_model(model_name, x, y, z, pitch, yaw, roll, scale, entity_name)`                  | Creates a built-in model (USDZ). |  `model_name`: Name of the model (string), `x`, `y`, `z`: Translation values (float), `pitch`, `yaw`, `roll`: Rotation values (float), `scale`: Scale (float), `entity_name`: Name assigned to the created model (string) |
| `move_model(entity_name, x, y, z, pitch, yaw, roll, scale)`                                | Moves the created model (USDZ). |  `entity_name`: Name assigned to the created model (string), `x`, `y`, `z`: Translation values (float), `pitch`, `yaw`, `roll`: Rotation values (float), `scale`: Scale (float) |
| `send_data(name)`                                                                          | Sends voxel data to the device; if the name argument is set, the voxel data can be stored and reproduced as history. | |
| `clear_data()`                                                                             | Initializes voxel data. | |
| `transform(x, y, z, pitch, yaw, roll)`                                                     | Moves and rotates the coordinate system of the voxel. | `x`, `y`, `z`: Translation amount (float), `pitch`, `yaw`, `roll`: Rotation amount (float) |
| `animate(x, y, z, pitch, yaw, roll, scale, interval)`                                      | Animates a voxel. | `x`, `y`, `z`: Translation amount (float), `pitch`, `yaw`, `roll`: Rotation amount (float), `scale`: Scale (float), `interval`: Interval (float) |
| `animate_global(x, y, z, pitch, yaw, roll, scale, interval)`                               | Animates all voxels. | `x`, `y`, `z`: Translation amount (float), `pitch`, `yaw`, `roll`: Rotation amount (float), `scale`: Scale (float), `interval`: Interval (float) |
| `push_matrix()`                                                                            | Saves the current coordinate system to the stack. | |
| `pop_matrix()`                                                                             | Restores the coordinate system from the stack. | |
| `frame_in()`                                                                               | Starts recording a frame. | |
| `frame_out()`                                                                              | Ends recording a frame. | |
| `set_frame_fps(fps)`                                                                       | Sets the frame rate (default: 2). | `fps`: Frame rate (int) |
| `set_frame_repeats(repeats)`                                                               | Sets the number of frame repetitions (default: 10). | `repeats`: Number of repetitions (int) |
| Game Method Name                                                                           | Description | Arguments                                                                                                                                                            |
| `set_game_screen_size(width, height, angle=90, r=1, g=1, b=0, alpha=0.5)`                  | Sets the game screen size. | `width`, `height`: screen size (float), `angle`: angle (float), `r`, `g`, `b`, `alpha`: color (float, 0-1)                                                            |
| `set_game_score(score)`                                                                    | Sets the game score. | `score`: game score (int)                                                                                                                                            |
| `send_game_over()`                                                                         | Triggers game over. |                                                                                                                                                                     |
| `send_game_clear()`                                                                  | Triggers game clear. |                                                                                                                                                                   |
| `create_sprite(sprite_name, color_list, x, y, direction=90, scale=1, visible=True)`        | Creates a sprite. | `sprite_name`: sprite name (string), `color_list`: dot color data (string), `x`, `y`: position (float), `direction`: angle (float), `scale`: scale (float), `visible`: visibility (boolean) |
| `move_sprite(sprite_name, x, y, direction=90, scale=1, visible=True)`                      | Moves a sprite. | `sprite_name`: sprite name (string), `x`, `y`: position (float), `direction`: angle (float), `scale`: scale (float), `visible`: visibility (boolean)                                  |
| `move_sprite_clone(sprite_name, x, y, direction=90, scale=1,)`               | Moves a clone of the sprite. Can be executed multiple times and is used when creating multiple sprites. | `sprite_name`: Sprite name (string), `x`, `y`: Position (float), `direction`: Direction (float), `scale`: Scale (float)                                  |
| `display_dot(sprite_name, x, y, direction=90, scale=1)`               | Used to place multiple dots, such as bullets or particles. | `sprite_name`: Sprite name (string), `x`, `y`: Position (float), `direction`: Direction (float), `scale`: Scale (float)                                  |
| `display_text(sprite_name, x, y, direction=90, scale=1, is_vertical=True)`               | Displays text on the game screen. | `sprite_name`: Sprite name (string), `x`, `y`: Position (float), `direction`: Direction (float), `scale`: Scale (float), `is_vertical`: Vertical display (boolean)                                  |

## Notes

- Ensure that the Voxelamming app is running and connected to the same room name specified in your Python script.
- This library requires Python 3.9 or higher. 
- Executing arbitrary Python code can be a security risk. Be cautious when running code from untrusted sources. 

This library is under active development. More features and improvements are planned for future releases. 

## License

[MIT License](https://github.com/creativival/voxelamming/blob/master/LICENSE)

## Author

creativival