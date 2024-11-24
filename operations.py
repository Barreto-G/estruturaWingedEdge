from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import math
from wingedEdge import WingedEdge


def get_vertices_sharing_face(mesh: WingedEdge, face_id: int):
    """Retorna uma lista dos vertices que compartilham uma face"""
    face = mesh.faces[face_id]
    if not face:
        return []  # retorna vazio se a face não existir

    vertices = []
    for edge in face.edges:
        vertices.append(edge.vertex1.id)
        vertices.append(edge.vertex2.id)

    return vertices


def get_edges_sharing_vertex(mesh, vertex_id):
    """Retorna uma lista de arestas que compartilham o mesmo vertice"""
    vertex = mesh.vertices.get(vertex_id)
    if not vertex:
        return []  # retorna vazio se o vertice não existir

    # retorna os ids das arestas conectadas ao vértice
    return [edge.id for edge in vertex.edges]

def get_faces_sharing_edge(mesh, edge_id):
    """Retorna uma lista de faces que compartilham uma mesma aresta"""
    edge = mesh.edges.get(edge_id)
    if not edge:
        return []  # Retorna vazio se a aresta não existir

    # Retorna as faces associadas a aresta, se existirem
    faces = []
    if edge.left_face:
        faces.append(edge.left_face.id)
    if edge.right_face:
        faces.append(edge.right_face.id)
    return faces


def read_obj(filename):
    """Lê um arquivo .obj e retorna um objeto da classe WingedEdge"""
    vertex_map = {}  # Dicionario garante a criação de arestas únicas
    mesh = WingedEdge()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts or parts[0] == '#':   # Ignora as linhas em branco do arquivo
                continue

            # Cuida das linhas de vertices no arquivo
            if parts[0] == 'v':
                x, y, z = map(float, parts[1:4])
                vertex_id = len(mesh.vertices) + 1
                mesh.add_vertex(vertex_id, (x, y, z))

            # Le informações das faces e adiciona faces e arestas ao objeto
            elif parts[0] == 'f':
                # Quebra o formato da face nos vertices que a compoem, pegando apenas o primeiro vertice de cada conjunto x//y.
                # Isso é suficiente caso as informações das faces venham em ordem, mas caso não seja, o código precisará ser modificado
                vertex_indices = [int(part.split('//')[0]) for part in parts[1:4]]
                edge_ids = []

                # Cria arestas a partir dos vertices que compoem a face, ligando um vertice x ao x+1 de forma circular
                for i in range(3):
                    v1_id = vertex_indices[i]
                    v2_id = vertex_indices[(i + 1) % 3]  # Conecta o último vertice ao primeiro
                    edge_key = tuple(sorted((v1_id, v2_id)))

                    # Adiciona uma aresta caso ela ainda nao exista
                    if edge_key not in vertex_map:
                        edge_id = len(mesh.edges) + 1
                        mesh.add_edge(edge_id, v1_id, v2_id)
                        vertex_map[edge_key] = edge_id

                    # Adiciona o id da aresta à lista da face
                    edge_ids.append(vertex_map[edge_key])

                # Adiciona a face triangular usando a lista de arestas
                face_id = len(mesh.faces) + 1
                mesh.add_face(face_id, edge_ids)

    # Configura os links entre as arestas
    mesh.link_edges()
    return mesh

def plot_3d_object(winged_edge: WingedEdge, ax: plt.Axes, colors: list):
    # Plotando vértices
    for vertex in winged_edge.vertices.values():
        ax.scatter(*vertex.position, color='r', marker='o', s=20)
    
    # Lista com 4 tons de azul
    colors = ['lightblue', 'skyblue', 'dodgerblue', 'royalblue']

    # Plotando faces
    for face_id, face in winged_edge.faces.items():
        face_vertices = []
        for edge in face.edges:
            if edge.vertex1 not in face_vertices:
                face_vertices.append(edge.vertex1)
            if edge.vertex2 not in face_vertices:
                face_vertices.append(edge.vertex2)

        # Pegando as posições dos vértices para o polígono da face
        verts = [vertex.position for vertex in face_vertices]
        
        poly = Poly3DCollection([verts], alpha=1, linewidths=0.5)
        
        # Alternar entre os tons de azul
        poly.set_facecolor(colors[face_id % 4])
        ax.add_collection3d(poly)

    # Plotando arestas
    for edge in winged_edge.edges.values():
        x_values = [edge.vertex1.position[0], edge.vertex2.position[0]]
        y_values = [edge.vertex1.position[1], edge.vertex2.position[1]]
        z_values = [edge.vertex1.position[2], edge.vertex2.position[2]]
        ax.plot(x_values, y_values, z_values, color='k', linewidth=5)
    
    # Ajustando rótulos de eixos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')




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
            translation_matrix = np.array([
                [1, 0, 0, dx],
                [0, 1, 0, dy],
                [0, 0, 1, dz],
                [0, 0, 0, 1]
            ])
            transformation_matrix = translation_matrix @ transformation_matrix

        elif operation[0] == 'scale':
            sx, sy, sz = operation[1], operation[2], operation[3]
            scale_matrix = np.array([
                [sx, 0, 0, 0],
                [0, sy, 0, 0],
                [0, 0, sz, 0],
                [0, 0, 0, 1]
            ])
            transformation_matrix = scale_matrix @ transformation_matrix

        elif operation[0] == 'rotation_x':
            angle = math.radians(operation[1])
            rotation_x_matrix = np.array([
                [1, 0, 0, 0],
                [0, math.cos(angle), -math.sin(angle), 0],
                [0, math.sin(angle), math.cos(angle), 0],
                [0, 0, 0, 1]
            ])
            transformation_matrix = rotation_x_matrix @ transformation_matrix

        elif operation[0] == 'rotation_y':
            angle = math.radians(operation[1])
            rotation_y_matrix = np.array([
                [math.cos(angle), 0, math.sin(angle), 0],
                [0, 1, 0, 0],
                [-math.sin(angle), 0, math.cos(angle), 0],
                [0, 0, 0, 1]
            ])
            transformation_matrix = rotation_y_matrix @ transformation_matrix

        elif operation[0] == 'rotation_z':
            angle = math.radians(operation[1])
            rotation_z_matrix = np.array([
                [math.cos(angle), -math.sin(angle), 0, 0],
                [math.sin(angle), math.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            transformation_matrix = rotation_z_matrix @ transformation_matrix

        elif operation[0] == 'reflection':
            plane = operation[1]
            if plane == 'xy':
                reflection_matrix = np.array([
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, -1, 0],
                    [0, 0, 0, 1]
                ])
            elif plane == 'xz':
                reflection_matrix = np.array([
                    [1, 0, 0, 0],
                    [0, -1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])
            elif plane == 'yz':
                reflection_matrix = np.array([
                    [-1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])
            transformation_matrix = reflection_matrix @ transformation_matrix

        elif operation[0] == 'shear':
            sh_xy, sh_xz, sh_yz = operation[1], operation[2], operation[3]
            shear_matrix = np.array([
                [1, sh_xy, sh_xz, 0],
                [0, 1, sh_yz, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            transformation_matrix = shear_matrix @ transformation_matrix

    return transformation_matrix


if __name__ == "__main__":
    print("Este arquivo contém operações que podem ser utilizadas sobre a estrutura WingedEdge")