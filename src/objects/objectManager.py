from src.objects.objloader import OBJ
from OpenGL.GL import *

class ObjectManager:
    """Handles loading and rendering of multiple OBJ objects in the scene."""
    
    def __init__(self):
        self.objects = {}

    def load_object(self, name, path, scale=1.0, position=(0, 0, 0), rotation=(0, 0, 0)):
        """Loads an OBJ file and stores it with metadata."""
        obj = OBJ(path, swapyz=True)
        self.objects[name] = {
            "obj": obj,
            "scale": scale,
            "position": position,
            "rotation": rotation
        }

    def render_objects(self):
        """Renders all loaded objects in the scene."""
        
        for obj_data in self.objects.values():
            glPushMatrix()
            
            # Apply transformations
            glTranslatef(*obj_data["position"])
            glScalef(obj_data["scale"], obj_data["scale"], obj_data["scale"])
            glRotatef(obj_data["rotation"][0], 1, 0, 0)
            glRotatef(obj_data["rotation"][1], 0, 1, 0)
            glRotatef(obj_data["rotation"][2], 0, 0, 1)

            # Render the object
            obj_data["obj"].render()
            glPopMatrix()
       
