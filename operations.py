from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import random
import numpy as np

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


def transformation_matrix_2D():
    """Retorna a matriz transformacao de um objeto 2D para a sequencia de operacoes definida durante a execucao"""
    operations = [] # Salva as operacoes no formato de pilha

    while True:
        print("\nInsira a transformacao que deseja aplicar ou digite 0 para aplicar as ja inseridas:")
        print("1. Translacao")
        print("2. Escala")
        print("3. Reflexao")
        print("4. Cisalhamento")
        print("5. Rotacao")
        print("0. Aplicar tudo")

        choice = input("Digite o número da opção desejada: ")

        if choice == '1':  # Translação
            dx = float(input("Digite o deslocamento em x: "))
            dy = float(input("Digite o deslocamento em y: "))
            operations.append(('translation', dx, dy))

        elif choice == '2':  # Escala
            sx = float(input("Digite o fator de escala em x: "))
            sy = float(input("Digite o fator de escala em y: "))
            operations.append(('scaling', sx, sy))

        elif choice == '3':  # Reflexão
            print("Escolha o eixo de reflexão:")
            print("1. Reflexão no eixo X")
            print("2. Reflexão no eixo Y")
            print("3. Reflexão na origem")
            reflection_choice = input("Digite o número da reflexão: ")
            operations.append(('reflection', reflection_choice))

        elif choice == '4':  # Cisalhamento
            shx = float(input("Digite o fator de cisalhamento em x: "))
            shy = float(input("Digite o fator de cisalhamento em y: "))
            operations.append(('shear', shx, shy))

        elif choice == '5':  # Rotação
            angle = float(input("Digite o ângulo de rotação (em graus): "))
            rotate_about = input("Deseja rotacionar em torno de um ponto específico? (s/n): ")
            if rotate_about.lower() == 's':
                x_c = float(input("Digite a coordenada x do ponto: "))
                y_c = float(input("Digite a coordenada y do ponto: "))
                # Adiciona as translações para a origem e de volta
                operations.append(('translation', -x_c, -y_c))
                operations.append(('rotation', angle))
                operations.append(('translation', x_c, y_c))
            else:
                operations.append(('rotation', angle))

        elif choice == '0':  # Finalizar
            break

        else:
            print("Opção inválida. Por favor, escolha entre 0 a 5.")

        # Inicia a matriz como identidade
    result_matrix = np.identity(3)

    # Processa as transformações na ordem inversa (último a entrar é o primeiro a ser aplicado)
    while operations:
        transformation = operations.pop()

        if transformation[0] == 'translation':
            dx, dy = transformation[1], transformation[2]
            matrix = np.array([[1, 0, dx],
                               [0, 1, dy],
                               [0, 0, 1]])

        elif transformation[0] == 'rotation':
            angle = np.radians(transformation[1])
            cos_theta = np.cos(angle)
            sin_theta = np.sin(angle)
            matrix = np.array([[cos_theta, -sin_theta, 0],
                               [sin_theta, cos_theta, 0],
                               [0, 0, 1]])

        elif transformation[0] == 'scaling':
            sx, sy = transformation[1], transformation[2]
            matrix = np.array([[sx, 0, 0],
                               [0, sy, 0],
                               [0, 0, 1]])

        elif transformation[0] == 'reflection':
            reflection_choice = transformation[1]
            if reflection_choice == '1':  # Reflexão no eixo X
                matrix = np.array([[1, 0, 0],
                                   [0, -1, 0],
                                   [0, 0, 1]])
            elif reflection_choice == '2':  # Reflexão no eixo Y
                matrix = np.array([[-1, 0, 0],
                                   [0, 1, 0],
                                   [0, 0, 1]])
            elif reflection_choice == '3':  # Reflexão na origem
                matrix = np.array([[-1, 0, 0],
                                   [0, -1, 0],
                                   [0, 0, 1]])
            else:
                print("Reflexão inválida! Ignorando...")
                continue

        elif transformation[0] == 'shear':
            shx, shy = transformation[1], transformation[2]
            matrix = np.array([[1, shx, 0],
                               [shy, 1, 0],
                               [0, 0, 1]])

        # Multiplica a matriz resultante pela transformação atual
        result_matrix = matrix @ result_matrix

    return result_matrix

if __name__ == "__main__":
    print("Este arquivo contém operações que podem ser utilizadas sobre a estrutura WingedEdge")