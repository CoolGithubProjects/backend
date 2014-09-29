from os import listdir
from os.path import isfile, join
import datetime as dt
import os
import re

cgpBasePath = ""
dataPath = "/data"
os.chdir(cgpBasePath + "/external")

files = [f for f in listdir(cgpBasePath + dataPath) if isfile(join(cgpBasePath + dataPath, f))]

if len(files) < 0:
    print "No file found."
else:
    for f in files:
        start = dt.datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

        path = cgpBasePath + dataPath + "/" + f
        date = re.sub('\.json.gz$', '', f)
        os.system("sudo ruby flatten.rb -i " + path + " -o ../flatten/" + date)

        end = dt.datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
        print "Processing file [" + f + "] complete." + "[" + str(start) + " | " + str(end) + "]"
        os.remove(cgpBasePath + dataPath + "/" + f)
