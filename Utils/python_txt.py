

def txtRead(strFilename):
    with open(strFilename, 'r') as f:
        listData = f.read()
    return listData


def txtWrite(strFilename, strData):
    with open(strFilename, 'w') as f:
        f.write(strData)






