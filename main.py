'''Check the Ursina Game Engine page at https://github.com/pokepetter/ursina'''

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import camera_grayscale_shader

from chunk import Chunk
app = Ursina()

# Dictionary to store world chunks (Vec3 position, Chunk)
world = {}

def update():

    render_distance = 3

    for j in range(int(player.position.z/16) - render_distance, int(player.position.z/16)+render_distance):
        for i in range(int(player.position.x/16) - render_distance, int(player.position.x/16)+render_distance):
            if not Vec3(i,0,j) in world:
                chunk = Chunk(position=Vec3(i,0,j))
                world.update({Vec3(i,0,j) : chunk})
                print("Generating new chunk in {}, {}, {}".format(i,0,j))

    for chunk in world.values():
        chunk.generate_mesh()
    
    #print("Player At " + str(player.position))

if __name__ == "__main__":

    player = FirstPersonController()
    app.run()