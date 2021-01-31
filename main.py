'''Check the Ursina Game Engine page at https://github.com/pokepetter/ursina'''

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import camera_grayscale_shader

from chunk import Chunk
from utils import *

import threading, queue

q = queue.Queue()
render_distance = 2


def update():
    for j in range(int(player.position.z/16) - render_distance, int(player.position.z/16)+render_distance):
        for i in range(int(player.position.x/16) - render_distance, int(player.position.x/16)+render_distance):
            if  not (Vec3(i,0,j) in world):
                world.update({Vec3(i,0,j) : Chunk(position=Vec3(i,0,j))})
                #print("Generating new chunk in {}, {}, {}".format(i,0,j))   

    for vec in world:
        world[vec].update()
        q.put(world[vec])

    # for vec in world:
    #     if vec3dist(player_to_chunk(player.position, world[vec].size), vec) > render_distance+1:
    #         print("Deleting chunk at " + str(vec))
    #         world[vec].destroy()
    #         todelete.append(vec)
    #     else:
    #         world[vec].update()
    #         if(world[vec].needs_update == True):
    #             q.put(world[vec])

    # for vec in todelete:
    #     del world[vec]
    # todelete.clear()

def threaded_update():
    while(1):
        chunk = q.get()
        chunk.compute_mesh()
        q.task_done()

if __name__ == "__main__":
    initUtils()
    app = Ursina()

    # Dictionary to store world chunks (Vec3 position, Chunk)
    world = {}
    todelete = []

    player = FirstPersonController(world_position=Vec3(8,35,8))
    collision_zone = CollisionZone(parent=player, radius=32)
    #player = EditorCamera()

    try:
        threading.Thread(target=threaded_update, daemon=True).start()
    except:
        print("Couldn't start update thread")

    window.vsync = False
    window.show_ursina_splash = True

    app.run()