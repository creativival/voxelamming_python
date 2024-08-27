## voxelamming

This Python library converts Python code into JSON format and sends it to the Voxelamming app using WebSockets, allowing users to create 3D voxel models by writing Python scripts.

## What's Voxelamming?

<p align="center"><img src="https://creativival.github.io/voxelamming/image/voxelamming_icon.png" alt="Voxelamming Logo" width="200"/></p>

Voxelamming is an AR programming learning app. Even programming beginners can learn programming visually and enjoyably. Voxelamming supports iPhones and iPads with iOS 16 or later, and Apple Vision Pro.

## Resources

* **Homepage:** https://creativival.github.io/voxelamming/index.en
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
from voxelamming import Voxelamming


class Cat:
    def __init__(self, app):
        self.app = app
        self.name = 'cat_8x8'
        self.dot_data = (
            '-1 -1 9 -1 9 -1 -1 -1 -1 -1 9 9 9 9 -1 -1 '
            '-1 -1 9 0 9 0 9 -1 -1 -1 9 9 7 7 7 -1 -1 -1 '
            '9 9 9 -1 -1 -1 9 9 9 9 9 9 9 -1 -1 -1 9 9 7 '
            '-1 -1 -1 -1 9 9 -1 9 9 -1 -1'
        )
        self.direction = 0
        self.x = 0
        self.y = 0
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 8
        self.speed = 0.1  # Speed of the cat's movement
        self.diameter = 4  # Initial size of the cat (diameter of the circle)

    def chase(self, mouse):
        # The cat chases the mouse
        if self.x < mouse.x:
            self.x += self.speed
            self.w = 8
            self.h = 8
            self.direction = 0
        elif self.x > mouse.x:
            self.x -= self.speed
            self.w = -8
            self.h = 8
            self.direction = -180  # Flip the image

        if self.y < mouse.y:
            self.y += self.speed
        elif self.y > mouse.y:
            self.y -= self.speed

        # Gradually increase the size of the cat
        self.diameter += 0.05


class Mouse:
    def __init__(self, app):
        self.app = app
        self.name = 'mouse_8x8'
        self.dot_data = (
            '-1 -1 -1 -1 -1 -1 -1 -1 -1 13 -1 -1 13 -1 -1 -1 '
            '-1 13 13 13 -1 -1 -1 -1 -1 13 13 13 13 0 13 -1 '
            '13 13 13 13 13 13 13 0 -1 13 13 13 13 0 13 -1 '
            '-1 13 13 13 -1 -1 -1 -1 -1 13 -1 -1 13 -1 -1 -1'
        )
        self.direction = 0
        self.x = 20
        self.y = 0
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8
        self.speed = 0.5  # Speed of the mouse's movement
        self.diameter = 8  # Size of the mouse (diameter of the circle)

    def move(self):
        # Move the mouse with arrow keys
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.u = 0
            self.v = 8
            self.w = -8
            self.h = 8
            self.direction = 180  # Rotate 180 degrees
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.u = 0
            self.v = 8
            self.w = 8
            self.h = 8
            self.direction = 0
        if pyxel.btn(pyxel.KEY_UP):
            self.y += self.speed
            self.u = 8
            self.v = 8
            self.w = 8
            self.h = 8
            self.direction = 90
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y -= self.speed
            self.u = 8
            self.v = 8
            self.w = 8
            self.h = -8
            self.direction = -90

        # Limit movement within the screen
        self.x = max(-self.app.window_width // 2, min(self.app.window_width // 2, self.x))
        self.y = max(-self.app.window_height // 2, min(self.app.window_height // 2, self.y))


class App:
    def __init__(self):
        # Initialize Pyxel
        self.dot_size = 1  # Size of the sprite's dots displayed in the AR space (centimeters)
        self.window_width = 64 * 4 / 3  # The width of the AR window will be multiplied by self.dot_size (centimeters)
        self.window_height = 64  # The height of the AR window will be multiplied by self.dot_size (centimeters)
        self.window_angle = 80  # Tilt of the AR window (degrees)
        self.sprite_base_diameter = 8  # Base diameter of the sprite (reference value for sprite sending scale)
        self.cat = Cat(self)
        self.mouse = Mouse(self)
        self.game_started = False
        self.game_over = False
        self.score = 0  # Initial score
        self.last_score_update_time = 0  # Timer to update the score

        # Initialize Voxelamming
        self.vox = Voxelamming('1000')
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0, alpha=0.8)
        self.vox.set_game_score(self.score)
        cat_scale = self.cat.diameter / self.sprite_base_diameter
        mouse_scale = self.mouse.diameter / self.sprite_base_diameter
        self.vox.create_sprite(self.cat.name, self.cat.dot_data, self.cat.x, self.cat.y, self.cat.direction, cat_scale,
                               True)
        self.vox.create_sprite(self.mouse.name, self.mouse.dot_data, self.mouse.x, self.mouse.y, self.mouse.direction,
                               mouse_scale, True)
        self.vox.send_data()
        self.vox.clear_data()

        pyxel.init(self.window_width, self.window_height, title='Cat Game')

        pyxel.load('my_resource.pyxres')

        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_started:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        self.mouse.move()  # Update the position of the mouse
        self.cat.chase(self.mouse)  # The cat chases the mouse

        # Collision detection: Game over when the cat's circle touches the mouse
        if ((self.cat.x - self.mouse.x) ** 2 + (self.cat.y - self.mouse.y) ** 2) < (
                self.cat.diameter / 2 + self.mouse.diameter / 2) ** 2:
            self.game_over = True

            # Send game over (change the window to red)
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=0, blue=0, alpha=0.8)
            self.vox.set_game_score(self.score)
            self.vox.set_command('gameOver')
            self.vox.send_data()
            self.vox.clear_data()

        # Add score every second
        if pyxel.frame_count - self.last_score_update_time >= 30:  # Pyxel's default FPS is 30
            self.score += 1
            self.last_score_update_time = pyxel.frame_count

        # Send sprite information every 0.1 seconds
        if pyxel.frame_count - self.last_score_update_time >= 3:  # Pyxel's default FPS is 30
            if not self.game_over:  # Do not send immediately after game over
                self.vox.set_box_size(self.dot_size)
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0, alpha=0.5)
                self.vox.set_game_score(self.score)
                cat_scale = self.cat.diameter / self.sprite_base_diameter
                mouse_scale = self.mouse.diameter / self.sprite_base_diameter
                self.vox.move_sprite(self.cat.name, self.cat.x, self.cat.y, self.cat.direction, cat_scale, True)
                self.vox.move_sprite(self.mouse.name, self.mouse.x, self.mouse.y, self.mouse.direction, mouse_scale, True)
                self.vox.send_data()
                self.vox.clear_data()

    def draw(self):
        pyxel.cls(1)

        # Display the score at the top left
        pyxel.text(2, 2, f"Score: {self.score}", pyxel.COLOR_WHITE)

        if not self.game_started:
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 - 8, "Click to start",
                       pyxel.frame_count % 16)
            self.draw_cursor()  # Draw custom cursor
            return

        if self.game_over:
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 - 8, "Game Over!", pyxel.frame_count % 16)
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 + 8, "Click to start",
                       pyxel.frame_count % 16)
            self.draw_cursor()  # Draw custom cursor
            return

        # Draw a circle that gradually grows larger
        cat_x, cat_y = self.get_sprite_position(self.cat.x, self.cat.y)
        pyxel.circ(cat_x + 4, cat_y + 4, self.cat.diameter / 2, pyxel.COLOR_RED)

        # Draw the cat's sprite
        pyxel.blt(cat_x, cat_y, self.cat.img, self.cat.u, self.cat.v, self.cat.w, self.cat.h, 1)

        # Draw the mouse's sprite
        mouse_x, mouse_y = self.get_sprite_position(self.mouse.x, self.mouse.y)
        pyxel.blt(mouse_x, mouse_y, self.mouse.img, self.mouse.u, self.mouse.v, self.mouse.w, self.mouse.h, 1)

    def get_sprite_position(self, x, y):
        return self.window_width // 2 + x - 4, self.window_height // 2 - y - 4

    def reset_game(self):
        self.score = 0  # Reset score
        self.last_score_update_time = pyxel.frame_count  # Reset timer
        self.cat = Cat(self)  # Initialize the cat (position, size)
        self.mouse = Mouse(self)  # Initialize the mouse (position)
        self.game_started = True
        self.game_over = False

    @staticmethod
    def draw_cursor():
        cursor_x = pyxel.mouse_x
        cursor_y = pyxel.mouse_y
        pyxel.blt(cursor_x - 4, cursor_y - 4, 0, 0, 16, 8, 8, 1)


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
| `create_sprite(sprite_name, color_list, x, y, direction=90, scale=1, visible=True)`        | Creates a sprite. | `sprite_name`: sprite name (string), `color_list`: dot color data (string), `x`, `y`: position (float), `direction`: angle (float), `scale`: scale (float), `visible`: visibility (boolean) |
| `move_sprite(sprite_name, x, y, direction=90, scale=1, visible=True)`                      | Moves a sprite. | `sprite_name`: sprite name (string), `x`, `y`: position (float), `direction`: angle (float), `scale`: scale (float), `visible`: visibility (boolean)                                  |

## Notes

- Ensure that the Voxelamming app is running and connected to the same room name specified in your Python script.
- This library requires Python 3.9 or higher. 
- Executing arbitrary Python code can be a security risk. Be cautious when running code from untrusted sources. 

This library is under active development. More features and improvements are planned for future releases. 

## License

[MIT License](https://github.com/creativival/voxelamming/blob/master/LICENSE)

## Author

creativival