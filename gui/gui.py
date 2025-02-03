import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox

from core import Scene, read_obj
from graphics import Renderer, CameraController, RenderMode
from .custom_widgets import CustomOpenGLFrame, TransformControlsFrame, ObjectListFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Gráfico Interativo")
        self.geometry("1450x880")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.selected_object_id = None
        self.scene = Scene()
        self.object_names = {}

        self._create_layout()

        self.canvas.bind('<ButtonPress-1>', self.on_mouse_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<Button-3>', self.on_right_click)
        self.canvas.bind('<B3-Motion>', self.on_right_drag)
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.canvas.bind('<Button-4>', self.on_mouse_wheel)
        self.canvas.bind('<Button-5>', self.on_mouse_wheel)
        self.canvas.bind('<Configure>', self.renderer.resize)            
    
    def _create_layout(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.object_list = ObjectListFrame(main_frame, self.scene, self)
        self.object_list.pack(side=tk.LEFT, fill="y", padx=5, pady=5)
        
        self.canvas = CustomOpenGLFrame(main_frame, width=800, height=600)
        self.canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.transform_controls = TransformControlsFrame(main_frame, self)
        self.transform_controls.pack(side="right", fill="y", padx=5, pady=5)
        
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Adicionar Objeto", command=self.add_object)
        file_menu.add_command(label="Remover Objeto", command=self.remove_selected_object)

        # Menu Visão
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visão", menu=view_menu)
        view_menu.add_command(label="Resetar Câmera", command=self.reset_view)
        
        # Submenu de modos de visualização
        render_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Modos", menu=render_menu)
        render_menu.add_command(label="Esqueleto", 
            command=lambda: self.set_render_mode(RenderMode.WIREFRAME))
        render_menu.add_command(label="Sólido", 
            command=lambda: self.set_render_mode(RenderMode.SOLID))
        render_menu.add_command(label="Sólido + Esqueleto (Padrão)", 
            command=lambda: self.set_render_mode(RenderMode.SOLID_WIREFRAME))
        
        self.renderer = Renderer(self.canvas)
        self.canvas.renderer = self.renderer
        self.canvas.scene = self.scene
        self.camera_controller = CameraController(self.renderer)       
        

    def select_object(self, object_id):
        """Seleciona um objeto na cena"""
        if self.selected_object_id == object_id:
            self.selected_object_id = None
            self.object_list.radio_var.set(0)
        else:
            self.selected_object_id = object_id
            self.scene.select_object(object_id)
            self.render_scene()

    def add_object(self):
        filetypes = [('OBJ files', '*.obj'), ('All files', '*.*')]
        filename = filedialog.askopenfilename(title="Open 3D Model", filetypes=filetypes)        
        if filename:
            try:
                new_object = read_obj(filename)
                if new_object and new_object.objects:
                    obj = list(new_object.objects.values())[0]
                    obj_id = self.scene.add_object(obj)
                    obj_name = filename.split('/')[-1].split('.')[0] # Deixa apenas o nome do arquivo sem o .obj
                    self.object_names[obj_id] = obj_name
                    
                    self.object_list.update_object_list(self.object_names)
                    self.render_scene()
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar o arquivo: {str(e)}")

    def remove_selected_object(self):
        if self.scene.remove_object(self.selected_object_id):
            del self.object_names[self.selected_object_id]
            self.selected_object_id = None
            self.scene.select_object(None)
            
            self.object_list.update_object_list(self.object_names)
            self.render_scene()

    def reset_view(self):
        self.renderer.reset_camera()
        self.render_scene()

    def render_scene(self):
        self.canvas.redraw()
        self.canvas.update_idletasks()

    def set_render_mode(self, mode: RenderMode):
        self.renderer.render_mode = mode
        self.render_scene()

    def on_mouse_press(self, event):
        self.camera_controller.start_drag(event.x, event.y)

    def on_mouse_release(self, event):
        self.camera_controller.end_drag()

    def on_mouse_drag(self, event):
        self.camera_controller.drag(event.x, event.y)
        self.render_scene()

    def on_right_click(self, event):
        self.camera_controller.start_drag(event.x, event.y)

    def on_right_drag(self, event):
        dx = event.x - self.camera_controller.last_x
        dy = event.y - self.camera_controller.last_y
        self.camera_controller.pan(dx, dy)
        self.camera_controller.last_x = event.x
        self.camera_controller.last_y = event.y
        self.render_scene()

    def on_mouse_wheel(self, event):
        if event.num == 5 or event.delta < 0:
            delta = -1 
        else:
            delta = 1

        self.camera_controller.zoom(delta)
        self.render_scene()

    def apply_translation(self):
        if not self.scene.selected_object:
            return
        
        obj = self.scene.selected_object
        dx, dy, dz = [var.get() for var in self.transform_controls.trans_vars]
        obj.add_transformation('Translação', (dx, dy, dz))
        self.render_scene()

    def apply_rotation(self):
        if not self.scene.selected_object:
            return
        
        obj = self.scene.selected_object
        axis = self.transform_controls.rot_axis.get()
        angle = self.transform_controls.rot_angle.get()
        obj.add_transformation('Rotação', (axis, angle))
        self.render_scene()

    def apply_scale(self):
        if not self.scene.selected_object:
            return
        
        obj = self.scene.selected_object
        sx, sy, sz = [var.get() for var in self.transform_controls.scale_vars]
        obj.add_transformation('Escala', (sx, sy, sz))
        self.render_scene()

    def reset_transform(self):
        if not self.scene.selected_object:
            return
        
        obj = self.scene.selected_object
        obj.clear_transformations()
        self.render_scene()