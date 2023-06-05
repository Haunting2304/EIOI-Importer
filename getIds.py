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
import os
import common

parser = argparse.ArgumentParser(description='A script to get Open Images image IDs.')
parser.add_argument("csvBoxes", type=str, help="The CSV file with the boxes.")
parser.add_argument("csvClass", type=str, help="The CSV file with the class names.")
parser.add_argument("imageSet", type=str, help="The image set the CSV is from. eg. \"train\", \"test\"")
parser.add_argument("classFile", type=str, help="File containing the names of the classes you want to download on each line. Example file: https://pastebin.com/raw/LS1p0GBf")
parser.add_argument("--limit", default=None, type=int, help="A limit on the amount of bounding boxes(not images) that will be downloaded. ")
parser.add_argument("--getExtraBoxes", default=True, type=int, help="Whether to include all the boxes from the images that are downloaded")
args = parser.parse_args()


data = common.openCSV(args.csvBoxes)

classNames = common.openCSV(args.csvClass)

downloadClasses = common.openFile(args.classFile)
downloadClasses = downloadClasses.splitlines()
for i, x in enumerate(downloadClasses):
    downloadClasses[i] = downloadClasses[i].strip()

lutIndex = {}
counter = []
for i, x in enumerate(downloadClasses):
    lutIndex[common.classNameToClassId(x, classNames)] = i
    counter.append(0)

def determine(x):
    global counter
    global lutIndex
    if (not (x[2] in lutIndex)):
        return False
    if x[3] != "1" or x[11] == "1" or counter[lutIndex[x[2]]] >= args.limit:
        return False
    counter[lutIndex[x[2]]] += 1
    return True

dataSorted = data
dataSorted = [x for x in dataSorted if determine(x)]


if not os.path.exists("working"):
    os.makedirs("working")


mainStr = ""
alreadyWritten = []
for i, x in enumerate(dataSorted):
    if mainStr.find(dataSorted[i][0]) == -1:
        mainStr += args.imageSet + "/" + dataSorted[i][0] + "\n"

f = open("working/imageIds.txt", "w")
f.write(mainStr)
f.close()




def determineExtra(x):
    for y in dataSorted:        
        if x[0] == y[0] and (x[2] != y[2] and x[4] != y[4] and x[5] != y[5] and x[6] != y[6] and x[7] != y[7]):
            return True
    return False

if(args.getExtraBoxes == True):
    dataExtra = data
    dataExtra = [x for x in dataExtra if determineExtra(x)] # Probably really slow, I don't really care though
    for x in dataExtra:
        dataSorted.append(x)


f = open("working/data", "w")
output = json.dumps(dataSorted, indent=0)
output = output.replace("\n", "")
f.write(output)
f.close()