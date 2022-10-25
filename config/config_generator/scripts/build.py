#!/usr/bin/env python3

import os, sys, time
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

    """ Construct a tmap.tmap2 file """
    tmap(Grid, yml_cats)


if __name__=='__main__':
    import rospy, sys
    from std_msgs.msg import String as Str

    print("1")
    rospy.init_node('build')
    CONFIG = sys.argv[1]
    print("2")
    pub = rospy.Publisher('~complete', Str, queue_size=5)

    path = rospkg.RosPack().get_path("config_generator")+"/config/%s.yaml"%(CONFIG)
    with open(path, 'r') as f:
        yml_cats = yaml.safe_load(f)
    yml_cats['CONFIG'] = CONFIG
    print("3")
    pprint(yml_cats)
    create(CONFIG, yml_cats)

    print("4")
    time.sleep(2)
    pub.publish(Str("complete"))
    print("5")
