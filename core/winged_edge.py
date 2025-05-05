import numpy as np
from .transformations import create_transformation

class Vertex:
    """Vértice com posição em coordenadas 3D e lista de arestas conectadas"""
    def __init__(self, id, position):
        self.id = id
        self.position = np.array(position, dtype=np.float32)
        self.edges: list['Edge'] = []


class Edge:
    """Aresta definida por dois vértices e suas conexões com faces e outras arestas"""
    def __init__(self, id, vertex1, vertex2):
        self.id = id
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.left_face: 'Face' = None    # Face à esquerda da aresta
        self.right_face: 'Face' = None   # Face à direita da aresta
        self.next_left: 'Edge' = None    # Próxima aresta em relação à face esquerda
        self.prev_left: 'Edge' = None    # Aresta anterior em relação à face esquerda
        self.next_right: 'Edge' = None   # Próxima aresta em relação à face direita
        self.prev_right: 'Edge' = None   # Aresta anterior em relação à face direita


class Face:
    """Face definida por um conjunto de arestas e vértices"""
    def __init__(self, id):
        self.id = id
        self.edges: list[Edge] = []
        self.vertex_indices: list[int] = []  # Store original vertex order


class WingedEdge:
    """Estrutura de dados Winged Edge para representação de malhas 3D"""
    def __init__(self):
        self.vertices: dict[int, Vertex] = {}
        self.edges: dict[int, Edge] = {}
        self.faces: dict[int, Face] = {}
        self.centroid = np.zeros(3, dtype=np.float32)
        # List to store transformations
        self.transformations = []

    def add_transformation(self, transform_type, params):
        self.transformations.append({
            'type': transform_type,
            'params': params
        })

    def clear_transformations(self):
        self.transformations = []

    def get_transformed_vertex(self, vertex_id):
        """Get vertex position with all transformations applied"""
        vertex = self.vertices[vertex_id]
        
        if not self.transformations:
            return vertex.position
            
        transform_matrix = create_transformation(self.transformations)
        
        # Move to origin (subtract centroid)
        pos = vertex.position - self.centroid
        
        # Convert to homogeneous coordinates
        pos = np.append(pos, 1.0)
        
        # Apply transformation
        transformed = transform_matrix @ pos
        
        # Convert back to 3D coordinates
        transformed = transformed[0:3] / transformed[3]
        
        # Move back (add centroid)
        transformed = transformed + self.centroid
        
        return transformed


    @property
    def vertex_count(self):
        return len(self.vertices)

    @property
    def edge_count(self):
        return len(self.edges)

    @property
    def face_count(self):
        return len(self.faces)

    def add_vertex(self, id, position):
        if id in self.vertices:
            raise ValueError(f"O Vértice {id} já existe")
        self.vertices[id] = Vertex(id, position)

    def add_edge(self, id, vertex1_id, vertex2_id):
        if id in self.edges:
            raise ValueError(f"A Aresta {id} já existe")
        
        try:
            vertex1 = self.vertices[vertex1_id]
            vertex2 = self.vertices[vertex2_id]
        except KeyError as e:
            raise ValueError(f"Vértice não encontrado: {e}")

        edge = Edge(id, vertex1, vertex2)
        self.edges[id] = edge
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)

    def add_face(self, id, edge_ids, vertex_indices):
        if id in self.faces:
            raise ValueError(f"A Face {id} já existe")

        face = Face(id)
        face.vertex_indices = vertex_indices
        self.faces[id] = face

        for edge_id in edge_ids:
            try:
                edge = self.edges[edge_id]
            except KeyError:
                raise ValueError(f"A Aresta {edge_id} não existe")

            face.edges.append(edge)

            if edge.left_face is None:
                edge.left_face = face
            elif edge.right_face is None:
                edge.right_face = face
            else:
                raise ValueError(f"A Aresta {edge_id} já está conectada com 2 Faces")


    def link_edges(self):
        """Estabelece as conexões entre as arestas adjacentes"""
        for face in self.faces.values():
            num_edges = len(face.edges)
            for i, edge in enumerate(face.edges):
                next_edge = face.edges[(i + 1) % num_edges]
                prev_edge = face.edges[(i - 1) % num_edges]

                # Atualiza as referências das arestas com base na face atual
                if edge.left_face == face:
                    edge.next_left = next_edge
                    edge.prev_left = prev_edge
                elif edge.right_face == face:
                    edge.next_right = next_edge
                    edge.prev_right = prev_edge

    def calculate_centroid(self):
        """Calcula o centroide do objeto"""
        if not self.vertices:
            return

        positions = np.array([v.position for v in self.vertices.values()])
        self.centroid = np.mean(positions, axis=0)

    def get_vertices_as_array(self):
        return np.array([vertex.position for vertex in self.vertices.values()], 
                       dtype=np.float32)

    def get_face_vertices(self, face_id):
        """Retorna os vértices de uma face em ordem"""
        face = self.faces.get(face_id)
        if not face:
            return []

        return [self.vertices[idx] for idx in face.vertex_indices]
    

    