import numpy as np
from scipy.spatial.transform import Rotation


def get_translation_matrix(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ], dtype=np.float32)


def get_scale_matrix(sx, sy, sz):
    print("get_scale_matrix")
    return np.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1]
    ], dtype=np.float32)


def get_rotation_matrix(axis, angle_degrees):
    angle = np.radians(angle_degrees)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    # Matrizes de rotação em torno dos eixos x, y e z
    if axis == 'x':
        return np.array([
            [1, 0, 0, 0],
            [0, cos_a, -sin_a, 0],
            [0, sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
    elif axis == 'y':
        return np.array([
            [cos_a, 0, sin_a, 0],
            [0, 1, 0, 0],
            [-sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
    elif axis == 'z':
        return np.array([
            [cos_a, -sin_a, 0, 0],
            [sin_a,  cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
    else:
        raise ValueError("Eixo deve ser 'x', 'y' ou 'z'")


def create_transformation(transformations):
    """
    Cria uma matriz de transformação composta a partir de uma lista de transformações.
    """
    result = np.identity(4, dtype=np.float32)

    for transform in transformations:
        if transform['type'] == 'Translação':
            dx, dy, dz = transform['params']
            matrix = get_translation_matrix(dx, dy, dz)
        elif transform['type'] == 'Rotação':
            axis, angle = transform['params']
            matrix = get_rotation_matrix(axis, angle)
        elif transform['type'] == 'Escala':
            sx, sy, sz = transform['params']
            matrix = get_scale_matrix(sx, sy, sz)
        else:
            continue  # Tipo de transformação desconhecido ignora

        result = matrix @ result

    return result
