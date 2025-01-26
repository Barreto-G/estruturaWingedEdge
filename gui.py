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
        self.title("Sistema Gráfico Interativo")
        self.geometry("800x600")
        self.scene = None  # Armazena a cena com os objetos
        self.figure = None
        self.canvas = None
        self.consultation_window = None
        self.transformation_window = None
        self.current_object_id = None  # Armazena o ID do objeto selecionado
        self.radio_var = tk.IntVar()
        self.setup_initial_ui()

    def setup_initial_ui(self):
        """Configura a interface inicial com o botão para carregar o arquivo OBJ."""
        self.geometry("500x200")

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
        self.geometry("1000x600")
        self.initial_frame.pack_forget()

        # Container principal
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True)

        # Painel esquerdo para lista de objetos
        self.object_panel = ctk.CTkFrame(main_container, width=200)
        self.object_panel.pack(side=tk.LEFT, fill="y", padx=5, pady=5)
        
        # Título da lista de objetos
        objects_label = ctk.CTkLabel(
            self.object_panel,
            text="Objetos na Cena",
            font=("Arial", 16, "bold")
        )
        objects_label.pack(pady=5)

        # Frame para lista de objetos
        self.objects_frame = ctk.CTkFrame(self.object_panel)
        self.objects_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Popula a lista de objetos
        self.update_object_list()

        # Painel central para botões
        self.main_frame = ctk.CTkFrame(main_container)
        self.main_frame.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

        button_container = ctk.CTkFrame(
            self.main_frame, fg_color="transparent")
        button_container.pack(expand=True)

        btn_consultar_aresta = ctk.CTkButton(
            button_container, text="Consultar Faces",
            command=lambda: self.open_consultation_window(
                "Consultar as faces que compartilham uma determinada aresta", 
                self.consult_faces_sharing_edge)
        )
        btn_consultar_aresta.pack(pady=(20, 10), padx=10)

        btn_consultar_vertice = ctk.CTkButton(
            button_container, text="Consultar Arestas",
            command=lambda: self.open_consultation_window(
                "Consultar as arestas que compartilham um determinado vértice", 
                self.consult_edges_sharing_vertex)
        )
        btn_consultar_vertice.pack(pady=10, padx=10)

        btn_consultar_face = ctk.CTkButton(
            button_container, text="Consultar Vértices",
            command=lambda: self.open_consultation_window(
                "Consultar os vértices que compartilham uma determinada face", 
                self.consult_vertices_sharing_face)
        )
        btn_consultar_face.pack(pady=10, padx=10)

        btn_load = ctk.CTkButton(
            button_container, text="Carregar outro arquivo OBJ", 
            command=self.load_additional_file
        )
        btn_load.pack(pady=10, padx=10)

        btn_transform = ctk.CTkButton(
            button_container, text="Aplicar uma transformação ao OBJ",
            command=lambda: self.open_transformation_window()
        )
        btn_transform.pack(pady=10, padx=10)

        # Painel direito para visualização 3D
        self.plot_frame = ctk.CTkFrame(main_container)
        self.plot_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)

        self.plot_graph()

    def update_object_list(self):
        """Atualiza a lista de objetos na interface"""
        # Limpa objetos existentes
        for widget in self.objects_frame.winfo_children():
            widget.destroy()

        if self.scene and self.scene.objects:
            for obj_id in self.scene.objects:
                obj_frame = ctk.CTkFrame(self.objects_frame)
                obj_frame.pack(fill="x", padx=2, pady=2)

                # Cria botão de rádio para seleção do objeto
                radio_btn = ctk.CTkRadioButton(
                    obj_frame,
                    text=f"Objeto {obj_id}",
                    variable=self.radio_var,  # Use the IntVar
                    value=obj_id,
                    command=lambda id=obj_id: self.select_object(id)
                )
                radio_btn.pack(side=tk.LEFT, padx=5)

                # Adiciona informações do objeto
                obj = self.scene.objects[obj_id]
                info_text = f"V:{len(obj.vertices)} F:{len(obj.faces)}"
                info_label = ctk.CTkLabel(obj_frame, text=info_text)
                info_label.pack(side=tk.RIGHT, padx=5)

    def select_object(self, object_id):
        """Seleciona um objeto na cena"""
        if self.current_object_id == object_id:
            # Se clicar no mesmo objeto já selecionado, desseleciona
            self.current_object_id = None
            self.radio_var.set(0)  # Reset the radio button selection
        else:
            self.current_object_id = object_id
        self.plot_graph()  # Atualiza a visualização

    def load_file(self):
        """Carrega o primeiro arquivo OBJ"""
        file_path = tk.filedialog.askopenfilename(
            title="Selecione um arquivo OBJ", 
            filetypes=[("Mesh Files", "*.obj")]
        )
        if file_path:
            try:
                self.scene = op.read_3d_obj(file_path)
                self.setup_main_ui()
            except FileNotFoundError:
                CustomPopUp(self, title="Erro",
                          message="Arquivo não encontrado, tente novamente")
            except Exception as error:
                CustomPopUp(self, title="Erro Desconhecido",
                          message=str(error))

    def load_additional_file(self):
        """Carrega arquivos OBJ adicionais na cena"""
        file_path = tk.filedialog.askopenfilename(
            title="Selecione um arquivo OBJ", 
            filetypes=[("Mesh Files", "*.obj")]
        )
        if file_path:
            try:
                new_scene = op.read_3d_obj(file_path)
                # Adiciona os novos objetos à cena existente
                for obj_id, obj in new_scene.objects.items():
                    new_id = max(self.scene.objects.keys()) + 1 if self.scene.objects else 1
                    self.scene.add_object(new_id, obj)
                self.update_object_list()
                self.plot_graph()
            except Exception as error:
                CustomPopUp(self, title="Erro",
                          message=str(error))

    def open_consultation_window(self, title, query_function):
        if self.consultation_window is None or not self.consultation_window.winfo_exists():
            self.consultation_window = ConsultationWindow(
                self, title, query_function)
        else:
            self.consultation_window.focus()

    def open_transformation_window(self):
        if self.transformation_window is None or not self.transformation_window.winfo_exists():
            self.transformation_window = TransformationWindow(
                self, self.scene, self.current_object_id)
        else:
            self.transformation_window.focus()

    def consult_faces_sharing_edge(self):
        if not self.scene:
            CustomPopUp(self, title="Aviso",
                      message="Carregue um arquivo OBJ primeiro")
            return
        
        if self.current_object_id is None:
            CustomPopUp(self, title="Aviso",
                      message="Selecione um objeto primeiro")
            return

        edge_id = self.consultation_window.entry.get()
        try:
            edge_id = int(edge_id)
            faces = op.get_faces_sharing_edge(
                self.scene, edge_id, self.current_object_id)

            if not faces or len(faces) == 0:
                self.consultation_window.display_result(
                    f"Não há faces conectadas a aresta {edge_id}")
            else:
                self.consultation_window.display_result(
                    f"Faces que compartilham a aresta {edge_id}: {faces}")

        except (ValueError, KeyError):
            self.consultation_window.display_result(
                "ID inválido!")

    def consult_edges_sharing_vertex(self):
        if not self.scene:
            CustomPopUp(self, title="Aviso",
                      message="Carregue um arquivo OBJ primeiro")
            return

        if self.current_object_id is None:
            CustomPopUp(self, title="Aviso",
                      message="Selecione um objeto primeiro")
            return

        vertex_id = self.consultation_window.entry.get()
        try:
            vertex_id = int(vertex_id)
            edges = op.get_edges_sharing_vertex(
                self.scene, vertex_id, self.current_object_id)

            if not edges or len(edges) == 0:
                self.consultation_window.display_result(
                    f"Não há arestas conectadas ao vértice {vertex_id}")
            else:
                self.consultation_window.display_result(
                    f"Arestas que compartilham o vértice {vertex_id}: {edges}")
        except (ValueError, KeyError):
            self.consultation_window.display_result(
                "ID inválido!")

    def consult_vertices_sharing_face(self):
        if not self.scene:
            CustomPopUp(self, title="Aviso",
                      message="Carregue um arquivo OBJ primeiro")
            return

        if self.current_object_id is None:
            CustomPopUp(self, title="Aviso",
                      message="Selecione um objeto primeiro")
            return

        face_id = self.consultation_window.entry.get()
        try:
            face_id = int(face_id)
            vertices = op.get_vertices_sharing_face(
                self.scene, face_id, self.current_object_id)
            
            self.consultation_window.display_result(
                f"Vértices que compartilham a face {face_id}: {vertices}")
        except (ValueError, KeyError):
            self.consultation_window.display_result(
                "ID inválido!")

    def plot_graph(self):
        if self.scene is None:
            CustomPopUp(self, title="Erro",
                    message="Carregue um arquivo OBJ primeiro")
            return

        self.figure = Figure(figsize=(5, 4), dpi=100)
        ax = self.figure.add_subplot(111, projection='3d')

        # Plota todos os objetos com cores diferentes
        colors = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow']
        
        for i, obj_id in enumerate(self.scene.objects):
            # Se houver um objeto selecionado, destaca-o
            if obj_id == self.current_object_id:
                op.plot_3d_object(self.scene, ax, object_id=obj_id, 
                                colors=[colors[i]], highlight=True)
            else:
                op.plot_3d_object(self.scene, ax, object_id=obj_id, 
                                colors=[colors[i]])

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(
            self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()