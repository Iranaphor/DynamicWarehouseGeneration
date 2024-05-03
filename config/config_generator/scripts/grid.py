import sys
import yaml
from pprint import pprint
import cv2
import rospkg
import numpy as np

from wfc import wfc


def printer(img, labels, name=''):
    keys=' | '.join(["\"%s\" : %s"%(l['icon'],l['sdf']) for l in labels.values()])
    kl = '-'*len(keys)

    image = img.copy().astype(str)
    for k,v in labels.items():
        image[image==str(k)] = v['icon']

    print('\n'+kl+"\n"+name)
    print('\n'.join([''.join(o) for o in np.flip(image, (0))]))
    print(kl+"\n"+keys+"\n"+kl+"\n\n")



def grid(yml_cats):
    grid_size = (yml_cats['grid']['size']['h'], yml_cats['grid']['size']['w'])
    template = [r for r in yml_cats['wfc_template']]
    save_as = yml_cats['save_as']
    labels = yml_cats['renderings']

    pixels = [[111-c for c in r] for r in template]
    pixe = np.where(np.array(pixels)==0, 1, 0)
    pixels = [[c for c in r] for r in pixels]
    printer(np.where(np.array(pixe).astype(np.uint8)==0,0,2), labels, name="Pixel Input:")

    pix = np.array(wfc(pixels, input_size=np.array(pixels).shape, output_size=grid_size))
    np.set_printoptions(linewidth=150)

    grid = np.where(pix==0, True, False)
    printer(grid.astype(np.uint8)*2, labels, name="WCF Output:")


    ## Fill holes
    base = np.pad(np.where(pix==0, 1, 0).astype(np.uint8),2)

    h,w = base.shape
    mask = np.zeros((h+2, w+2), np.uint8)

    cv2.floodFill(base, mask, (0,0), 2)

    grid = np.pad(np.pad(2-base[2:-2,2:-2], pad_width=1, constant_values=0), pad_width=1, constant_values=2)
    printer(grid, labels, name="Pole Renderings:")

    ## Fill secondary holes (where shelf is blocked by poles)


    ## Save output
    if save_as:
        path = rospkg.RosPack().get_path("config_generator")+"/../scenarios/scenario___%s/config/wfc.grid"%(save_as)
        with open(path, 'wb') as f:
            np.save(f, grid)
    return grid



if __name__=='__main__':
    if len(sys.argv) > 1:
        config_filepath = sys.argv[1]
    else:
        config_filepath = os.getenv('CONFIG_FILEPATH')

    """ Load yaml file """
    with open(config_filepath, 'r') as f:
        yml_cats = yaml.safe_load(f)
    yml_cats['CONFIG'] = config_filepath
    yml_cats['save_as'] = False

    pprint(yml_cats)

    """ Generate a grid using Wave-Form Collapse """
    Grid = grid(yml_cats)

