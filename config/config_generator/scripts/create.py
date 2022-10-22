import os
import rospkg
import shutil

from grid import grid
from world import world
from tmap import tmap


"""  CONFIGURATION  """
CONFIG="warehouse_simple_2"


shelf_dim = [0.65, 0.65]
#shelf_dim = [1.0, 1.0]


#output_siz = (40, 40)
output_siz = (10, 10)


pixels = [[000, 000, 000, 000, 000, 000],
          [000, 000, 000, 111, 000, 000],
          [000, 111, 000, 111, 000, 000],
          [000, 111, 111, 111, 111, 000],
          [000, 000, 000, 000, 111, 000],
          [000, 000, 000, 000, 000, 000]]
#pixels = [[111, 000, 111],
#          [000, 111, 000],
#          [111, 111, 111]]


""" Create rospackage """
root = rospkg.RosPack().get_path('config_generator')+"/../scenarios/"
temp = root + "TEMPLATE"
pack = root + "scenario___"+CONFIG
if not os.path.exists(pack):
    shutil.copytree(temp, pack)
    with open(pack+"/CMakeLists.txt") as f: newText=f.read().replace("TEMPLATE", "scenario___"+CONFIG)
    with open(pack+"/CMakeLists.txt", "w") as f: f.write(newText)
    with open(pack+"/package.xml") as f: newText=f.read().replace("TEMPLATE", "scenario___"+CONFIG)
    with open(pack+"/package.xml", "w") as f: f.write(newText)


"""Generate a grid using Wave-Form Collapse"""
grid = grid(grid_size=output_siz, template=pixels, save_as=CONFIG)


"""Call a GZServer Spawn Service to build the world.world file"""
world(grid, shelf_dim, sdf="")


"""Construct a tmap.tmap2 file"""
tmap(grid, dims=shelf_dim, save_as=CONFIG)
