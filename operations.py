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


def read_3d_obj(filename):
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
    mesh.calcular_centroide()
    return mesh

def plot_3d_object(winged_edge: WingedEdge, ax: plt.Axes, colors: list=None):
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


def plot_3d(winged_edge_structure):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Supondo que a estrutura 'winged_edge_structure' contenha listas de vértices e faces.
    vertices = [vertice.position for vertice in winged_edge_structure.vertices.values()]  # Lista de vértices (cada vértice é uma tupla (x, y, z))
    faces = [list(set(get_vertices_sharing_face(winged_edge_structure, face.id))) for face in winged_edge_structure.faces.values()]  # Lista de faces (cada face é uma lista de índices de vértices)
    # Plotando os vértices
    xs, ys, zs = zip(*vertices)
    ax.scatter(xs, ys, zs, color='b', marker='o', label='Vértices')

    # Plotando as arestas (conectando os vértices)
    for face in faces:
        for i in range(len(face)):
            # Conectando vértices consecutivos de cada face
            v1 = vertices[face[i]-1]
            v2 = vertices[face[(i + 1) % len(face)]-1]
            ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], color='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Visualização 3D de Estrutura Winged Edge')

    plt.legend()
    plt.show()

if __name__ == "__main__":
    print("Este arquivo contém operações que podem ser utilizadas sobre a estrutura WingedEdge")