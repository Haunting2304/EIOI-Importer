def openFile(location):
    file = open(location, "r", encoding="utf-8")
    fileString = file.read()
    file.close()
    return fileString
def downloadClassesIndex(x, downloadClasses):
    for i, y in enumerate(downloadClasses):
        if x == y:
            return i
    return -1
def classNameToClassId(x, classNames):
    for i, y in enumerate(classNames):
        if x == y[1]:
            return y[0]
    raise Exception("Could not find class name in CSV")
def classIdToClassName(x, classNames):
    for i, y in enumerate(classNames):
        if x == y[0]:
            return y[1]
    raise Exception("Could not find class ID in CSV")
def openCSV(location):
    data = openFile(location)
    data = data.splitlines()

    for i, x in enumerate(data):
        data[i] = data[i].strip()

    del data[0]

    for i, x in enumerate(data):
        data[i] = data[i].split(",")
    return data