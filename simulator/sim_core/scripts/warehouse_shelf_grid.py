import time, os
import numpy as np
from wfc import wfc


## SEEDING
#import random
#new_seed = random.random()
#random.seed(new_seed)
#print(0.9908590606333316) #new_seed)
# :( ? -  doesnt work for some reason

## CONFIGURATION

shelf_dim = [0.65, 0.65]
output_siz = (32, 32)
render = True
pixels = [[000, 000, 000, 000, 000, 000],
          [000, 000, 000, 000, 000, 000],
          [000, 000, 111, 111, 000, 000],
          [000, 000, 111, 000, 000, 000],
          [000, 000, 000, 000, 000, 000],
          [000, 000, 000, 000, 000, 000]]


## GENERATOR CODE

pixels = [[111-c for c in r] for r in pixels]
pixe = np.where(np.array(pixels)==0, 1, 0)
pixels = [[c for c in r] for r in pixels]
print('\n'.join([''.join(map(str,p)) for p in pixe]))


pix = np.array(wfc(pixels, input_size=np.array(pixels).shape, output_size=output_siz))
np.set_printoptions(linewidth=150)

out  = np.where(pix==0, '[X]', ' * ')
grid = np.where(pix==0, True, False)
print('\n'.join([''.join(o) for o in np.flip(out, (0))]))


def send_cmd (name, x, y, z=0):
    file = "~/warez/src/warez/config/warehouse_gazebo_models/warehouse_shelf/warehouse_shelf.sdf"
    command = "rosrun gazebo_ros spawn_model -file %s -sdf -model %s -x %s -y %s -z %s"
    os.system(command%(file, name, x, y, z))


for ri,r in enumerate(grid):
    for ci,c in enumerate(grid[ri]):
        if grid[ri][ci]:
            x = ci*shelf_dim[0] - (0.5*shelf_dim[0]*(len(grid)-1))
            y = ri*shelf_dim[1] - (0.5*shelf_dim[1]*(len(grid[ri])-1))
            if render:
                send_cmd("shelf_%s_%s"%(ri,ci), x, y)
                print("shelf_%s_%s"%(ri,ci))
                time.sleep(0.2)


