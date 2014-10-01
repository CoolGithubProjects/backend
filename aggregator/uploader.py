import os
import shutil
import threading
from os import listdir
from os.path import isfile, join
from threading import Thread

import util


config = util.getConfig()
basePath = config.basePath
flattenPath = "/flatten"
processedPath = "/processed"
externalPath = "/external"
os.chdir(basePath)

lock = threading.Lock()


def getFile():
    with lock:
        if len(fileList) > 0:
            fileName = fileList.pop()
            print "Uploading : " + str(fileName)
            return fileName
    return None


def upload():
    while True:
        fileName = getFile()
        if fileName:
            svcAccount = config.bigQuerySvcAccount
            scvAccountKeyFile = "keyfile.p12"
            svcAccountCredFile = ".bigquery.v2.token"

            projectId = config.bigQueryProjectId
            datasetName = config.bigQueryDataSet

            dataLocation = basePath + flattenPath + "/" + fileName
            processedLocation = basePath + processedPath + "/" + fileName
            schemaLocation = basePath + externalPath + "/" + "schema.js"

            os.system("sudo bq --service_account " + svcAccount + " --service_account_private_key_file " + scvAccountKeyFile + " --service_account_credential_file " + svcAccountCredFile + " --project_id " + projectId + " load " + datasetName + " " + dataLocation + " " + schemaLocation)

            shutil.move(dataLocation, processedLocation)
        else:
            break;
    return


def getFlattenList():
    files = [f for f in listdir(basePath + flattenPath) if isfile(join(basePath + flattenPath, f))]
    if len(files) > 0:
        return files
    else:
        print "No file found in " + flattenPath
        return None


def main():
    global fileList
    fileList = getFlattenList()
    if fileList != None:
        for i in range(5):
            t = Thread(target=upload)
            t.start()
    else:
        print "No file to upload"


if __name__ == "__main__":
    main()