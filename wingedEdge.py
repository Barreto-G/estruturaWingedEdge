# Implementação das classes para Vertices, Arestas, Faces e a própria estrutura Winged Edge
# A ideia é utilizar apenas a WingedEdge, adicionando primeiro os vertices, depois as arestas e por fim as faces.
# Após adicionar tudo, chamar a função link edges para fazer todas as ligações necessárias.

# A ideia principal e que cada objeto contenha informacoes de outros objetos adjacentes a ele. Dessa forma:
#   Vertices mantem a informacao das arestas conectadas a eles;
#   Arestas mantem informacoes dos vertices que as definem, faces adjacentes e arestas adjacentes com relacao a cada face;
#   Faces mantem apenas a informacao das arestas que as compoem.

class Vertex:
    def __init__(self, id: int, position):
        self.id = id
        self.position = position # Tupla no modelo [x,y,z]
        self.edges = []          # Lista de arestas incidentes no vertice

    def __repr__(self):
        return f"Vertice {self.id}, posicao = {self.position}"


class Edge:
    def __init__(self, id: int, vertex1: Vertex, vertex2: Vertex):
        self.id = id
        self.vertex1 = vertex1
        self.vertex2 = vertex2

        self.left_face = None   # Face a esquerda da aresta
        self.right_face = None  # Face a direita da aresta

        self.next_left = None   # Proxima aresta em relacao a face esquerda
        self.prev_left = None   # Aresta Anterior em relacao a face esquerda

        self.next_right = None  # Proxima aresta em relacao a face direita
        self.prev_right = None  # Aresta Anterior em relacao a face direita

    def __repr__(self):
        return f"Aresta {self.id}, vertices = {self.vertex1}, {self.vertex2}"


class Face:
    def __init__(self, id: int):
        self.id = id
        self.edges = []

    def __repr__(self):
        return f"Face {self.id}"


# A estrutura WingedEdge mantem um dicionario para cada elemento do objeto a ser representado(de forma a evitar duplicados),
# sendo eles vertices, arestas e faces. A estrutura foi pensada de forma que adicionam-se primeiro os vertices do objeto,
# entao as arestas e por fim as faces. Com todas as informações estabelecidas, deve-se executar a função LinkEdges para que,
# a partir da informação das faces, sejam salvas em cada aresta as referencias de arestas vizinhas
class WingedEdge:
    def __init__(self):
        # Armazena em estrutura de dicionário para facilitar o acesso e operacoes posteriores
        self.vertices = {}
        self.edges = {}
        self.faces = {}

    def add_vertex(self, id: int, position):
        vertex = Vertex(id, position)
        self.vertices[id] = vertex # usa-se o id da propria aresta para sua demarcação no dicionário, assim, não teremos vertices duplicados

    def add_edge(self, id: int, vertex1_id: int, vertex2_id: int): # Cria uma aresta a partir de 2 vertices pre-existentes
        # Pega a referencia dos vertices pre-existentes
        vertex1 = self.vertices[vertex1_id]
        vertex2 = self.vertices[vertex2_id]

        # Cria a aresta e a adiciona no dicionario
        edge = Edge(id, vertex1, vertex2)
        self.edges[id] = edge

        # Adiciona a referencia da nova aresta aos vertices
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)

    def add_face(self, id: int, edge_ids):
        # Edge_ids é um vetor de ids das arestas que comporão a face
        # Criando uma nova face e adicionando sua referencia ao dicionario
        face = Face(id)
        self.faces[id] = face

        # Para cada aresta que compoe a face, adiciona a referência da face à aresta, no sentido horário (esquerda - direita)
        for edge_id in edge_ids:
            edge = self.edges[edge_id]
            face.edges.append(edge)

            if edge.left_face is None:
                edge.left_face = face
            elif edge.right_face is None:
                edge.right_face = face
            else:
                raise ValueError(f"Aresta {edge_id} já pertence a duas faces e não pode ser compartilhada por mais.")


    def link_edges(self):
        """Estabelece as conexões entre as arestas adjacentes no objeto"""

        # Para cada aresta, analisa suas faces e as arestas que as compõem
        for edge in self.edges.values():
            for face in [edge.left_face, edge.right_face]:
                if face:    # Se face != None
                    edges = face.edges
                    idx = edges.index(edge)
                    # Verifica se a face esta como face esquerda ou direita de edge e seta as arestas adjascentes de forma correspondente
                    if face == edge.left_face:
                        edge.next_left = edges[(idx + 1) % len(edges)]
                        edge.prev_left = edges[(idx - 1) % len(edges)]
                    elif face == edge.right_face:
                        edge.next_right = edges[(idx + 1) % len(edges)]
                        edge.prev_right = edges[(idx - 1) % len(edges)]
                    # Utilizar %len(edges) garante que os indices se ajustem de forma rotativa
                    # Assim, se idx+1 extrapolar os ids possiveis, o indice calculado volta pro inicio, como se fosse uma lista circular
                    # Genialidade fornecida por: ChatGpt da Silva

    def __repr__(self):
        return f"WingedEdgeMesh(vertices={list(self.vertices.keys())}, edges={list(self.edges.keys())}, faces={list(self.faces.keys())})"

if __name__ == "__main__":
    print("Este arquivo contém a estrutura de dados Winged Edge e as classes para implementá-la")