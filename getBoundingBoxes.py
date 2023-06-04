import json
from PIL import Image
import argparse


parser = argparse.ArgumentParser(description='A script to get Open Images bounding boxes.')
parser.add_argument("labelName", type=str, help="The name of the label it will be called in Edge Impulse.")
parser.add_argument("--whitespace", type=bool, default=False, help="Whether to include whitespace and linebreaks")
args = parser.parse_args()


def openFile(location):
    file = open(location, "r")
    fileString = file.read()
    file.close()
    return fileString

data = openFile("working/loadLater.txt")
data = json.loads(data)


boxesDict = {"version":1,"type": "bounding-box-labels","boundingBoxes":{}}
for i, a in enumerate(data):
    try:
        boxesDict["boundingBoxes"][data[i][0] + ".jpg"]
    except KeyError:
        boxesDict["boundingBoxes"][data[i][0] + ".jpg"] = []
    curImage = Image.open("downloadedImages/" + data[i][0] + ".jpg")
    imageWidth = curImage.size[0]
    imageHeight = curImage.size[1]
    x = int(float(data[i][4]) * imageWidth)
    y = int(float(data[i][6]) * imageHeight)
    width = int((float(data[i][5]) * imageWidth) - (float(data[i][4]) * imageWidth))
    height = int((float(data[i][7]) * imageHeight) - (float(data[i][6]) * imageHeight))
    boxesDict["boundingBoxes"][data[i][0] + ".jpg"].append({"label": args.labelName, "x": x, "y": y, "width": width, "height": height})

f = open("downloadedImages/bounding_boxes.labels", "w")
if(args.whitespace):
    f.write(json.dumps(boxesDict, indent=4))
else:
    f.write(json.dumps(boxesDict, indent=0))
f.close()