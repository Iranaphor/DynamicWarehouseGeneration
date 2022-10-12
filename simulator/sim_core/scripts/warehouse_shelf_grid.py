import time, os

def send_cmd (name, x, y, z=0):
    file = "~/warez/src/warez/config/warehouse_gazebo_models/warehouse_shelf/warehouse_shelf.sdf"
    command = "rosrun gazebo_ros spawn_model -file %s -sdf -model %s -x %s -y %s -z %s"
    os.system(command%(file, name, x, y, z))

shelf_dim = [0.65, 0.65]

grid = [
[0, 1, 1, 0, 1, 1, 0],
[0, 1, 1, 0, 1, 1, 0],
[0, 1, 1, 0, 0, 0, 0],
[0, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0]]

import numpy as np
N = 25; p=0.65; grid=np.random.choice(a=[False, True], size=(N, N), p=[p, 1-p])

for ri,r in enumerate(grid):
    for ci,c in enumerate(grid[ri]):
        if grid[ri][ci]:
            x = ci*shelf_dim[0] - (0.5*shelf_dim[0]*(len(grid)-1))
            y = ri*shelf_dim[1] - (0.5*shelf_dim[1]*(len(grid[ri])-1))
            send_cmd("shelf_%s_%s"%(ri,ci), x, y)
            time.sleep(0.2)
