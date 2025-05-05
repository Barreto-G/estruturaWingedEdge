import tkinter as tk
import customtkinter as ctk
from pyopengltk import OpenGLFrame
import OpenGL.GL as gl

class CustomOpenGLFrame(OpenGLFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderer = None
        self.scene = None

    def initgl(self):
        """Inicializa o contexto do OpenGL com fundo branco."""
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glCullFace(gl.GL_BACK)

    def redraw(self):
        """Renderiza a cena."""
        # Limpa o buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        if self.renderer and self.scene:
            self.renderer.render(self.scene)        
        self.tkSwapBuffers()

class TransformControlsFrame(ctk.CTkFrame):
    def __init__(self, parent, callback_handler):
        super().__init__(parent)
        self.callback_handler = callback_handler
        
        self.trans_vars = [ctk.DoubleVar(value=0.0) for _ in range(3)]
        self.rot_axis = ctk.StringVar(value='x')
        self.rot_angle = ctk.DoubleVar(value=0.0)
        self.scale_vars = [ctk.DoubleVar(value=1.0) for _ in range(3)]
        
        self._create_widgets()
        
    def _create_widgets(self):
        title = ctk.CTkLabel(self, text="Transformações", 
                    font=ctk.CTkFont(size=14, weight="bold"), width=200)
        title.pack(pady=5)
        
        trans_frame = ctk.CTkFrame(self)
        trans_frame.pack(fill="x", padx=5, pady=5)

        # Controles de Translação        
        ctk.CTkLabel(trans_frame, text="Translação").pack()

        for i, label in enumerate(['X:', 'Y:', 'Z:']):
            row = ctk.CTkFrame(trans_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=label, width=20).pack(side="left")
            ctk.CTkEntry(row, textvariable=self.trans_vars[i], 
                        width=80).pack(side="right", padx=5)            
        rot_frame = ctk.CTkFrame(self)
        rot_frame.pack(fill="x", padx=5, pady=5)
        
        # Controles de Rotação
        ctk.CTkLabel(rot_frame, text="Rotação").pack()
        
        axis_frame = ctk.CTkFrame(rot_frame)
        axis_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(axis_frame, text="Eixo:", width=15).pack(side="left")
        ctk.CTkOptionMenu(axis_frame, variable=self.rot_axis, 
                         values=['x', 'y', 'z'], width=80).pack(side="right", padx=5)
        
        angle_frame = ctk.CTkFrame(rot_frame)
        angle_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(angle_frame, text="Ângulo:", width=20).pack(side="left")
        ctk.CTkEntry(angle_frame, textvariable=self.rot_angle, 
                    width=80).pack(side="right", padx=5)
        
        scale_frame = ctk.CTkFrame(self)
        scale_frame.pack(fill="x", padx=5, pady=5)

        # Controles de Escala        
        ctk.CTkLabel(scale_frame, text="Escala").pack()
        
        for i, label in enumerate(['X:', 'Y:', 'Z:']):
            row = ctk.CTkFrame(scale_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=label, width=20).pack(side="left")
            ctk.CTkEntry(row, textvariable=self.scale_vars[i], 
                        width=80).pack(side="right", padx=5)
        
        # Botões
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="y", padx=5, pady=5)
        
        ctk.CTkButton(btn_frame, text="Aplicar Translação", 
                     command=self.callback_handler.apply_translation).pack(side="top", pady=2)
        ctk.CTkButton(btn_frame, text="Aplicar Rotação", 
                     command=self.callback_handler.apply_rotation).pack(side="top", pady=2)
        ctk.CTkButton(btn_frame, text="Aplicar Escala", 
                     command=self.callback_handler.apply_scale).pack(side="top", pady=2)
        ctk.CTkButton(btn_frame, text="Resetar", 
                     command=self.callback_handler.reset_transform).pack(side="top", pady=2)
    
class ObjectListFrame(ctk.CTkFrame):
    def __init__(self, parent, scene, callback_handler):
        super().__init__(parent)
        self.scene = scene
        self.callback_handler = callback_handler
        self.radio_var = tk.IntVar()
        
        objects_label = ctk.CTkLabel(
            self,
            text="Objetos",
            font=("Arial", 16, "bold")
        )
        objects_label.pack(pady=5)

        self.objects_frame = ctk.CTkFrame(self)
        self.objects_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
    
    def update_object_list(self, object_names):
        """Atualiza a lista de objetos"""
        for widget in self.objects_frame.winfo_children():
            widget.destroy()

        if self.scene and self.scene.objects:
            for obj_id in self.scene.objects:
                obj_frame = ctk.CTkFrame(self.objects_frame)
                obj_frame.pack(fill="x", padx=2, pady=2)

                radio_btn = ctk.CTkRadioButton(
                    obj_frame,
                    text=f"Nome: {object_names[obj_id]}",
                    variable=self.radio_var,
                    value=obj_id,
                    command=lambda id=obj_id: self.callback_handler.select_object(id)
                )
                radio_btn.pack(side=tk.LEFT, padx=5)

                obj = self.scene.objects[obj_id]
                info_text = f"Vértices: {len(obj.vertices)} Faces: {len(obj.faces)}"
                info_label = ctk.CTkLabel(obj_frame, text=info_text)
                info_label.pack(side=tk.RIGHT, padx=5)