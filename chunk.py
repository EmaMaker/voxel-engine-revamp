from blocks import *
from ursina import *
import utils
import threading

class Chunk(object):

    generated_a_mesh_this_frame = False

    def __init__(self, position=Vec3(0, 0, 0)):
        self.position = position
        utils.chunk_size = 16

        self.requestUpdate()
        self.mesh = None
        
        # Dictionary to store chunks blocks (Vec3 position, BlockType)
        self.blocks = {}
        self.generateOpenSimplex()

    def update(self):
        self.generate_mesh()

    # Generate a mesh using quads
    def generate_mesh(self):
        if self.computed_mesh and not Chunk.generated_a_mesh_this_frame:
            self.mesh = Entity(model=Mesh(
                vertices=self.mesh_data[0], triangles=self.mesh_data[1], normals=self.mesh_data[2], colors=self.mesh_data[3]), scale=1)
            self.mesh.origin = Vec3.zero
            self.mesh.position = self.position * utils.chunk_size
            self.mesh.collider = MeshCollider(
                self.mesh, mesh=self.mesh.model, center=self.mesh.origin)

            self.computed_mesh = False
            Chunk.generated_a_mesh_this_frame = True
            #print("Generating mesh for chunk at " + str(self.position))

    def compute_mesh(self):
        # print("Updating chunk " + str(self))
        if self.needs_update is True:
            verts = ()
            tris = ()
            #uvs = ()
            norms = ()
            colors = ()

            for i in self.blocks:
                # print("Updating block " + str(i))

                # Left
                if not Vec3(i.x-1, i.y, i.z) in self.blocks or self.blocks.get(Vec3(i.x-1, i.y, i.z)) == BlockType.AIR:
                    verts = verts + (i, Vec3(i.x, i.y, i.z+1),
                                    Vec3(i.x, i.y+1, i.z+1), Vec3(i.x, i.y+1, i.z))
                    tris = tris + ((len(verts)-4, len(verts)-1, len(verts)-2),
                                (len(verts)-4, len(verts)-2, len(verts)-3))
                    norms = norms + ((-1, 0, 0), (-1, 0, 0),
                                    (-1, 0, 0), (-1, 0, 0))
                    colors = colors + (color.red, color.blue,
                                    color.lime, color.black)
                # Right
                if not Vec3(i.x+1, i.y, i.z) in self.blocks or self.blocks.get(Vec3(i.x+1, i.y, i.z)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x+1, i.y, i.z), Vec3(i.x+1, i.y, i.z+1),
                                    Vec3(i.x+1, i.y+1, i.z+1), Vec3(i.x+1, i.y+1, i.z))
                    tris = tris + ((len(verts)-3, len(verts)-2, len(verts)-4),
                                (len(verts)-2, len(verts)-1, len(verts)-4))
                    norms = norms + ((1, 0, 0), (1, 0, 0),
                                    (1, 0, 0), (1, 0, 0))
                    colors = colors + (color.red, color.blue,
                                    color.lime, color.black)

                # Front
                if not Vec3(i.x, i.y, i.z+1) in self.blocks or self.blocks.get(Vec3(i.x, i.y, i.z+1)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y, i.z+1), Vec3(i.x+1, i.y, i.z+1),
                                    Vec3(i.x+1, i.y+1, i.z+1), Vec3(i.x, i.y+1, i.z+1))
                    tris = tris + ((len(verts)-4, len(verts)-1, len(verts)-2),
                                (len(verts)-4, len(verts)-2, len(verts)-3))
                    norms = norms + ((1, 0, 0), (1, 0, 0),
                                    (1, 0, 0), (1, 0, 0))
                    colors = colors + (color.red, color.blue,
                                    color.lime, color.black)

                # Back
                if not Vec3(i.x, i.y, i.z-1) in self.blocks or self.blocks.get(Vec3(i.x, i.y, i.z-1)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y, i.z), Vec3(i.x+1, i.y, i.z),
                                    Vec3(i.x+1, i.y+1, i.z), Vec3(i.x, i.y+1, i.z))
                    tris = tris + ((len(verts)-3, len(verts)-2, len(verts)-4),
                                (len(verts)-2, len(verts)-1, len(verts)-4))
                    norms = norms + ((1, 0, 0), (1, 0, 0),
                                    (1, 0, 0), (1, 0, 0))
                    colors = colors + (color.red, color.blue,
                                    color.lime, color.black)

                # Top
                if not Vec3(i.x, i.y+1, i.z) in self.blocks or self.blocks.get(Vec3(i.x, i.y+1, i.z)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y+1, i.z), Vec3(i.x+1, i.y+1, i.z),
                                    Vec3(i.x+1, i.y+1, i.z+1), Vec3(i.x, i.y+1, i.z+1))
                    tris = tris + ((len(verts)-3, len(verts)-2, len(verts)-4),
                                (len(verts)-2, len(verts)-1, len(verts)-4))
                    norms = norms + ((1, 0, 0), (1, 0, 0),
                                    (1, 0, 0), (1, 0, 0))
                    colors = colors + (color.red, color.blue,
                                    color.lime, color.black)

                # Back
                if not Vec3(i.x, i.y-1, i.z) in self.blocks or self.blocks.get(Vec3(i.x, i.y-1, i.z)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y, i.z), Vec3(i.x+1, i.y, i.z),
                                    Vec3(i.x+1, i.y, i.z+1), Vec3(i.x, i.y, i.z+1))
                    tris = tris + ((len(verts)-4, len(verts)-1, len(verts)-2),
                                (len(verts)-4, len(verts)-2, len(verts)-3))
                    norms = norms + ((1, 0, 0), (1, 0, 0),
                                    (1, 0, 0), (1, 0, 0))
                    colors = colors + (color.red, color.blue,
                                    color.lime, color.black)

            self.needs_update = False
            self.computed_mesh = True

            self.mesh_data = (verts, tris, norms, colors)

            #print("Updated mesh for chunk at " + str(self.position))
        
    def requestUpdate(self):
        #print("Requested update for " + str(self))
        self.needs_update = True
        self.computed_mesh = False

    def destroy(self):
        destroy(self.mesh)

    def placeBlockAt(self, x, y, z, type):
        self.blocks.update({Vec3(x, y, z): type})

    def generatePlain(self):
        for i in range(0, utils.chunk_size):
            for k in range(0, utils.chunk_size):
                self.placeBlockAt(i, 0, k, BlockType.GRASS)

    def generateOpenSimplex(self):
        self.generatePlain()
        for i in range(0, utils.chunk_size):
            for k in range(0, utils.chunk_size):
                value = utils.map(utils.simplex2d((self.position.x*utils.chunk_size+i)*0.025,
                                                  (self.position.z*utils.chunk_size+k)*0.025), -1, 1, 0, utils.chunk_size)
                for j in range(0, int(value)):
                    self.placeBlockAt(i, j, k, BlockType.GRASS)
