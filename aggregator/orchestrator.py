import os
import subprocess

cgpBasePath = ""
os.chdir(cgpBasePath)

subprocess.call(["python", cgpBasePath + "/downloader.py"], stdout=True)
subprocess.call(["python", cgpBasePath + "/flattener.py"], stdout=True)
subprocess.call(["python", cgpBasePath + "/uploader.py"], stdout=True)