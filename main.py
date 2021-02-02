'''Check the Ursina Game Engine page at https://github.com/pokepetter/ursina'''

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import camera_grayscale_shader

from chunk import Chunk
import utils
import threading, queue

compute_mesh_queue = queue.Queue()
render_distance = 3
condition = threading.Condition()

def update():
    condition.acquire()
    
    Chunk.generated_a_mesh_this_frame = False

    for chunk in world.values():
        chunk.update()

    condition.release()

def threaded_update():
    while executing:
        condition.acquire()

        player_pos_chunk = utils.player_to_chunk(player.position)
        for j in range(int(player_pos_chunk.z) - render_distance, int(player_pos_chunk.z)+render_distance):
            for i in range(int(player_pos_chunk.x) - render_distance, int(player_pos_chunk.x)+render_distance):
                if  not (Vec3(i,0,j) in world):
                    world.update({Vec3(i,0,j) : Chunk(position=Vec3(i,0,j))})
                    #print("Generating new chunk in {}, {}, {}".format(i,0,j))   

        for vec in world:
            if utils.vec2dist(utils.player_to_chunk(player.position).xz, vec.xz) > render_distance + 1:
                #print("Deleting chunk at " + str(vec))
                world[vec].destroy()
                todelete.append(vec)
            else:
                world[vec].update()

        for vec in todelete:
            del world[vec]
        todelete.clear()

        for chunk in world.values():
            chunk.compute_mesh()
        condition.release()
        time.sleep(0.5)

def quit():
    executing = False


if __name__ == "__main__":
    utils.initUtils()
    app = Ursina()

    # Dictionary to store world chunks (Vec3 position, Chunk)
    world = {}
    todelete = []

    #player = FirstPersonController(world_position=Vec3(8,100,8))
    #collision_zone = CollisionZone(parent=player, radius=32)
    player = EditorCamera()

    executing = True

    try:
        threading.Thread(target=threaded_update).start()
    except:
        print("Couldn't start update thread")

    window.vsync = False
    window.show_ursina_splash = True
    window.borderless = False
    window.fullscreen= True

    application.development_mode = False

    Sky()

    app.run()