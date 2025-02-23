import numpy as np
from .winged_edge import WingedEdge

def create_cube(center, size):
    cube = WingedEdge()
    half = size / 2.0
    cx, cy, cz = center

    vertices = [
        (cx - half, cy - half, cz - half),
        (cx + half, cy - half, cz - half),
        (cx + half, cy + half, cz - half),
        (cx - half, cy + half, cz - half),
        (cx - half, cy - half, cz + half),
        (cx + half, cy - half, cz + half),
        (cx + half, cy + half, cz + half),
        (cx - half, cy + half, cz + half)
    ]
    for i, pos in enumerate(vertices):
        cube.add_vertex(i, pos)

    faces = [
        [0, 3, 2, 1],  # face trás 
        [4, 5, 6, 7],  # face frente
        [0, 1, 5, 4],  # face baixo
        [2, 3, 7, 6],  # face cima
        [0, 4, 7, 3],  # face esquerda
        [1, 2, 6, 5],  # face direita
    ]

    edge_map = {}
    next_edge_id = 0
    next_face_id = 0

    for face_vert_indices in faces:
        face_edge_ids = []
        num = len(face_vert_indices)
        for i in range(num):
            v1 = face_vert_indices[i]
            v2 = face_vert_indices[(i + 1) % num]
            key = tuple(sorted((v1, v2)))
            if key not in edge_map:
                edge_map[key] = next_edge_id
                cube.add_edge(next_edge_id, v1, v2)
                next_edge_id += 1
            face_edge_ids.append(edge_map[key])
        cube.add_face(next_face_id, face_edge_ids, face_vert_indices)
        next_face_id += 1

    cube.link_edges()
    cube.calculate_centroid()
    return cube

def create_square_pyramid(center, base_size, height):
    pyramid = WingedEdge()
    half = base_size / 2.0
    cx, cy, cz = center

    base_vertices = [
        (cx - half, cy, cz - half),
        (cx + half, cy, cz - half), 
        (cx + half, cy, cz + half),
        (cx - half, cy, cz + half)
    ]

    apex = (cx, cy + height, cz)

    for i, pos in enumerate(base_vertices):
        pyramid.add_vertex(i, pos)
    pyramid.add_vertex(4, apex)

    faces = [
        {'vertices': [0, 1, 2, 3]},      # base
        {'vertices': [0, 4, 1]},         # face frente
        {'vertices': [1, 4, 2]},         # face direita
        {'vertices': [2, 4, 3]},         # face tras
        {'vertices': [3, 4, 0]}          # face esquerda
    ]


    edge_map = {}
    next_edge_id = 0
    next_face_id = 0

    for face_data in faces:
        face_vert_indices = face_data['vertices']
        face_edge_ids = []
        num = len(face_vert_indices)
        for i in range(num):
            v1 = face_vert_indices[i]
            v2 = face_vert_indices[(i + 1) % num]
            key = tuple(sorted((v1, v2)))
            if key not in edge_map:
                edge_map[key] = next_edge_id
                pyramid.add_edge(next_edge_id, v1, v2)
                next_edge_id += 1
            face_edge_ids.append(edge_map[key])
        pyramid.add_face(next_face_id, face_edge_ids, face_vert_indices)
        next_face_id += 1

    pyramid.link_edges()
    pyramid.calculate_centroid()
    return pyramid

def create_triangular_pyramid(center, base_size, height):
    pyramid = WingedEdge()
    cx, cy, cz = center

    angle_offsets = [0, 120, 240]
    base_vertices = []
    radius = base_size / np.sqrt(3)
    
    for ang in angle_offsets:
        rad = np.deg2rad(ang)
        x = cx + radius * np.cos(rad)
        z = cz + radius * np.sin(rad)
        base_vertices.append((x, cy, z))

    apex = (cx, cy + height, cz)

    for i, pos in enumerate(base_vertices):
        pyramid.add_vertex(i, pos)
    pyramid.add_vertex(3, apex)

    faces = [
        {'vertices': [0, 2, 1]},     
        {'vertices': [0, 3, 2]},     
        {'vertices': [1, 3, 0]},     
        {'vertices': [2, 3, 1]} 
    ]

    edge_map = {}
    next_edge_id = 0
    next_face_id = 0

    for face_data in faces:
        face_vert_indices = face_data['vertices']
        face_edge_ids = []
        num = len(face_vert_indices)
        for i in range(num):
            v1 = face_vert_indices[i]
            v2 = face_vert_indices[(i + 1) % num]
            key = tuple(sorted((v1, v2)))
            if key not in edge_map:
                edge_map[key] = next_edge_id
                pyramid.add_edge(next_edge_id, v1, v2)
                next_edge_id += 1
            face_edge_ids.append(edge_map[key])
        pyramid.add_face(next_face_id, face_edge_ids, face_vert_indices)
        next_face_id += 1

    pyramid.link_edges()
    pyramid.calculate_centroid()
    return pyramid