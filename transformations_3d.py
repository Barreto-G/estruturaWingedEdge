import numpy as np
import math
from wingedEdge import Scene

def get_translation_matrix(dx,dy,dz):
    return np.array([
                [1, 0, 0, dx],
                [0, 1, 0, dy],
                [0, 0, 1, dz],
                [0, 0, 0, 1]
            ])

def get_scale_matrix(sx, sy, sz):
    return np.array([
                [sx, 0, 0, 0],
                [0, sy, 0, 0],
                [0, 0, sz, 0],
                [0, 0, 0, 1]
            ])

def get_rotation_matrix(ax:str, dg_angle):
    angle = math.radians(dg_angle)
    if ax == 'x':
        return np.array([
            [1, 0, 0, 0],
            [0, math.cos(angle), -math.sin(angle), 0],
            [0, math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1]
        ])
    elif ax == 'y':
        return np.array([
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ])
    elif ax == 'z':
        return np.array([
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    else:
        raise TypeError("Eixo escolhido inválido")

def get_reflection_matrix(plane: str):
    if plane == 'xy':
        return np.array([
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, -1, 0],
                    [0, 0, 0, 1]
                ])
    elif plane == 'xz':
        return np.array([
                    [1, 0, 0, 0],
                    [0, -1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])
    elif plane == 'yz':
        return np.array([
                    [-1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])
    else:
        raise TypeError("Eixo escolhido inválido")

def get_shear_matrix(xy=0, xz=0, yz=0):
    return np.array([
        [1, xy, xz, 0],
        [0, 1, yz, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def apply_transformation(mesh_or_scene, matrix, object_id=None):
    """Aplica uma matriz de transformação a um objeto ou cena"""
    if isinstance(mesh_or_scene, Scene):
        if object_id is not None:
            obj = mesh_or_scene.get_object(object_id)
            if obj is None:
                return
            apply_transformation(obj, matrix)
        else:
            for obj in mesh_or_scene.objects.values():
                apply_transformation(obj, matrix)
    else:
        # Aplica a transformação em cada vértice do objeto
        for vertex in mesh_or_scene.vertices.values():
            point = np.array([*vertex.position, 1])
            transformed_point = matrix @ point
            vertex.position = (transformed_point[0], transformed_point[1], transformed_point[2])
        
        # Recalcula o centroide após a transformação
        mesh_or_scene.calculate_centroid()

def transformation_matrix_3d():
    """Retorna a matriz transformacao para um objeto 3D de acordo com as operacoes escolhidas"""
    # Pilha de transformações
    stack = []
    print("Escolha as transformações 3D para o objeto:")

    while True:
        print("\nTransformações disponíveis:")
        print("1. Translação")
        print("2. Escala")
        print("3. Rotação em torno de X")
        print("4. Rotação em torno de Y")
        print("5. Rotação em torno de Z")
        print("6. Reflexão")
        print("7. Cisalhamento")
        print("8. Finalizar escolhas")
        choice = input("Digite o número da transformação desejada: ")

        if choice == "1":  # Translação
            dx = float(input("Digite a translação em X: "))
            dy = float(input("Digite a translação em Y: "))
            dz = float(input("Digite a translação em Z: "))
            stack.append(('translation', dx, dy, dz))

        elif choice == "2":  # Escala
            sx = float(input("Digite a escala em X: "))
            sy = float(input("Digite a escala em Y: "))
            sz = float(input("Digite a escala em Z: "))
            stack.append(('scale', sx, sy, sz))

        elif choice == "3":  # Rotação em torno de X
            angle = float(input("Digite o ângulo de rotação em graus (X): "))
            stack.append(('rotation_x', angle))

        elif choice == "4":  # Rotação em torno de Y
            angle = float(input("Digite o ângulo de rotação em graus (Y): "))
            stack.append(('rotation_y', angle))

        elif choice == "5":  # Rotação em torno de Z
            angle = float(input("Digite o ângulo de rotação em graus (Z): "))
            stack.append(('rotation_z', angle))

        elif choice == "6":  # Reflexão
            print("Escolha o plano de reflexão:")
            print("1. XY (Z inverte)")
            print("2. XZ (Y inverte)")
            print("3. YZ (X inverte)")
            reflection_choice = input("Digite o número do plano: ")
            if reflection_choice == "1":
                stack.append(('reflection', 'xy'))
            elif reflection_choice == "2":
                stack.append(('reflection', 'xz'))
            elif reflection_choice == "3":
                stack.append(('reflection', 'yz'))

        elif choice == "7":  # Cisalhamento
            sh_xy = float(input("Digite o fator de cisalhamento no plano XY: "))
            sh_xz = float(input("Digite o fator de cisalhamento no plano XZ: "))
            sh_yz = float(input("Digite o fator de cisalhamento no plano YZ: "))
            stack.append(('shear', sh_xy, sh_xz, sh_yz))

        elif choice == "8":  # Finalizar escolhas
            break
        else:
            print("Opção inválida, tente novamente.")

    # Matriz de transformação composta (identidade)
    transformation_matrix = np.identity(4)

    # Processar a pilha na ordem inversa
    while stack:
        operation = stack.pop()
        if operation[0] == 'translation':
            dx, dy, dz = operation[1], operation[2], operation[3]
            translation_matrix = get_translation_matrix(dx, dy, dz)
            transformation_matrix = translation_matrix @ transformation_matrix

        elif operation[0] == 'scale':
            sx, sy, sz = operation[1], operation[2], operation[3]
            scale_matrix = get_scale_matrix(sx, sy, sz)
            transformation_matrix = scale_matrix @ transformation_matrix

        elif operation[0] == 'rotation_x':
            angle = operation[1]
            rotation_x_matrix = get_rotation_matrix("x", angle)
            transformation_matrix = rotation_x_matrix @ transformation_matrix

        elif operation[0] == 'rotation_y':
            angle = operation[1]
            rotation_y_matrix = get_rotation_matrix("y", angle)
            transformation_matrix = rotation_y_matrix @ transformation_matrix

        elif operation[0] == 'rotation_z':
            angle = operation[1]
            rotation_z_matrix = get_rotation_matrix("z", angle)
            transformation_matrix = rotation_z_matrix @ transformation_matrix

        elif operation[0] == 'reflection':
            plane = operation[1]
            reflection_matrix = get_reflection_matrix(plane)
            transformation_matrix = reflection_matrix @ transformation_matrix

        elif operation[0] == 'shear':
            sh_xy, sh_xz, sh_yz = operation[1], operation[2], operation[3]
            shear_matrix = get_shear_matrix(sh_xy, sh_xz, sh_yz)
            transformation_matrix = shear_matrix @ transformation_matrix

    return transformation_matrix


if __name__ == "__main__":
    print(transformation_matrix_3d())