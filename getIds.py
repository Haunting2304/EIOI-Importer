# Update it to check for zero licence

# 0 : ID
# 1 : Source
# 2 : LabelName
# 3 : Confidence
# 4 : XMin
# 5 : XMax
# 6 : YMin
# 7 : YMax
# 8 : IsOccluded
# 9 : IsTruncated
# 10: IsGroupOf
# 11: IsDepiction
# 12: IsInside
# 13: XClick1X
# 14: XClick2X
# 15: XClick3X
# 16: XClick4X
# 17: XClick1Y
# 18: XClick2Y
# 19: XClick3Y
# 20: XClick4Y

import json
import argparse


parser = argparse.ArgumentParser(description='A script to get Open Images image IDs.')
parser.add_argument("csv", type=str, help="The CSV file you are using.")
parser.add_argument("imageSet", type=str, help="The image set the CSV is from. eg. \"train\", \"test\"")
parser.add_argument("classID", type=str, help="The ID of the class you are downloading. eg. \"/m/01m2v\"")
args = parser.parse_args()


def openFile(location):
    file = open(location, "r")
    fileString = file.read()
    file.close()
    return fileString

data = openFile(args.csv)
data = data.splitlines()

for i, x in enumerate(data):
    data[i] = data[i].strip()

del data[0]

for i, x in enumerate(data):
    data[i] = data[i].split(",")


def determine(x):
    if x[2] != args.classID or x[3] != "1" or x[11] == "1":
        return False
    return True

data = [x for x in data if determine(x)]

f = open("working/loadLater.txt", "w")
f.write(json.dumps(data, indent=0))
f.close()


mainStr = ""
alreadyWritten = []
for i, x in enumerate(data):
    if mainStr.find(data[i][0]) == -1:
        mainStr += args.imageSet + "/" + data[i][0] + "\n"

f = open("working/imageIds.txt", "w")
f.write(mainStr)
f.close()