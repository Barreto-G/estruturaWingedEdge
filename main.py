
## Função base para ler .obj, deve ser modificada para ir adicionando as linhas à um objeto WingedEdge
## Uma ideia é tornar ela um método estático da classe WingedEdge e fazer ela retornar um objeto já completo
def load_shape_from_obj(self, file_path):
    try:
        vertices = []
        faces = []
        with open(file_path) as f:
            for line in f:
                if line[0] == "v":
                    vertex = list(map(float, line[2:].strip().split()))
                    vertices.append(vertex)
                elif line[0] == "f":
                    face = list(map(int, line[2:].strip().split()))
                    faces.append(face)

        shape_data = {"vertices": vertices, "faces": faces}

        return shape_data

    except FileNotFoundError:
        print(f"{file_path} not found.")
    except:
        print("An error occurred while loading the shape.")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
