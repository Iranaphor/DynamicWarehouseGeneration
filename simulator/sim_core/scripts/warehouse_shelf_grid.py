import time, os
import numpy as np
from wfc import wfc


## CONFIGURATION

shelf_dim = [0.65, 0.65]
output_siz = (3, 3)
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

#out = np.flip(np.where(mask==0, '[X]', '   ')[3:-3, 3:-3], (0))
#grid = np.flip(np.where(mask==0, 1, 0)[2:-2, 2:-2], (0))

grid = np.pad(np.pad(2-base[2:-2,2:-2], pad_width=1, constant_values=0), pad_width=1, constant_values=2)
pretty(grid, name="Pole Renderings:")

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

                renders = {1:'warehouse_shelf', 2:'pole'}
                send_cmd("%s_%s_%s"%(renders[grid[ri][ci]],ri,ci), x, y, sdf=renders[grid[ri][ci]])
                time.sleep(0.2)





## GENERATE TMAP
#tmap_details = {'gen_time': '2022-06-23_13-10-11', 'location': 'riseholme'}
def get_tmap(tmap_details):
    return"""meta:
  last_updated: {gen_time}
metric_map: {location}
name: {location}_restrict
pointset: {location}_restrict
transformation:
  child: topo_map
  parent: map
  rotation:
    w: 1.0
    x: 0.0
    y: 0.0
    z: 0.0
  translation:
    x: 0.0
    y: 0.0
    z: 0.0
nodes:""".format(**tmap_details)

#verts = {'vert0':'*id00vert0', 'vert1':'*id00vert1', 'vert2':'*id00vert2'}
#node_details = {'name':name, 'location':location, 'vert': verts[type], 'x':x, 'y':y}
def get_node(node_details):
    return """
- meta:
    map: {location}
    node: {name}
    pointset: {location}_restrict
  node:
    localise_by_topic: ''
    parent_frame: map
    name: {name}
    pose:
      orientation:
        w: 0.7897749049165983
        x: 0.0
        y: 0.0
        z: -0.6133967717260812
      position:
        x: {x}
        y: {y}
        z: 0.0
    properties:
      xy_goal_tolerance: 0.3
      yaw_goal_tolerance: 0.1
    restrictions_planning: 'True'
    restrictions_runtime: obstacleFree_1
    verts: {vert}
""".format(**node_details)

#edge_details = {'name':'WayPoint140', 'name2':'WayPoint142', 'action':'move_base', 'action_type':'move_base_msgs/MoveBaseGoal'}
def get_edge(edge_details):
    return """
    - edge_id: {name}_{name2}
      action: {action}
      action_type: {action_type}
      config: []
      fail_policy: fail
      fluid_navigation: true
      goal:
        target_pose:
          header:
            frame_id: $node.parent_frame
          pose: $node.pose
      node: {name2}
      recovery_behaviours_config: ''
      restrictions_planning: 'True'
      restrictions_runtime: obstacleFree_1
""".format(**edge_details)

def get_verts():
    return """
verts:
  verts:
  - verts: &vert0
    - x: -0.389276951551
      y: 0.63791257143
    - x: -0.725811064243
      y: 0.177953019738
    - x: -0.63791257143
      y: -0.389276951551
    - x: -0.177953019738
      y: -0.725811064243
    - x: 0.389276951551
      y: -0.63791257143
    - x: 0.725811064243
      y: -0.177953019738
    - x: 0.63791257143
      y: 0.389276951551
    - x: 0.177953019738
      y: 0.725811064243
  - verts: &vert1
    - x: 0.3839717361251064
      y: -0.6411198818013286
    - x: 0.5264215248037732
      y: -0.212953957097135
    - x: 0.4432315207951729
      y: 0.3549856737865013
    - x: 0.1839678947585299
      y: 0.724309885809929
    - x: -0.3839717361251064
      y: 0.6411198818013286
    - x: -0.5264215248037732
      y: 0.212953957097135
    - x: -0.4432315207951729
      y: -0.3549856737865013
    - x: -0.1839678947585299
      y: -0.724309885809929
    verts: &vert3
    - x: 0.3839717361251064
      y: -0.6411198818013286
    - x: 0.5264215248037732
      y: -0.212953957097135
    - x: 0.4432315207951729
      y: 0.3549856737865013
    - x: 0.1839678947585299
      y: 0.724309885809929
    - x: -0.3839717361251064
      y: 0.6411198818013286
    - x: -0.5264215248037732
      y: 0.212953957097135
    - x: -0.4432315207951729
      y: -0.3549856737865013
    - x: -0.1839678947585299
      y: -0.724309885809929
"""

def get_neighbours(grid, ri, ci):
    neighbours = []
    h,v = np.array(grid.shape)-1
    if ri-1 >= 0: neighbours+=[[ri-1, ci, grid[ri-1][ci] ]]
    if ci-1 >= 0: neighbours+=[[ri, ci-1, grid[ri][ci-1] ]]
    if ri+1 <= v: neighbours+=[[ri+1, ci, grid[ri+1][ci] ]]
    if ci+1 <= h: neighbours+=[[ri, ci+1, grid[ri][ci+1] ]]
    return neighbours

def generate_tmap(grid):
    renders = {
      '0': {'type': 'walkway',         'vert': '*vert0'},
      '1': {'type': 'warehouse_shelf', 'vert': '*vert1'},
      '2': {'type': 'pole',            'vert': '*vert2'}}

    # Get standard vertice points
    verts = get_verts()

    # Get tmap base setup
    tmap_details = {'gen_time': '2022-06-23_13-10-11', 'location': 'riseholme'}
    tmap = get_tmap(tmap_details)

    for ri,r in enumerate(grid):
        for ci,c in enumerate(grid[ri]):

            # Skip pole nodes
            if str(grid[ri][ci]) == "2": continue

            # Generate generic node template
            cat = str(grid[ri][ci])
            name = "%s-r%s-c%s"%(renders[cat]['type'], ri, ci)
            x = ci*shelf_dim[0] - (0.5*shelf_dim[0]*(len(grid)-1))
            y = ri*shelf_dim[1] - (0.5*shelf_dim[1]*(len(grid[ri])-1))
            node_details = {'name':name, 'location':tmap_details['location'], 'vert': renders[cat]['vert'], 'x':x, 'y':y}
            node = get_node(node_details)

            #Get neighbouring edges
            neighbours = get_neighbours(grid, ri, ci)
            if any([n[2] for n in neighbours if str(n[2]) != "2"]):
                node += """    edges:
"""
            for nei in neighbours:

                #Skip if pole
                if str(nei[2]) == "2": continue

                # Generate edge
                neighbour = str(grid[nei[0], nei[1]])
                name2 = "%s-r%s-c%s"%(renders[str(nei[2])]['type'], nei[0], nei[1])
                edge_details = {'name':name, 'name2':name2, 'action':'move_base', 'action_type':'move_base_msgs/MoveBaseGoal'}
                node += get_edge(edge_details)

            tmap+=node
    tmap+=verts
    return tmap


tmap = generate_tmap(grid)
tmap_path = "/home/diababa/warez/src/warez/config/scenario_object_search_arena/config/tmaps/tmap_AUTO.yaml"
#print("\n\n+=+=+=+=+\n")

with open(tmap_path, 'w+') as f:
    f.write(tmap)
