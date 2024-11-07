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

if __name__ == "__main__":
    print("Este arquivo contém operações que podem ser utilizadas sobre a estrutura WingedEdge")