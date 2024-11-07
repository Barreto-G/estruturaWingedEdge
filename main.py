from wingedEdge import WingedEdge
import operations as op


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
                faces = op.get_faces_sharing_edge(mesh, edge_id)
                print(f"Faces que compartilham a aresta {edge_id}: {faces}")
            except ValueError:
                print("ID inválido! Por favor, digite um número.")

        elif choice == '2':
            try:
                vertex_id = int(input("Digite o ID do vértice: "))
                edges = op.get_edges_sharing_vertex(mesh, vertex_id)
                print(
                    f"Arestas que compartilham o vértice {vertex_id}: {edges}")
            except ValueError:
                print("ID inválido! Por favor, digite um número.")

        elif choice == '3':
            try:
                face_id = int(input("Digite o ID da face: "))
                vertices = op.get_vertices_sharing_face(mesh, face_id)
                print(
                    f"Vértices que compartilham a face {face_id}: {vertices}")
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
        objeto = op.read_obj(filename)
        while True:
            print("\nEscolha uma das opções:")
            print("1. Fazer consultas")
            print("2. Imprimir informacoes do objeto")
            print("3. Plotar um gráfico 3D do objeto")
            print("4. Fechar o programa")
            choice = input("Digite o número da opção desejada: ")

            if choice == '1':
                main_console(objeto)

            elif choice == '2':
                vertices_info = list(objeto.vertices.values())
                edges_info = list(objeto.edges.values())
                faces_info = list(objeto.faces.values())
                print(vertices_info)
                print(edges_info)
                print(faces_info)

            elif choice == '3':
                op.plot_3d_object(objeto)

            elif choice == '4':
                break

    except FileNotFoundError:
        print("Arquivo nao encontrado, tente novamente")
    except Exception as error:
        print(f"Erro Desconhecido: {error}")
