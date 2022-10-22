import time, os
import rospkg


def world(grid, dims, sdf):
    sdf_folder = rospkg.RosPack().get_path("config_generator")+"/../warez_models/"

    def send_cmd (name, x, y, z=0, sdf="warehouse_shelf"):
        print("\nRendering: %s"%name)
        file = sdf_folder + "%s/%s.sdf"%(sdf,sdf)
        command = "rosrun gazebo_ros spawn_model -file %s -sdf -model %s -x %s -y %s -z %s"
        os.system(command%(file, name, x, y, z))

    for ri,r in enumerate(grid):
        for ci,c in enumerate(grid[ri]):
            if grid[ri][ci] > 0:
                x = ci*dims[0] - (0.5*dims[0]*(len(grid)-1))
                y = ri*dims[1] - (0.5*dims[1]*(len(grid[ri])-1))

                renders = {1:'warehouse_shelf', 2:'pole'}
                send_cmd("%s_%s_%s"%(renders[grid[ri][ci]],ri,ci), x, y, sdf=renders[grid[ri][ci]])
                time.sleep(0.2)

