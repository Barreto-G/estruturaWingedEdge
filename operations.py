from wingedEdge import WingedEdge

def get_vertices_sharing_face(mesh: WingedEdge, face_id):
    """Retorna os vertices que compartilham uma face"""
    face = mesh.faces.get(face_id)
    if face is None:
        return []  # Retorna vazio se a face não existir

    vertices = set()
    for edge in face.edges:
        vertices.add(edge.vertex1.id)
        vertices.add(edge.vertex2.id)

    # Converte o conjunto para lista antes de retornar
    return list(vertices)


def get_edges_sharing_vertex(mesh, vertex_id):
    """Retorna as arestas que compartilham o mesmo vertice"""
    vertex = mesh.vertices.get(vertex_id)
    if vertex is None:
        return []  # Retorna vazio se o vértice não existir

    # Retorna os IDs das arestas conectadas ao vértice
    return [edge.id for edge in vertex.edges]

def get_faces_sharing_edge(mesh, edge_id):
    """Retorna faces que compartilham uma mesma aresta"""
    edge = mesh.edges.get(edge_id)
    if edge is None:
        return []  # Retorna vazio se a aresta não existir

    # Retorna as faces associadas à aresta (esquerda e direita, se existirem)
    faces = []
    if edge.left_face:
        faces.append(edge.left_face.id)
    if edge.right_face:
        faces.append(edge.right_face.id)
    return faces


def read_obj(filename, mesh: WingedEdge):
    """Lê um arquivo .obj e retorna um objeto baseado na estrutura WingedEdge"""
    vertex_map = {}  # Mapeamento para garantir a criação de arestas únicas

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue

            # Adiciona vértices
            if parts[0] == 'v':
                x, y, z = map(float, parts[1:4])
                vertex_id = len(mesh.vertices) + 1
                mesh.add_vertex(vertex_id, (x, y, z))

            # Adiciona faces e arestas, com triângulos representados na forma v//n
            elif parts[0] == 'f':
                vertex_indices = [int(part.split('//')[0]) for part in parts[1:4]]
                edge_ids = []

                # Criar arestas para a face triangular
                for i in range(3):
                    v1_id = vertex_indices[i]
                    v2_id = vertex_indices[(i + 1) % 3]  # Conecta o último vértice ao primeiro
                    edge_key = tuple(sorted((v1_id, v2_id)))

                    # Verifica se a aresta já foi criada
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

if __name__ == "__main__":
    print("Este arquivo contém operações que podem ser utilizadas sobre a estrutura WingedEdge")