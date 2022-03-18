import os
import sys

path_ = os.path.abspath(__file__).replace("\\", "/")
location_folders = os.path.dirname(path_).split("/")
removed_folder = ""
while removed_folder != "notebook":
    removed_folder = location_folders.pop(-1)
location = "/".join(location_folders)
sys.path.append(location)
