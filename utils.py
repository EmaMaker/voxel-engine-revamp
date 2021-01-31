from ursina import *

def player_to_chunk(player, size):
    return Vec3(int(player.x / size), int(player.y / size), int(player.z / size))

def vec3dist(vec1, vec2):
    return sqrt( (vec1.x-vec2.x)**2 + (vec1.y-vec2.y)**2  + (vec1.z-vec2.z)**2 )