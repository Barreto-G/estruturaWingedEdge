import numpy as np

class CameraController:
    def __init__(self, renderer):
        self.renderer = renderer

        # Estados do mouse
        self.last_x = 0
        self.last_y = 0
        self.dragging = False

        # Par
        self.distance = np.linalg.norm(
            self.renderer._camera_position - self.renderer.camera_target
        )
        self.azimuth = 45.0  # Horizontal angle
        self.elevation = 35.264  # Vertical angle (arctan(1/√2))

        # Sensitivity
        self.rotation_speed = 0.25
        self.zoom_speed = 1.2
        self.pan_speed = 0.001

    def start_drag(self, x, y):
        self.last_x = x
        self.last_y = y
        self.dragging = True

    def end_drag(self):
        self.dragging = False

    def drag(self, x, y):
        if not self.dragging:
            return

        # Calculate delta movement
        dx = x - self.last_x
        dy = y - self.last_y

        # Update angles with reduced speed
        self.azimuth += dx * self.rotation_speed
        self.elevation += dy * self.rotation_speed

        # Limit elevation to prevent camera flipping
        self.elevation = np.clip(self.elevation, -89.0, 89.0)

        # Convert spherical to cartesian coordinates
        phi = np.radians(self.azimuth)
        theta = np.radians(self.elevation)
        
        # Calculate new camera position
        camera_x = self.distance * np.cos(theta) * np.sin(phi)
        camera_y = self.distance * np.sin(theta)
        camera_z = self.distance * np.cos(theta) * np.cos(phi)
        
        # Update camera position
        self.renderer._camera_position = (
            self.renderer.camera_target + 
            np.array([camera_x, camera_y, camera_z], dtype=np.float32)
        )

        # Update last position
        self.last_x = x
        self.last_y = y

    def zoom(self, delta):
        # Update distance with zoom factor
        self.distance *= 0.9 if delta > 0 else 1.1
        self.distance = np.clip(self.distance, 1.0, 100.0)
        
        # Update camera position after zoom
        phi = np.radians(self.azimuth)
        theta = np.radians(self.elevation)
        
        camera_x = self.distance * np.cos(theta) * np.sin(phi)
        camera_y = self.distance * np.sin(theta)
        camera_z = self.distance * np.cos(theta) * np.cos(phi)
        
        self.renderer._camera_position = (
            self.renderer.camera_target + 
            np.array([camera_x, camera_y, camera_z], dtype=np.float32)
        )

    def pan(self, dx, dy):
        # Calculate camera right and up vectors
        forward = self.renderer.camera_target - self.renderer._camera_position
        forward = forward / np.linalg.norm(forward)
        
        right = np.cross(forward, self.renderer.camera_up)
        right = right / np.linalg.norm(right)
        
        up = np.cross(right, forward)
        up = up / np.linalg.norm(up)

        # Calculate pan movement
        pan_x = -right * (dx * self.pan_speed * self.distance)
        pan_y = up * (dy * self.pan_speed * self.distance)

        # Update camera position and target
        self.renderer._camera_position += pan_x + pan_y
        self.renderer.camera_target += pan_x + pan_y