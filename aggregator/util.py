import re
import argparse
import datetime
import os
import ConfigParser
import inspect
from os import listdir
from os.path import isfile, join

basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(basePath)


class Configuration():
    def __init__(self):
        configParser = ConfigParser.RawConfigParser(allow_no_value=False)
        configParser.read(basePath + '/config')
        self.basePath = basePath
        self.bigQueryProjectId = configParser.get('aggregator', 'bigQueryProjectId')
        self.bigQuerySvcAccount = configParser.get('aggregator', 'bigQuerySvcAccount')
        self.bigQueryDataSet = configParser.get('aggregator', 'bigQueryDataSet')


def getConfig():
    return Configuration()


def getLastFlattenedDate():
    files = [f for f in listdir(basePath + "/flatten") if isfile(join(basePath + "/flatten", f))]

    convertedDates = []
    for date in files:
        date = re.sub('\.gz$', '', date)
        convertedDates.append(datetime.datetime.strptime(date, '%Y-%m-%d-%H'))
    convertedDates = sorted(convertedDates)

    if len(convertedDates) > 0:
        return convertedDates[-1]
    else:
        return None


def getLastDownloadedDate():
    files = [f for f in listdir(basePath + "/data") if isfile(join(basePath + "/data", f))]

    convertedDates = []
    for date in files:
        date = re.sub('\.json.gz$', '', date)
        convertedDates.append(datetime.datetime.strptime(date, '%Y-%m-%d-%H'))
    convertedDates = sorted(convertedDates)

    if len(convertedDates) > 0:
        return convertedDates[-1]
    else:
        return None


def getFirstProcessedDate():
    files = [f for f in listdir(basePath + "/processed") if isfile(join(basePath + "/processed", f))]

    convertedDates = []
    for date in files:
        date = re.sub('\.gz$', '', date)
        convertedDates.append(datetime.datetime.strptime(date, '%Y-%m-%d-%H'))
    convertedDates = sorted(convertedDates)

    if len(convertedDates) > 0:
        return convertedDates[0]
    else:
        return None


def getLastProcessedDate():
    files = [f for f in listdir(basePath + "/processed") if isfile(join(basePath + "/processed", f))]

    convertedDates = []
    for date in files:
        date = re.sub('\.gz$', '', date)
        convertedDates.append(datetime.datetime.strptime(date, '%Y-%m-%d-%H'))
    convertedDates = sorted(convertedDates)

    if len(convertedDates) > 0:
        return convertedDates[-1]
    else:
        return None


def getProcessedDateDelta():
    a = getFirstProcessedDate()
    b = getLastProcessedDate()
    return b - a


def getLastMonthsDate():
    b = getLastProcessedDate()
    a = b + datetime.timedelta(days=-30)
    return a


def init():
    if os.path.isfile("keyfile.p12") is False:
        print "KeyFile is missing."
    if os.path.isfile(".bigquery.v2.token") is False:
        print ".bigquery.v2.token is missing."
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
    group.add_argument("-ldd", "--lastdownloadeddate", action="store_true")
    group.add_argument("-lfd", "--lastflatteneddate", action="store_true")
    group.add_argument("-lpd", "--lastprocesseddate", action="store_true")
    group.add_argument("-fpd", "--firstprocesseddate", action="store_true")
    group.add_argument("-pdd", "--processeddatedelta", action="store_true")
    group.add_argument("-lmd", "--lastmonthsdate", action="store_true")
    group.add_argument("-i", "--init", action="store_true")
    args = parser.parse_args()

    if args.lastdownloadeddate:
        print getLastDownloadedDate()
    elif args.lastflatteneddate:
        print getLastFlattenedDate()
    elif args.lastprocesseddate:
        print getLastProcessedDate()
    elif args.firstprocesseddate:
        print getFirstProcessedDate()
    elif args.processeddatedelta:
        print getProcessedDateDelta()
    elif args.lastmonthsdate:
        print getLastMonthsDate()
    elif args.init:
        init()


if __name__ == "__main__":
    main()
