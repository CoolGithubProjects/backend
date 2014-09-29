import os
import shutil
import datetime
import subprocess
import util

cgpBasePath = ""
dataPath = "/data"
os.chdir(cgpBasePath + dataPath)


def download(date):
    date = date.strftime("%Y-%m-%d-%-H")
    url = "http://data.githubarchive.org/" + date + ".json.gz"
    subprocess.call(["wget", url], stdout=True)


def move(src, dest):
    shutil.move(src, dest)


def main():
    date = util.lastFlattenedData()
    if date != None:
        while date < datetime.datetime.now():
            date = date + datetime.timedelta(hours=1)
            download(date)
    else:
        date = util.lastProcessedData()
        if date != None:
            while date < datetime.datetime.now():
                date = date + datetime.timedelta(hours=1)
                download(date)


if __name__ == "__main__":
    main()