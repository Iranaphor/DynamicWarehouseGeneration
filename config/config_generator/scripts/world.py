#!/usr/bin/env python3


import time, os
import rospkg
import numpy as np
import yaml

def world(grid, yml_cats):
    renders = yml_cats['renderings']
    dims = yml_cats['grid']['resolution']
    sdf_folder = rospkg.RosPack().get_path("config_generator")+"/../warez_models/"

    def send_cmd (name, x, y, z=0, sdf="warehouse_shelf"):
        print("\n-------\nRendering: %s"%name)
        file = sdf_folder + "%s/%s.sdf"%(sdf,sdf)
        command = "rosrun gazebo_ros spawn_model -file %s -sdf -model %s -x %s -y %s -z %s"
        os.system(command%(file, name, x, y, z))

    for ri,r in enumerate(grid):
        for ci,c in enumerate(grid[ri]):
            if grid[ri][ci] > 0:
                x = ci*dims['x'] - (0.5*dims['x']*(len(grid)-1))
                y = ri*dims['y'] - (0.5*dims['y']*(len(grid[ri])-1))

                sdf = renders[grid[ri][ci]]['sdf']
                send_cmd("%s_%s_%s"%(sdf,ri,ci), x, y, sdf=sdf)
                time.sleep(0.1)



if __name__=='__main__':
    import rospy, sys
    rospy.init_node('world')
    CONFIG = sys.argv[1]


    path = rospkg.RosPack().get_path("config_generator")+"/../scenarios/scenario___%s/config/config.yaml"%(CONFIG)
    with open(path, 'r') as f:
        yml_cats = yaml.safe_load(f)
    yml_cats['CONFIG'] = CONFIG


    grid_path = rospkg.RosPack().get_path("config_generator")+"/../scenarios/scenario___%s/config/wfc.grid"%(CONFIG)
    with open(grid_path, 'rb') as f:
        grid = np.load(f)
    print(grid)

    world(grid, yml_cats)

