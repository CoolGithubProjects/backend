from os import listdir
from os.path import isfile, join
import os
import re

import util


config = util.getConfig()
basePath = config.basePath
dataPath = "/data"
os.chdir(basePath + "/external")

files = [f for f in listdir(basePath + dataPath) if isfile(join(basePath + dataPath, f))]

if len(files) < 0:
    print "No file found."
else:
    for f in files:
        path = basePath + dataPath + "/" + f
        date = re.sub('\.json.gz$', '', f)
        os.system("sudo ruby flatten.rb -i " + path + " -o ../flatten/" + date)
        os.remove(basePath + dataPath + "/" + f)
