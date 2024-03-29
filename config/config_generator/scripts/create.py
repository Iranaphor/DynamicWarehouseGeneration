import os, sys
import rospkg
import shutil
import yaml
from pprint import pprint

from folder import folder
from grid import grid
from world import world
from tmap import tmap


def create(CONFIG, yml_cats):

    """ Create rospackage """
    folder(save_as=CONFIG)

    """ Generate a grid using Wave-Form Collapse """
    Grid = grid(yml_cats)

    """ Call a GZServer Spawn Service to build the world.world file """
    world(Grid, yml_cats)

    """ Construct a tmap.tmap2 file """
    tmap(Grid, yml_cats)


if __name__=='__main__':
    CONFIG=sys.argv[1]
    path = rospkg.RosPack().get_path("config_generator")+"/config/%s.yaml"%(CONFIG)
    with open(path, 'r') as f:
        yml_cats = yaml.safe_load(f)
    yml_cats['CONFIG'] = CONFIG
    pprint(yml_cats)
    create(CONFIG, yml_cats)
