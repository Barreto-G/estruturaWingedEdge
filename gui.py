import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import operations as op
from custom_widgets import CustomPopUp, ConsultationWindow, TransformationWindow

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sistema Gráfico Iterativo")
        self.geometry("800x600")
        self.mesh = None
        self.figure = None
        self.canvas = None
        self.consultation_window = None
        self.transformation_window = None
        self.setup_initial_ui()

    def setup_initial_ui(self):
        """Configura a interface inicial com o botão para carregar o arquivo OBJ."""
        self.geometry("500x200")  # Aumenta o tamanho da janela inicial

        # Frame para o carregamento inicial
        self.initial_frame = ctk.CTkFrame(self)
        self.initial_frame.pack(fill="both", expand=True)

        label = ctk.CTkLabel(
            self.initial_frame,
            text="Selecione um arquivo OBJ para inicializar",
            font=("Arial", 24)
        )
        label.pack(pady=(50, 0))

        btn_load = ctk.CTkButton(
            self.initial_frame,
            text="Carregar Arquivo",
            command=self.load_file,
            font=("Arial", 16),
        )
        btn_load.pack(expand=True)

    def setup_main_ui(self):
        """Configura a interface completa após o carregamento do arquivo."""

        self.geometry("800x600")  # Define o tamanho da janela completa

        self.initial_frame.pack_forget()  # Limpar a interface inicial

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        button_container = ctk.CTkFrame(
            self.main_frame, fg_color="transparent")
        button_container.pack(expand=True)

        btn_consultar_aresta = ctk.CTkButton(
            button_container, text="Consultar Faces",
            command=lambda: self.open_consultation_window("Consultar as faces que compartilham um determinada aresta", self.consult_faces_sharing_edge))
        btn_consultar_aresta.pack(pady=(20, 10), padx=10)

        btn_consultar_vertice = ctk.CTkButton(
            button_container, text="Consultar Arestas",
            command=lambda: self.open_consultation_window("Consultar as arestas que compartilham um determinado vértice", self.consult_edges_sharing_vertex))
        btn_consultar_vertice.pack(pady=10, padx=10)

        btn_consultar_face = ctk.CTkButton(
            button_container, text="Consultar Vértices",
            command=lambda: self.open_consultation_window("Consultar os vértices que compartilham uma determinada face", self.consult_vertices_sharing_face))
        btn_consultar_face.pack(pady=10, padx=10)

        btn_load = ctk.CTkButton(
            button_container, text="Carregar um novo arquivo OBJ", command=self.load_file)
        btn_load.pack(pady=10, padx=10)

        btn_transform = ctk.CTkButton(
            button_container, text="Aplicar uma transformação ao OBJ",
            command=lambda: self.open_transformation_window())
        btn_transform.pack(pady=10, padx=10)

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.plot_graph()

    def load_file(self):
        file_path = tk.filedialog.askopenfilename(
            title="Selecione um arquivo OBJ", filetypes=[("Mesh Files", "*.obj")])
        if file_path:
            try:

                self.mesh = op.read_3d_obj(file_path)
                self.setup_main_ui()

            except FileNotFoundError:
                CustomPopUp(self, title="Erro",
                            message="Arquivo não encontrado, tente novamente")
            except Exception as error:
                CustomPopUp(self, title="Erro Desconhecido",
                            message=str(error))

    def open_consultation_window(self, title, query_function):
        ''' Abre uma janela de consulta para o tipo de consulta especificado. '''
        if self.consultation_window is None or not self.consultation_window.winfo_exists():
            self.consultation_window = ConsultationWindow(
                self, title, query_function)
        else:
            self.consultation_window.focus()

    def open_transformation_window(self):
        if self.transformation_window is None or not self.transformation_window.winfo_exists():
            self.transformation_window = TransformationWindow(self, self.mesh)
        else:
            self.transformation_window.focus()

    def consult_faces_sharing_edge(self):
        ''' Consulta as faces que compartilham uma aresta. '''
        if self.mesh is None:
            CustomPopUp(self, title="Aviso",
                        message="Carregue um arquivo OBJ primeiro")
            return

        edge_id = self.consultation_window.entry.get()
        try:
            edge_id = int(edge_id)
            faces = op.get_faces_sharing_edge(self.mesh, edge_id)

            if not faces or len(faces) == 0:
                self.consultation_window.display_result(
                    f"Não há faces conectadas a aresta {edge_id}")
            else:
                self.consultation_window.display_result(
                    f"Faces que compartilham a aresta {edge_id}: {faces}")

        except ValueError or KeyError:
            self.consultation_window.display_result(
                "ID inválido!")

    def consult_edges_sharing_vertex(self):
        ''' Consulta as arestas que compartilham um vértice. '''
        if self.mesh is None:
            CustomPopUp(self, title="Aviso",
                        message="Carregue um arquivo OBJ primeiro")
            return

        vertex_id = self.consultation_window.entry.get()
        try:
            vertex_id = int(vertex_id)
            edges = op.get_edges_sharing_vertex(self.mesh, vertex_id)

            if not edges or len(edges) == 0:
                self.consultation_window.display_result(
                    f"Não há arestas conectadas ao vértice {vertex_id}")
            else:
                self.consultation_window.display_result(
                    f"Arestas que compartilham o vértice {vertex_id}: {edges}")
        except ValueError or KeyError:
            self.consultation_window.display_result(
                "ID inválido!")

    def consult_vertices_sharing_face(self):
        ''' Consulta os vértices que compartilham uma face. '''
        if self.mesh is None:
            CustomPopUp(self, title="Aviso",
                        message="Carregue um arquivo OBJ primeiro")
            return

        face_id = self.consultation_window.entry.get()
        try:
            face_id = int(face_id)
            vertices = op.get_vertices_sharing_face(self.mesh, face_id)
            self.consultation_window.display_result(
                f"Vértices que compartilham a face {face_id}: {vertices}")
        except ValueError or KeyError:
            self.consultation_window.display_result(
                "ID inválido!")
        except Exception as error:
                self.consultation_window.display_result(
                "ID inválido!")

    def plot_graph(self):
        ''' Plota o objeto 3D na interface. '''
        if self.mesh is None:
            CustomPopUp(self, title="Erro",
                        message="Carregue um arquivo OBJ primeiro")
        else:
            # Criar uma nova figura
            self.figure = Figure(figsize=(5, 4), dpi=100)
            ax = self.figure.add_subplot(111, projection='3d')

            # Plotar o objeto 3D
            op.plot_3d_object(
                self.mesh, ax,
                colors=['lightblue', 'skyblue', 'dodgerblue', 'royalblue'])

            # Limpar canvas antigo se existir
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            # Plotar no Frame da interface (não abrir uma nova janela)
            self.canvas = FigureCanvasTkAgg(
                self.figure, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
