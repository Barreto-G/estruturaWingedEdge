from wingedEdge import WingedEdge
## Função base para ler .obj

def read_obj(filename, mesh: WingedEdge):
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


def get_edges_sharing_vertex(mesh, vertex_id):
    """Retorna as arestas que compartilham o mesmo vertice"""
    vertex = mesh.vertices.get(vertex_id)
    if vertex is None:
        return []  # Retorna vazio se o vértice não existir

    # Retorna os IDs das arestas conectadas ao vértice
    return [edge.id for edge in vertex.edges]


def get_vertices_sharing_face(mesh, face_id):
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


def main_console(mesh):
    while True:
        # Exibe o menu de opções
        print("\nEscolha uma das opções:")
        print("1. Consultar as faces que compartilham uma determinada aresta")
        print("2. Consultar as arestas que compartilham um determinado vértice")
        print("3. Consultar os vértices que compartilham uma determinada face")
        print("4. Sair")

        # Lê a escolha do usuário
        choice = input("Digite o número da opção desejada: ")

        if choice == '1':
            try:
                edge_id = int(input("Digite o ID da aresta: "))
                faces = get_faces_sharing_edge(mesh, edge_id)
                print(f"Faces que compartilham a aresta {edge_id}: {faces}")
            except ValueError:
                print("ID inválido! Por favor, digite um número.")

        elif choice == '2':
            try:
                vertex_id = int(input("Digite o ID do vértice: "))
                edges = get_edges_sharing_vertex(mesh, vertex_id)
                print(f"Arestas que compartilham o vértice {vertex_id}: {edges}")
            except ValueError:
                print("ID inválido! Por favor, digite um número.")

        elif choice == '3':
            try:
                face_id = int(input("Digite o ID da face: "))
                vertices = get_vertices_sharing_face(mesh, face_id)
                print(f"Vértices que compartilham a face {face_id}: {vertices}")
            except ValueError:
                print("ID inválido! Por favor, digite um número.")

        elif choice == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção de 1 a 4.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        filename = input("Digite o nome do arquivo: ")
        objeto = read_obj(filename, WingedEdge())

        main_console(objeto)
    except FileNotFoundError:
        print("Nome do arquivo errado, tente novamente")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
