import os
import shutil
from os import listdir
from os.path import isfile, join

import util


config = util.getConfig()
basePath = config.basePath
flattenPath = "/flatten"
processedPath = "/processed"
externalPath = "/external"
os.chdir(basePath)


def upload(fileName):
    svcAccount = config.bigQuerySvcAccount
    scvAccountKeyFile = "keyfile.p12"
    svcAccountCredFile = ".bigquery.v2.token"

    projectId = config.bigQueryProjectId
    datasetName = config.bigQueryDataSet

    dataLocation = basePath + flattenPath + "/" + fileName
    processedLocation = basePath + processedPath + "/" + fileName
    schemaLocation = basePath + externalPath + "/" + "schema.js"

    os.system("sudo bq --service_account " + svcAccount + " --service_account_private_key_file " + scvAccountKeyFile + " --service_account_credential_file " + svcAccountCredFile + " --project_id " + projectId + " load " + datasetName + " " + dataLocation + " " + schemaLocation)

    move(dataLocation, processedLocation)


def move(src, dest):
    shutil.move(src, dest)


def getFlattenList():
    files = [f for f in listdir(basePath + flattenPath) if isfile(join(basePath + flattenPath, f))]

    if len(files) > 0:
        return files
    else:
        print "No file found in " + flattenPath
        return None


def main():
    list = getFlattenList()
    if list != None:
        for file in list:
            print "Uploading : " + str(file)
            upload(file)
    else:
        print "No file to upload"


if __name__ == "__main__":
    main()