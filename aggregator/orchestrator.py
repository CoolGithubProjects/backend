import os
import subprocess

import util


config = util.getConfig()
basePath = config.basePath
os.chdir(basePath)

subprocess.call(["python", basePath + "/downloader.py"], stdout=True)
subprocess.call(["python", basePath + "/flattener.py"], stdout=True)
subprocess.call(["python", basePath + "/uploader.py"], stdout=True)