import pytest
from math import radians, sin, cos, isclose
from voxelamming import get_rotation_matrix, matrix_multiply, transform_point_by_rotation_matrix, add_vectors, transpose_3x3

@pytest.mark.parametrize("pitch, yaw, roll, expected_matrix", [
    (0, 0, 0, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    (90, 0, 0, [[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
    (0, 90, 0, [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
    (0, 0, 90, [[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
])
def test_get_rotation_matrix(pitch, yaw, roll, expected_matrix):
    R = get_rotation_matrix(pitch, yaw, roll)
    for i in range(3):
        for j in range(3):
            # 絶対許容誤差を1e-6に設定
            assert isclose(R[i][j], expected_matrix[i][j], rel_tol=1e-6, abs_tol=1e-6)

def test_matrix_multiply():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    expected_C = [[30, 24, 18], [84, 69, 54], [138, 114, 90]]  # 期待値を変更
    C = matrix_multiply(A, B)
    assert C == expected_C

def test_transform_point_by_rotation_matrix():
    point = [1, 2, 3]
    R = [[1, 0, 0], [0, 0, -1], [0, 1, 0]] # 90度回転行列 (X軸周り)
    expected_new_point = [1, -3, 2]
    new_point = transform_point_by_rotation_matrix(point, R)
    assert all(isclose(a, b, rel_tol=1e-6) for a, b in zip(new_point, expected_new_point)) # reltol を rel_tol に修正

def test_add_vectors():
    vector1 = [1, 2, 3]
    vector2 = [4, 5, 6]
    expected_sum = [5, 7, 9]
    sum = add_vectors(vector1, vector2)
    assert sum == expected_sum

def test_transpose_3x3():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected_transposed = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    transposed = transpose_3x3(matrix)
    assert transposed == expected_transposed