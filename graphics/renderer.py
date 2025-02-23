import OpenGL.GL as gl
import OpenGL.GLU as glu
import numpy as np

from enum import Enum, auto

class RenderMode(Enum):
    WIREFRAME = auto()
    SOLID = auto()
    SOLID_WIREFRAME = auto()

class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas
        
        self._camera_position = np.array([20.0, 20.0, 20.0], dtype=np.float32)
        self.camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        self.fov = 60.0
        self.near = 0.1
        self.far = 100.0
        
        self.render_mode = RenderMode.SOLID_WIREFRAME
    
    def resize(self, event):
        """Gerencia o redimensionamento do canvas."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        gl.glViewport(0, 0, width, height)
    
    def _render_face(self, face_vertices, obj):
        """Renderiza uma face."""
        if self.render_mode in [RenderMode.SOLID, RenderMode.SOLID_WIREFRAME]:
            gl.glColor3f(0.0, 0.9, 1.0)  # Ciano
            
            # Triangulação da face
            if len(face_vertices) > 3:
                # Para faces com 4 vértices (quadriláteros)
                gl.glBegin(gl.GL_TRIANGLES)
                # Primeiro triângulo
                pos = obj.get_transformed_vertex(face_vertices[0].id)
                gl.glVertex3f(*pos)
                pos = obj.get_transformed_vertex(face_vertices[1].id)
                gl.glVertex3f(*pos)
                pos = obj.get_transformed_vertex(face_vertices[2].id)
                gl.glVertex3f(*pos)
                # Segundo triângulo
                pos = obj.get_transformed_vertex(face_vertices[0].id)
                gl.glVertex3f(*pos)
                pos = obj.get_transformed_vertex(face_vertices[2].id)
                gl.glVertex3f(*pos)
                pos = obj.get_transformed_vertex(face_vertices[3].id)
                gl.glVertex3f(*pos)
                gl.glEnd()
            else:
                # Para faces triangulares
                gl.glBegin(gl.GL_TRIANGLES)
                for vertex in face_vertices:
                    pos = obj.get_transformed_vertex(vertex.id)
                    gl.glVertex3f(*pos)
                gl.glEnd()
        
        if self.render_mode in [RenderMode.WIREFRAME, RenderMode.SOLID_WIREFRAME]:
            # Render wireframe
            gl.glColor3f(0.0, 0.0, 0.0)  # Preto para o wireframe
            gl.glBegin(gl.GL_LINE_LOOP)
            for vertex in face_vertices:
                pos = obj.get_transformed_vertex(vertex.id)
                gl.glVertex3f(*pos)
            gl.glEnd()
    
    def render(self, scene):
        """Renderiza a cena inteira."""        
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glCullFace(gl.GL_BACK)
        gl.glFrontFace(gl.GL_CCW)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = self.canvas.winfo_width() / self.canvas.winfo_height()
        glu.gluPerspective(self.fov, aspect, self.near, self.far)
        

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            *self._camera_position,
            *self.camera_target,
            *self.camera_up
        )
        
        if scene and scene.objects:
            for obj_id, obj in scene.objects.items():                
                for face in obj.faces.values():
                    face_vertices = obj.get_face_vertices(face.id)
                    if face_vertices:
                        self._render_face(face_vertices, obj)
    
    def set_camera(self, position, target, up):
        self._camera_position = np.array(position, dtype=np.float32)
        self.camera_target = np.array(target, dtype=np.float32)
        self.camera_up = np.array(up, dtype=np.float32)
    
    def reset_camera(self):
        self._camera_position = np.array([20.0, 20.0, 20.0], dtype=np.float32)
        self.camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)