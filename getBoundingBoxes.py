import json
from PIL import Image
import argparse
import common


parser = argparse.ArgumentParser(description='A script to get Open Images bounding boxes.')
parser.add_argument("csvClass", type=str, help="The CSV file with the class names.")
parser.add_argument("classFile", type=str, help="File containing the names of the classes you want to download on each line. Example file: https://pastebin.com/raw/LS1p0GBf")
parser.add_argument("--labelOther", type=str, default="unknown", help="The label for the other random bounding boxes in the image. Default=\"unknown\"")
parser.add_argument("--whitespace", type=bool, default=False, help="Whether to include whitespace and linebreaks")
args = parser.parse_args()


data = common.openFile("working/data")
data = json.loads(data)

classNames = common.openCSV(args.csvClass)

downloadClasses = common.openFile(args.classFile)
downloadClasses = downloadClasses.splitlines()
for i, x in enumerate(downloadClasses):
    downloadClasses[i] = downloadClasses[i].strip()


boxesDict = {"version":1,"type": "bounding-box-labels","boundingBoxes":{}}
for i, a in enumerate(data):
    try:
        curImage = Image.open("downloadedImages/" + data[i][0] + ".jpg")
        imageWidth = curImage.size[0]
        imageHeight = curImage.size[1]
        x = int(float(data[i][4]) * imageWidth)
        y = int(float(data[i][6]) * imageHeight)
        width = int((float(data[i][5]) * imageWidth) - (float(data[i][4]) * imageWidth))
        height = int((float(data[i][7]) * imageHeight) - (float(data[i][6]) * imageHeight))
        try:
            boxesDict["boundingBoxes"][data[i][0] + ".jpg"]
        except KeyError:
            boxesDict["boundingBoxes"][data[i][0] + ".jpg"] = []
        index = common.downloadClassesIndex(common.classIdToClassName(data[i][2], classNames), downloadClasses)
        if(index == -1):
            label = args.labelOther
        else:
            label = downloadClasses[index].lower()
        boxesDict["boundingBoxes"][data[i][0] + ".jpg"].append({"label": label, "x": x, "y": y, "width": width, "height": height})
    except FileNotFoundError:
        print("Could not find file " + "downloadedImages/" + data[i][0] + ".jpg")

f = open("downloadedImages/bounding_boxes.labels", "w")
if(args.whitespace):
    f.write(json.dumps(boxesDict, indent=4))
else:
    output = json.dumps(boxesDict, indent=0)
    output = output.replace("\n", "")
    f.write(output)
f.close()