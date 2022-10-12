import time, os
import numpy as np
from wfc import wfc


## CONFIGURATION

shelf_dim = [0.65, 0.65]
output_siz = (32, 32)
render = False
pixels = [[000, 000, 000, 000, 000, 000],
          [000, 000, 000, 111, 000, 000],
          [000, 111, 000, 111, 000, 000],
          [000, 111, 111, 111, 111, 000],
          [000, 000, 000, 000, 111, 000],
          [000, 000, 000, 000, 000, 000]]


## PRINTING

def pretty(img, name=''):
    labels = {'0':['   ', 'walkway'],   '1':['[_]','shelf'],   '2':['{X}','obstruction']}
    keys=' | '.join(["\"%s\" : %s"%(l[0],l[1]) for l in labels.values()])
    kl = '-'*len(keys)

    image = img.copy().astype(str)
    for k,v in labels.items():
        image[image==k] = v[0]

    print('\n'+kl+"\n"+name)
    print('\n'.join([''.join(o) for o in np.flip(image, (0))]))
    print(kl+"\n"+keys+"\n"+kl+"\n\n")


## GENERATOR CODE

pixels = [[111-c for c in r] for r in pixels]
pixe = np.where(np.array(pixels)==0, 1, 0)
pixels = [[c for c in r] for r in pixels]
#print("----\nPixel input:")
#print('\n'.join([''.join(map(str,p)) for p in pixe]))
pretty(np.where(np.array(pixe).astype(np.uint8)==0,0,2), name="Pixel Input:")


pix = np.array(wfc(pixels, input_size=np.array(pixels).shape, output_size=output_siz))
np.set_printoptions(linewidth=150)

grid = np.where(pix==0, True, False)
pretty(grid.astype(np.uint8)*2, name="WCF Output:")


## FILL HOLES

import cv2
base = np.pad(np.where(pix==0, 1, 0).astype(np.uint8),2)

h,w = base.shape
mask = np.zeros((h+2, w+2), np.uint8)

cv2.floodFill(base, mask, (0,0), 2)

out = np.flip(np.where(mask==0, '[X]', '   ')[3:-3, 3:-3], (0))
grid = np.flip(np.where(mask==0, 1, 0)[2:-2, 2:-2], (0))

pretty(2-base[2:-2,2:-2], name="Pole Renderings:")


## GENERATE CODE

def send_cmd (name, x, y, z=0, sdf="warehouse_shelf"):
    print("\nRendering: %s"%name)
    file = "~/warez/src/warez/config/warehouse_gazebo_models/%s/%s.sdf"%(sdf,sdf)
    command = "rosrun gazebo_ros spawn_model -file %s -sdf -model %s -x %s -y %s -z %s"
    os.system(command%(file, name, x, y, z))

if render:
    for ri,r in enumerate(grid):
        for ci,c in enumerate(grid[ri]):
            if grid[ri][ci] > 0:
                x = ci*shelf_dim[0] - (0.5*shelf_dim[0]*(len(grid)-1))
                y = ri*shelf_dim[1] - (0.5*shelf_dim[1]*(len(grid[ri])-1))

                renders = {2:'warehouse_shelf', 1:'pole'}
                send_cmd("shelf_%s_%s"%(ri,ci), x, y, sdf=renders[grid[ri][ci]])
                time.sleep(0.2)


