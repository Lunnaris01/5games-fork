from settings import *
from os import path, listdir


def load_animations(animation_root):

    animations = {}
    for animation_name in listdir(animation_root):

        animations[animation_name] = [pygame.image.load(path.join(animation_root,animation_name,frame)) for frame in sorted(listdir(path.join(animation_root,animation_name)))]

    return animations