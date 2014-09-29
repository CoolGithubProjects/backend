import os
import shutil

from os import listdir
from os.path import isfile, join

cgpBasePath = ""
flattenPath = "/flatten"
processedPath = "/processed"
externalPath = "/external"
os.chdir(cgpBasePath)


def upload(fileName):
    svcAccount = ""
    scvAccountKeyFile = "keyfile.p12"
    svcAccountCredFile = "../.bigquery.v2.token"

    projectId = ""
    datasetName = "V2.GHEvents"

    dataLocation = cgpBasePath + flattenPath + "/" + fileName
    processedLocation = cgpBasePath + processedPath + "/" + fileName
    schemaLocation = cgpBasePath + externalPath + "/" + "schema.js"

    os.system("sudo bq --service_account " + svcAccount + " --service_account_private_key_file " + scvAccountKeyFile + " --service_account_credential_file " + svcAccountCredFile + " --project_id " + projectId + " load " + datasetName + " " + dataLocation + " " + schemaLocation)

    move(dataLocation, processedLocation)


def move(src, dest):
    shutil.move(src, dest)


def getFlattenList():
    files = [f for f in listdir(cgpBasePath + flattenPath) if isfile(join(cgpBasePath + flattenPath, f))]

    if len(files) > 0:
        return files
    else:
        print "No file found in " + flattenPath
        return None


def main():
    # get file list
    list = getFlattenList()
    if list != None:
        for file in list:
            print "Uploading : " + str(file)
            upload(file)
    else:
        print "No file to upload"


if __name__ == "__main__":
    main()