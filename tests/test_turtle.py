import pytest
from unittest.mock import MagicMock
from voxelamming import Turtle


@pytest.fixture
def voxelamming_mock():
    return MagicMock()

@pytest.fixture
def turtle(voxelamming_mock):
    return Turtle(voxelamming_mock)

def test_init(turtle):
    assert turtle.voxelamming is not None
    assert turtle.x == 0
    assert turtle.y == 0
    assert turtle.z == 0
    assert turtle.polar_theta == 90
    assert turtle.polar_phi == 0
    assert turtle.drawable is True
    assert turtle.color == [0, 0, 0, 1]
    assert turtle.size == 1

def test_forward(turtle):
    turtle.forward(1)
    assert turtle.x == 0.0
    assert turtle.y == 0.0
    assert turtle.z == 1.0
    turtle.voxelamming.draw_line.assert_called_once_with(0, 0, 0, 0.0, 0.0, 1.0, 0, 0, 0, 1)

def test_backward(turtle):
    turtle.backward(1)
    assert turtle.x == 0.0
    assert turtle.y == -0.0
    assert turtle.z == -1.0
    turtle.voxelamming.draw_line.assert_called_once_with(0, 0, 0, 0.0, -0.0, -1.0, 0, 0, 0, 1)

def test_up(turtle):
    turtle.up(30)
    assert turtle.polar_theta == 60

def test_down(turtle):
    turtle.down(30)
    assert turtle.polar_theta == 120

def test_right(turtle):
    turtle.right(30)
    assert turtle.polar_phi == -30

def test_left(turtle):
    turtle.left(30)
    assert turtle.polar_phi == 30

def test_set_color(turtle):
    turtle.set_color(1, 0, 0, 0.5)
    assert turtle.color == [1, 0, 0, 0.5]

def test_pen_down(turtle):
    turtle.pen_down()
    assert turtle.drawable is True

def test_pen_up(turtle):
    turtle.pen_up()
    assert turtle.drawable is False

def test_set_pos(turtle):
    turtle.set_pos(1, 2, 3)
    assert turtle.x == 1
    assert turtle.y == 2
    assert turtle.z == 3

def test_reset(turtle):
    turtle.x = 1
    turtle.y = 2
    turtle.z = 3
    turtle.polar_theta = 45
    turtle.polar_phi = 45
    turtle.drawable = False
    turtle.color = [1, 1, 1, 1]
    turtle.reset()
    assert turtle.x == 0
    assert turtle.y == 0
    assert turtle.z == 0
    assert turtle.polar_theta == 90
    assert turtle.polar_phi == 0
    assert turtle.drawable is True
    assert turtle.color == [0, 0, 0, 1]
    assert turtle.size == 1

