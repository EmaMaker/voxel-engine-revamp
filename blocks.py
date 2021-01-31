from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class BlockType(Enum):
    AIR = 0
    GRASS = 1
    STONE = 2

class VoxelQuad(Button):
    def __init__(self, chunk, position=(0,0,0), normal=(0,1,0)):
        super().__init__(
            parent = scene,
            position = position,
            origin_y = .5,
            model = 'quad',
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )
        self.chunk = chunk

    '''def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position=self.position + mouse.normal)
                chunk.requestChange()

            if key == 'right mouse down':
                destroy(self)
                chunk.requestChange()'''
