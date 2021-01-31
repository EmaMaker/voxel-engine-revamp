from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import camera_grayscale_shader

from chunk import Chunk
app = Ursina()

# Dictionary to store world chunks (Vec3 position, Chunk)
world = {}

def update():

    render_distance = 3

    for j in range(int(camera.position.z/16) - render_distance, int(camera.position.z/16)+render_distance):
        for i in range(int(camera.position.x/16) - render_distance, int(camera.position.x/16)+render_distance):
            if not Vec3(i,0,j) in world:
                chunk = Chunk(position=(i,0,j))
                world.update({Vec3(i,0,j) : chunk})
                print("Generating new chunk in {}, {}, {}".format(i,0,j))


    for chunk in world.values():
        chunk.generate_mesh()


# player = FirstPersonController()
camera = EditorCamera()
''''chunk = Chunk(position=(0,0,0))
chunk1 = Chunk(position=(1,0,0))
world.update({Vec3(0,0,0) : chunk})
world.update({Vec3(1,0,0) : chunk1})'''
app.run()