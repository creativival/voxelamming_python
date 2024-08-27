import pytest
from voxelamming import Voxelamming

# テスト用の仮のルーム名
TEST_ROOM_NAME = "test_room"


@pytest.fixture
def voxelamming():
    return Voxelamming(TEST_ROOM_NAME)


def test_init(voxelamming):
    assert voxelamming.room_name == TEST_ROOM_NAME
    assert voxelamming.is_allowed_matrix == 0
    assert voxelamming.saved_matrices == []
    assert voxelamming.node_transform == [0, 0, 0, 0, 0, 0]
    assert voxelamming.matrix_transform == [0, 0, 0, 0, 0, 0]
    assert voxelamming.frame_transforms == []
    assert voxelamming.global_animation == [0, 0, 0, 0, 0, 0, 1, 0]
    assert voxelamming.animation == [0, 0, 0, 0, 0, 0, 1, 0]
    assert voxelamming.boxes == []
    assert voxelamming.frames == []
    assert voxelamming.sentences == []
    assert voxelamming.lights == []
    assert voxelamming.commands == []
    assert voxelamming.size == 1
    assert voxelamming.shape == 'box'
    assert voxelamming.is_metallic == 0
    assert voxelamming.roughness == 0.5
    assert voxelamming.is_allowed_float == 0
    assert voxelamming.build_interval == 0.01
    assert voxelamming.is_framing is False
    assert voxelamming.frame_id == 0


def test_clear_data(voxelamming):
    voxelamming.is_allowed_matrix = 1
    voxelamming.saved_matrices.append([1, 2, 3])
    voxelamming.node_transform = [1, 2, 3, 4, 5, 6]
    # ... 他の属性も適当な値を設定
    voxelamming.clear_data()
    assert voxelamming.is_allowed_matrix == 0
    assert voxelamming.saved_matrices == []
    assert voxelamming.node_transform == [0, 0, 0, 0, 0, 0]
    # ... 他の属性も初期値に戻っていることを確認


def test_set_frame_fps(voxelamming):
    voxelamming.set_frame_fps(fps=10)
    assert voxelamming.commands == ['fps 10']


def test_set_frame_repeats(voxelamming):
    voxelamming.set_frame_repeats(repeats=5)
    assert voxelamming.commands == ['repeats 5']


def test_frame_in_out(voxelamming):
    voxelamming.frame_in()
    assert voxelamming.is_framing is True
    voxelamming.frame_out()
    assert voxelamming.is_framing is False
    assert voxelamming.frame_id == 1


def test_push_pop_matrix(voxelamming):
    voxelamming.matrix_transform = [1, 2, 3, 4, 5, 6]
    voxelamming.push_matrix()
    assert voxelamming.is_allowed_matrix == 1
    assert voxelamming.saved_matrices == [[1, 2, 3, 4, 5, 6]]
    voxelamming.matrix_transform = [7, 8, 9, 10, 11, 12]
    voxelamming.pop_matrix()
    assert voxelamming.is_allowed_matrix == 0
    assert voxelamming.matrix_transform == [1, 2, 3, 4, 5, 6]


def test_transform_without_matrix(voxelamming):
    voxelamming.transform(1, 2, 3, 4, 5, 6)
    assert voxelamming.node_transform == [1, 2, 3, 4, 5, 6]


# def test_transform_with_matrix(voxelamming):
#     voxelamming.push_matrix()
#     voxelamming.transform(1, 2, 3, 4, 5, 6)
#     # マトリックス変換を含めた最終的なtransformの値を検証する
#     # 必要であれば、matrix_util.pyの関数を使用して変換を行う
#     assert voxelamming.matrix_transform == [1, 2, 3, 0.2533807407753403, -0.6599836364963772, 0.7065879772298925, 0.6599836364963772, 0.75, 0.03675515622762612, -0.7065879772298925, 0.03675515622762612, 0.7075178667557078]

def test_create_box_without_matrix(voxelamming):
    voxelamming.create_box(1, 2, 3, r=0.5, g=0.6, b=0.7, alpha=0.8, texture="grass")
    assert voxelamming.boxes == [[1, 2, 3, 0.5, 0.6, 0.7, 0.8, 0]]


# def test_create_box_with_matrix(voxelamming):
#     voxelamming.push_matrix()
#     voxelamming.transform(1, 2, 3, 4, 5, 6)
#     voxelamming.create_box(1, 2, 3, r=0.5, g=0.6, b=0.7, alpha=0.8, texture="grass")
#     # マトリックス変換を含めた最終的なboxesの値を検証する
#     # 必要であれば、matrix_util.pyの関数を使用して変換を行う
#     assert voxelamming.boxes == [[2.0, 4.0, 6.0, 0.5, 0.6, 0.7, 0.8, 0]]

def test_remove_box(voxelamming):
    voxelamming.create_box(1, 2, 3)
    voxelamming.remove_box(1, 2, 3)
    assert voxelamming.boxes == []


def test_animate_global(voxelamming):
    voxelamming.animate_global(1, 2, 3, 4, 5, 6, 0.5, 20)
    assert voxelamming.global_animation == [1, 2, 3, 4, 5, 6, 0.5, 20]


def test_animate(voxelamming):
    voxelamming.animate(1, 2, 3, 4, 5, 6, 0.5, 20)
    assert voxelamming.animation == [1, 2, 3, 4, 5, 6, 0.5, 20]


def test_set_box_size(voxelamming):
    voxelamming.set_box_size(2)
    assert voxelamming.size == 2


def test_set_build_interval(voxelamming):
    voxelamming.set_build_interval(0.5)
    assert voxelamming.build_interval == 0.5


def test_write_sentence(voxelamming):
    voxelamming.write_sentence("Hello", 1, 2, 3, r=0.1, g=0.2, b=0.3, alpha=0.4)
    assert voxelamming.sentences == [['Hello', '1', '2', '3', '0.1', '0.2', '0.3', '0.4', '16', '0']]


def test_set_light(voxelamming):
    voxelamming.set_light(1, 2, 3, r=0.1, g=0.2, b=0.3, alpha=0.4, intensity=500, interval=2, light_type="spot")
    assert voxelamming.lights == [[1, 2, 3, 0.1, 0.2, 0.3, 0.4, 500, 2, 2]]


def test_set_command(voxelamming):
    voxelamming.set_command("float")
    assert voxelamming.commands == ["float"]
    assert voxelamming.is_allowed_float == 1


def test_draw_line(voxelamming):
    voxelamming.draw_line(0, 0, 0, 5, 0, 0)
    assert voxelamming.boxes == [[0, 0, 0, 1, 1, 1, 1, -1], [1, 0, 0, 1, 1, 1, 1, -1], [2, 0, 0, 1, 1, 1, 1, -1],
                               [3, 0, 0, 1, 1, 1, 1, -1], [4, 0, 0, 1, 1, 1, 1, -1], [5, 0, 0, 1, 1, 1, 1, -1]]


def test_change_shape(voxelamming):
    voxelamming.change_shape("sphere")
    assert voxelamming.shape == "sphere"


def test_change_material(voxelamming):
    voxelamming.change_material(is_metallic=True, roughness=0.2)
    assert voxelamming.is_metallic == 1
    assert voxelamming.roughness == 0.2


def test_round_numbers_with_float(voxelamming):
    voxelamming.is_allowed_float = 1
    assert voxelamming.round_numbers([1.234, 2.345, 3.456]) == [1.23, 2.35, 3.46]


def test_round_numbers_without_float(voxelamming):
    assert voxelamming.round_numbers([1.234, 2.345, 3.456]) == [1, 2, 3]


def test_round_two_decimals(voxelamming):
    assert voxelamming.round_two_decimals([0.123, 0.234, 0.345, 0.456]) == [0.12, 0.23, 0.34, 0.46]

# send_data関数は、実際にWebSocket通信を行うため、モックを使用するなどの対応が必要
# ここでは、send_data関数の呼び出しを確認するだけのテストとする

# def test_send_data(mocker, voxelamming):
#    mock_websocket = mocker.patch('websockets.connect')
#    voxelamming.send_data(name="test_model")
#    mock_websocket.assert_called_once_with('wss://websocket.voxelamming.com')
