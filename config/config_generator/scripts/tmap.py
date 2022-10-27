import numpy as np
import rospkg

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
    restrictions_planning: {restrictions}
    restrictions_runtime: obstacleFree_1
    verts: *{vert}
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
      restrictions_planning: {restrictions}
      restrictions_runtime: obstacleFree_1
""".format(**edge_details)



def get_verts():
    return """
verts:
  verts:
  - verts: &vert0
    - x: -0.13
      y:  0.213
    - x: -0.242
      y:  0.059
    - x: -0.213
      y: -0.13
    - x: -0.059
      y: -0.242
    - x:  0.13
      y: -0.213
    - x:  0.242
      y: -0.059
    - x:  0.213
      y:  0.13
    - x:  0.059
      y:  0.242
  - verts: &vert1
    - x:  0.128
      y: -0.214
    - x:  0.175
      y: -0.071
    - x:  0.148
      y:  0.118
    - x:  0.061
      y:  0.241
    - x: -0.128
      y:  0.214
    - x: -0.175
      y: 0.071
    - x: -0.148
      y: -0.118
    - x: -0.061
      y: -0.241
"""


def get_neighbours(grid, ri, ci):
    neighbours = []
    h,v = np.array(grid.shape)-1
    if ri-1 >= 0: neighbours+=[[ri-1, ci, grid[ri-1][ci] ]]
    if ci-1 >= 0: neighbours+=[[ri, ci-1, grid[ri][ci-1] ]]
    if ri+1 <= v: neighbours+=[[ri+1, ci, grid[ri+1][ci] ]]
    if ci+1 <= h: neighbours+=[[ri, ci+1, grid[ri][ci+1] ]]
    return neighbours



def tmap(grid, yml_cats):
    dims = (yml_cats['grid']['resolution']['x'], yml_cats['grid']['resolution']['y'])
    save_as = yml_cats['CONFIG']
    renders = yml_cats['renderings']

    # Get standard vertice points
    verts = get_verts()

    # Get tmap base setup
    tmap_details = {'gen_time': '2022-06-23_13-10-11', 'location': 'auto_gen'}
    tmap = get_tmap(tmap_details)

    for ri,r in enumerate(grid):
        for ci,c in enumerate(grid[ri]):

            # Skip pole nodes
            cat = grid[ri][ci]
            ren = renders[cat]['sdf']
            if ren == 'pole': continue

            # Generate generic node template
            name = "%s-r%s-c%s"%(ren, ri, ci)
            x = ci*dims[0] - (0.5*dims[0]*(len(grid)-1))
            y = ri*dims[1] - (0.5*dims[1]*(len(grid[ri])-1))
            node_details = {'name':name,
                            'location':tmap_details['location'],
                            'vert': renders[cat]['vert'],
                            'x':x,
                            'y':y,
                            'restrictions':renders[cat]['restrictions'][cat]}
            node = get_node(node_details)

            #Get neighbouring edges
            neighbours = get_neighbours(grid, ri, ci)
            edge_list = []

            for nei in neighbours:

                #Skip if pole
                cat2 = nei[2]
                ren2 = renders[cat2]['sdf']
                if ren2 == 'pole': continue

                # Generate edge
                neighbour = str(grid[nei[0], nei[1]])
                name2 = "%s-r%s-c%s"%(ren2, nei[0], nei[1])
                edge_details = {'name':name,
                                'name2':name2,
                                'action':'move_base',
                                'action_type':'move_base_msgs/MoveBaseGoal',
                                'restrictions': renders[cat]['restrictions'][cat2]}
                edge_list += [get_edge(edge_details)]

            # Add edges or empty list
            if edge_list:
                node += """    edges:
""" + ''.join(edge_list)
            else:
                node += """    edges: []
"""

            tmap+=node
    verts+=tmap

    # Save TMap file
    tmap = verts
    if save_as:
        path = rospkg.RosPack().get_path("config_generator")+"/../scenarios/scenario___%s/config/tmaps/tmap.tmap2"%(save_as)
        with open(path, 'w+') as f:
            f.write(tmap)
