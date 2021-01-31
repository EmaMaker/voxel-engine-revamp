'''Check the Ursina Game Engine page at https://github.com/pokepetter/ursina'''

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import camera_grayscale_shader

from chunk import Chunk
from utils import *

def update():

    render_distance = 2

    for j in range(int(player.position.z/16) - render_distance, int(player.position.z/16)+render_distance):
        for i in range(int(player.position.x/16) - render_distance, int(player.position.x/16)+render_distance):
            if  not (Vec3(i,0,j) in world):
                chunk = Chunk(position=Vec3(i,0,j))
                chunk.generate_mesh()
                world.update({Vec3(i,0,j) : chunk})
                print("Generating new chunk in {}, {}, {}".format(i,0,j))   

    for vec in world:
        if vec3dist(player_to_chunk(player.position, world[vec].size), vec) > render_distance+1:
            print("Deleting chunk at " + str(vec))
            world[vec].destroy()
            todelete.append(vec)

    for vec in todelete:
        del world[vec]
    todelete.clear()
    
    #print("Player At " + str(player.position))

if __name__ == "__main__":
    app = Ursina()

    # Dictionary to store world chunks (Vec3 position, Chunk)
    world = {}
    todelete = []

    player = FirstPersonController()
    app.run()