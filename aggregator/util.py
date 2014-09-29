import re
import argparse
import datetime
import os
from os import listdir
from os.path import isfile, join

cgpBasePath = ""
os.chdir(cgpBasePath)


def lastFlattenedData():
    files = [f for f in listdir(cgpBasePath + "/flatten") if isfile(join(cgpBasePath + "/flatten", f))]

    convertedDates = []
    for date in files:
        date = re.sub('\.gz$', '', date)
        convertedDates.append(datetime.datetime.strptime(date, '%Y-%m-%d-%H'))
    convertedDates = sorted(convertedDates)

    if len(convertedDates) > 0:
        print convertedDates[-1]
        return convertedDates[-1]
    else:
        return None


def lastDownloadedData():
    files = [f for f in listdir(cgpBasePath + "/data") if isfile(join(cgpBasePath + "/data", f))]

    convertedDates = []
    for date in files:
        date = re.sub('\.json.gz$', '', date)
        convertedDates.append(datetime.datetime.strptime(date, '%Y-%m-%d-%H'))
    convertedDates = sorted(convertedDates)

    if len(convertedDates) > 0:
        print convertedDates[-1]
        return convertedDates[-1]
    else:
        return None


def lastProcessedData():
    files = [f for f in listdir(cgpBasePath + "/processed") if isfile(join(cgpBasePath + "/processed", f))]

    convertedDates = []
    for date in files:
        date = re.sub('\.gz$', '', date)
        convertedDates.append(datetime.datetime.strptime(date, '%Y-%m-%d-%H'))
    convertedDates = sorted(convertedDates)

    if len(convertedDates) > 0:
        print convertedDates[-1]
        return convertedDates[-1]
    else:
        return None


def init():
    if os.path.isfile("keyfile.p12") is False:
        print "KeyFile is missing."
    if os.path.isdir("data") is False:
        print "[Data] folder not found. Creating folder..."
        os.makedirs("data")
    if os.path.isdir("flatten") is False:
        print "[Flatten] folder not found. Creating folder..."
        os.makedirs("flatten")
    if os.path.isdir("processed") is False:
        print "[Processed] folder not found. Creating folder..."
        os.makedirs("processed")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-ldd", "--lastdownloadeddata", action="store_true")
    group.add_argument("-lfd", "--lastflatteneddata", action="store_true")
    group.add_argument("-lpd", "--lastprocesseddata", action="store_true")
    group.add_argument("-i", "--init", action="store_true")
    args = parser.parse_args()

    if args.lastdownloadeddata:
        lastDownloadedData()
    elif args.lastflatteneddata:
        lastFlattenedData()
    elif args.lastprocesseddata:
        lastProcessedData()
    elif args.init:
        init()


if __name__ == "__main__":
    main()
