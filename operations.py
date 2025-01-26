from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import math
from wingedEdge import WingedEdge, Scene


def get_vertices_sharing_face(mesh: WingedEdge, face_id: int, object_id: int = None):
    """Retorna uma lista dos vertices que compartilham uma face"""
    if isinstance(mesh, Scene):
        if object_id is None:
            raise ValueError("Informe o ID do objeto")
        mesh = mesh.get_object(object_id)
    
    face = mesh.faces[face_id]
    if not face:
        return []  # retorna vazio se a face não existir

    vertices = []
    for edge in face.edges:
        vertices.append(edge.vertex1.id)
        vertices.append(edge.vertex2.id)

    return vertices


def get_edges_sharing_vertex(mesh, vertex_id: int, object_id: int = None):
    """Retorna uma lista de arestas que compartilham o mesmo vertice"""
    if isinstance(mesh, Scene):
        if object_id is None:
            raise ValueError("Informe o ID do objeto")
        mesh = mesh.get_object(object_id)
    
    vertex = mesh.vertices.get(vertex_id)
    if not vertex:
        return []  # retorna vazio se o vertice não existir

    # retorna os ids das arestas conectadas ao vértice
    return [edge.id for edge in vertex.edges]


def get_faces_sharing_edge(mesh, edge_id: int, object_id: int = None):
    """Retorna uma lista de faces que compartilham uma mesma aresta"""
    if isinstance(mesh, Scene):
        if object_id is None:
            raise ValueError("Informe o ID do objeto")
        mesh = mesh.get_object(object_id)
    
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


def get_scene_boundaries(scene: Scene):
    """Retorna os limites minimos e maximos da cena em cada eixo"""
    if not scene.objects:
        return None
    
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')
    
    for obj in scene.objects.values():
        for vertex in obj.vertices.values():
            x, y, z = vertex.position
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)
    
    return {
        'x': (min_x, max_x),
        'y': (min_y, max_y),
        'z': (min_z, max_z)
    }


def get_scene_center(scene: Scene):
    """Retorna o ponto central da cena"""
    boundaries = get_scene_boundaries(scene)
    if not boundaries:
        return None
    
    center_x = (boundaries['x'][0] + boundaries['x'][1]) / 2
    center_y = (boundaries['y'][0] + boundaries['y'][1]) / 2
    center_z = (boundaries['z'][0] + boundaries['z'][1]) / 2
    
    return (center_x, center_y, center_z)


def read_3d_obj(filename):
    """Lê um arquivo .obj e retorna um objeto da classe Scene"""
    vertex_map = {}  # Dicionario garante a criação de arestas únicas
    scene = Scene()
    current_object = WingedEdge()
    current_object_id = 1
    
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts or parts[0] == '#':   # Ignora as linhas em branco do arquivo
                continue

            # Se encontrar um novo objeto, salva o atual e cria um novo
            if parts[0] == 'o':
                if current_object.vertices:
                    current_object.link_edges()
                    current_object.calculate_centroid()
                    scene.add_object(current_object_id, current_object)
                    current_object_id += 1
                    current_object = WingedEdge()
                    vertex_map = {}

            # Cuida das linhas de vertices no arquivo
            elif parts[0] == 'v':
                x, y, z = map(float, parts[1:4])
                vertex_id = len(current_object.vertices) + 1
                current_object.add_vertex(vertex_id, (x, y, z))

            # Le informações das faces e adiciona faces e arestas ao objeto
            elif parts[0] == 'f':
                vertex_indices = [int(part.split('//')[0]) for part in parts[1:4]]
                edge_ids = []

                for i in range(3):
                    v1_id = vertex_indices[i]
                    v2_id = vertex_indices[(i + 1) % 3]
                    edge_key = tuple(sorted((v1_id, v2_id)))

                    if edge_key not in vertex_map:
                        edge_id = len(current_object.edges) + 1
                        current_object.add_edge(edge_id, v1_id, v2_id)
                        vertex_map[edge_key] = edge_id

                    edge_ids.append(vertex_map[edge_key])

                face_id = len(current_object.faces) + 1
                current_object.add_face(face_id, edge_ids)

    # Adiciona o último objeto à cena
    if current_object.vertices:
        current_object.link_edges()
        current_object.calculate_centroid()
        scene.add_object(current_object_id, current_object)

    return scene


def plot_3d_object(mesh, ax: plt.Axes, colors: list=None, object_id: int = None, highlight: bool = False):
    """Plota um objeto 3D com transformações de viewport"""
    if isinstance(mesh, Scene):
        if object_id is None:
            for obj_id, obj in mesh.objects.items():
                plot_3d_object(obj, ax, colors)
            return
        mesh = mesh.get_object(object_id)

    # Plotando vértices
    vertex_color = 'red' if highlight else 'black'
    vertex_size = 30 if highlight else 20
    for vertex in mesh.vertices.values():
        ax.scatter(*vertex.position, color=vertex_color, marker='o', s=vertex_size)
    
    # Lista com cores
    if colors is None:
        colors = ['lightblue']

    # Plotando faces
    alpha = 1.0 if highlight else 0.7  # Face mais transparente se não estiver selecionado
    for face_id, face in mesh.faces.items():
        face_vertices = []
        for edge in face.edges:
            if edge.vertex1 not in face_vertices:
                face_vertices.append(edge.vertex1)
            if edge.vertex2 not in face_vertices:
                face_vertices.append(edge.vertex2)

        verts = [vertex.position for vertex in face_vertices]
        
        poly = Poly3DCollection([verts], alpha=alpha, linewidths=0.5)
        poly.set_facecolor(colors[face_id % len(colors)])
        ax.add_collection3d(poly)

    # Plotando arestas
    edge_color = 'black' if highlight else 'gray'
    edge_width = 2 if highlight else 1
    for edge in mesh.edges.values():
        x_values = [edge.vertex1.position[0], edge.vertex2.position[0]]
        y_values = [edge.vertex1.position[1], edge.vertex2.position[1]]
        z_values = [edge.vertex1.position[2], edge.vertex2.position[2]]
        ax.plot(x_values, y_values, z_values, color=edge_color, linewidth=edge_width)

    # Ajusta os limites do plot para mostrar todos os objetos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


def plot_3d(scene_or_mesh):
    """Plota uma cena ou objeto 3D completo"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if isinstance(scene_or_mesh, Scene):
        for obj_id in scene_or_mesh.objects:
            plot_3d_object(scene_or_mesh, ax, object_id=obj_id)
        
        # Ajusta os limites do plot baseado nos limites da cena
        boundaries = get_scene_boundaries(scene_or_mesh)
        if boundaries:
            ax.set_xlim(boundaries['x'])
            ax.set_ylim(boundaries['y'])
            ax.set_zlim(boundaries['z'])
    else:
        plot_3d_object(scene_or_mesh, ax)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Visualização 3D')

    plt.show()

