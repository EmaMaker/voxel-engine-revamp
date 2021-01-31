from ursina import *
from opensimplex import OpenSimplex

chunk_size = 16

def initUtils():
    global simplex
    simplex = OpenSimplex()

def simplex2d(x, y):
    global simplex
    return simplex.noise2d(x=x, y=y)

# Courtesy of Arduino
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def player_to_chunk(player):
    return Vec3(int(player.x / chunk_size), int(player.y / chunk_size), int(player.z / chunk_size))

def vec3dist(vec1, vec2):
    return sqrt( (vec1.x-vec2.x)**2 + (vec1.y-vec2.y)**2  + (vec1.z-vec2.z)**2 )

def vec2dist(vec1, vec2):
    return sqrt( (vec1.x-vec2.x)**2 + (vec1.y-vec2.y)**2  )