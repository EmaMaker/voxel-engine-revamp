from blocks import *
from ursina import *

class Chunk:
    def __init__(self, position=Vec3(0, 0, 0)):
        self.position = position
        self.size = 16

        self.update = True

        # Dictionary to store chunks blocks (Vec3 position, BlockType)
        self.blocks = {}

        for i in range(0, self.size):
            for k in range(0, self.size):
                self.blocks.update({Vec3(i, 0, k): BlockType.GRASS})

    # Generate a mesh using quads
    def generate_mesh(self):
        if self.update is True:

            # print("Updating chunk " + str(self))

            verts = ()
            tris = ()
            #uvs = ()
            norms = ()
            colors = ()

            for i in self.blocks:
                # print("Updating block " + str(i))

                # Left
                if not Vec3(i.x-1, i.y, i.z) in self.blocks or self.blocks.get(Vec3(i.x-1, i.y, i.z)) == BlockType.AIR:
                    verts = verts + (i, Vec3(i.x, i.y, i.z+1), Vec3(i.x, i.y+1, i.z+1), Vec3(i.x, i.y+1, i.z))
                    tris = tris + ((len(verts)-4, len(verts)-1, len(verts)-2), (len(verts)-4, len(verts)-2, len(verts)-3))
                    norms = norms + ((-1,0,0), (-1,0,0), (-1,0,0), (-1,0,0))
                    colors = colors + (color.red, color.blue, color.lime, color.black)
                # Right
                if not Vec3(i.x+1, i.y, i.z) in self.blocks or self.blocks.get(Vec3(i.x+1, i.y, i.z)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x+1, i.y, i.z), Vec3(i.x+1, i.y, i.z+1), Vec3(i.x+1, i.y+1, i.z+1), Vec3(i.x+1, i.y+1, i.z))
                    tris = tris + ((len(verts)-3, len(verts)-2, len(verts)-4), (len(verts)-2, len(verts)-1, len(verts)-4))
                    norms = norms + ((1,0,0), (1,0,0), (1,0,0), (1,0,0))
                    colors = colors + (color.red, color.blue, color.lime, color.black)

                # Front
                if not Vec3(i.x, i.y, i.z+1) in self.blocks or self.blocks.get(Vec3(i.x, i.y, i.z+1)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y, i.z+1), Vec3(i.x+1, i.y, i.z+1), Vec3(i.x+1, i.y+1, i.z+1), Vec3(i.x, i.y+1, i.z+1))
                    tris = tris + ((len(verts)-4, len(verts)-1, len(verts)-2), (len(verts)-4, len(verts)-2, len(verts)-3))
                    norms = norms + ((1,0,0), (1,0,0), (1,0,0), (1,0,0))
                    colors = colors + (color.red, color.blue, color.lime, color.black)

                # Back
                if not Vec3(i.x, i.y, i.z-1) in self.blocks or self.blocks.get(Vec3(i.x, i.y, i.z-1)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y, i.z), Vec3(i.x+1, i.y, i.z), Vec3(i.x+1, i.y+1, i.z), Vec3(i.x, i.y+1, i.z))
                    tris = tris + ((len(verts)-3, len(verts)-2, len(verts)-4), (len(verts)-2, len(verts)-1, len(verts)-4))
                    norms = norms + ((1,0,0), (1,0,0), (1,0,0), (1,0,0))
                    colors = colors + (color.red, color.blue, color.lime, color.black)

                # Top
                if not Vec3(i.x, i.y+1, i.z) in self.blocks or self.blocks.get(Vec3(i.x, i.y+1, i.z)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y+1, i.z), Vec3(i.x+1, i.y+1, i.z), Vec3(i.x+1, i.y+1, i.z+1), Vec3(i.x, i.y+1, i.z+1))
                    tris = tris + ((len(verts)-3, len(verts)-2, len(verts)-4), (len(verts)-2, len(verts)-1, len(verts)-4))
                    norms = norms + ((1,0,0), (1,0,0), (1,0,0), (1,0,0))
                    colors = colors + (color.red, color.blue, color.lime, color.black)

                # Back
                if not Vec3(i.x, i.y-1, i.z) in self.blocks or self.blocks.get(Vec3(i.x, i.y-1, i.z)) == BlockType.AIR:
                    verts = verts + (Vec3(i.x, i.y, i.z), Vec3(i.x+1, i.y, i.z), Vec3(i.x+1, i.y, i.z+1), Vec3(i.x, i.y, i.z+1))
                    tris = tris + ((len(verts)-4, len(verts)-1, len(verts)-2), (len(verts)-4, len(verts)-2, len(verts)-3))
                    norms = norms + ((1,0,0), (1,0,0), (1,0,0), (1,0,0))
                    colors = colors + (color.red, color.blue, color.lime, color.black)

            self.mesh = Entity(model=Mesh(vertices=verts, triangles=tris, normals=norms, colors=colors), scale=1)
            self.mesh.origin = Vec3.zero
            self.mesh.position = self.position * self.size
            self.mesh.collider = MeshCollider(self.mesh, mesh=self.mesh.model, center=self.mesh.origin)

            self.update = False

    def requestChange(self):
        self.update = True

    def destroy(self):
        destroy(self.mesh)

