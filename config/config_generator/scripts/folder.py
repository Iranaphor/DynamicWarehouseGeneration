import os
import shutil
import rospkg


def folder(save_as):
    root = rospkg.RosPack().get_path('config_generator')+"/../scenarios/"
    conf = rospkg.RosPack().get_path("config_generator")+"/config/%s.yaml"%(save_as)
    temp = root + "scenario_template"
    pack = root + "scenario___"+save_as
    if not os.path.exists(pack):
        shutil.copytree(temp, pack)
        with open(pack+"/CMakeLists.txt") as f: newText=f.read().replace("scenario_template", "scenario___"+save_as)
        with open(pack+"/CMakeLists.txt", "w") as f: f.write(newText)
        with open(pack+"/package.xml") as f: newText=f.read().replace("scenario_template", "scenario___"+save_as)
        with open(pack+"/package.xml", "w") as f: f.write(newText)
        shutil.copy(conf, pack+"/config/config.yaml")
